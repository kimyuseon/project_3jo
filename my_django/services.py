import os
import base64
from typing import List
from pydantic import BaseModel, Field
from django.conf import settings  
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# --- [Pydantic 모델 정의] ---
class ReceiptItem(BaseModel):
    name: str = Field(description="품목 이름")
    count: int = Field(description="수량")

class ReceiptData(BaseModel):
    items: List[ReceiptItem]

class Recipe(BaseModel):
    title: str = Field(description="요리 이름")
    description: str = Field(description="요리에 대한 간단한 설명")
    ingredients: List[str] = Field(description="필요한 전체 재료 목록")
    steps: List[str] = Field(description="조리 단계")
    tip: str = Field(description="맛을 높이는 꿀팁")

class RecipeRecommendation(BaseModel):
    recipes: List[Recipe] = Field(description="추천 레시피 리스트 (최대 3개)")

# --- [공통 모델 설정 함수] ---
def get_model(temperature=0):
    api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv("GEMINI_API_KEY"))
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key, 
        temperature=temperature
    )

# --- [함수 1: 영수증 분석] ---
def extract_receipt_data_langchain(image_file):
    model = get_model(temperature=0)
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
            {"type": "image_url", "image_url": {"url": "{full_image_url}"}} 
        ])
    ])

    chain = prompt | model | parser
    return chain.invoke({"full_image_url": full_image_url, "format_instructions": parser.get_format_instructions()})

# --- [함수 2: 레시피 추천] ---
def get_recipe_recommendations_langchain(ingredient_names: List[str]):
    model = get_model(temperature=0.7)
    parser = JsonOutputParser(pydantic_object=RecipeRecommendation)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 냉장고 재료를 활용하는 전문 요리사야. 제공된 재료를 기반으로 맛있는 레시피를 추천해줘. {format_instructions}"),
        ("human", "내 냉장고 재료: {ingredients_str}. 이 재료들로 만들 수 있는 요리 3가지를 추천해줘.")
    ])

    chain = prompt | model | parser
    return chain.invoke({
        "ingredients_str": ", ".join(ingredient_names),
        "format_instructions": parser.get_format_instructions()
    })