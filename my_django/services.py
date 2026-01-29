import os
import base64
from typing import List
from pydantic import BaseModel, Field
from django.conf import settings  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


class ReceiptItem(BaseModel):
    name: str = Field(description="품목 이름")
    count: int = Field(description="수량")

class ReceiptData(BaseModel):
    items: List[ReceiptItem]

def extract_receipt_data_langchain(image_file):
    api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv("GEMINI_API_KEY"))
    
    model = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash", 
        google_api_key=api_key,
        temperature=0
    )
    
    parser = JsonOutputParser(pydantic_object=ReceiptData)

    #이미지처리
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    content_type = getattr(image_file, 'content_type', 'image/png')
    full_image_url = f"data:{content_type};base64,{image_base64}"

    #프롬프트 구성
    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 영수증 분석 전문가야. 사용자의 영수증 이미지를 보고 품목과 수량을 정확히 추출해야 해. {format_instructions}"),
        ("human", [
            {"type": "text", "text": "이 영수증 사진에서 품목 이름과 수량을 뽑아줘."},
            {
                "type": "image_url", 
                "image_url": {"url": "{full_image_url}"} 
            }
        ])
    ])

    chain = prompt | model | parser

    result = chain.invoke({
        "full_image_url": full_image_url,
        "format_instructions": parser.get_format_instructions()
    })

    return result