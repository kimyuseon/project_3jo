from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingredient
from django.utils import timezone
from datetime import timedelta

# 1. 냉장고 메인 화면 (재료 목록 표시)
def fridge_main(request):
    # 카테고리별로 정렬하고, 최근 추가된 순서대로 가져옵니다.
    ingredients = Ingredient.objects.all().order_by('category', '-added_at')
    return render(request, 'my_django/fridge_main.html', {'ingredients': ingredients})

# 2. 재료 선택 화면 (샘플 데이터 표시)
def ingredient_select(request):
    sample_data = {
        '채소': ['브로콜리', '감자', '고추', '당근', '오이', '파', '파프리카', '토마토', '버섯', '무', '마늘', '양파', '애호박'],
        '양념': ['와사비', '간장', '고추장', '된장', '마요네즈', '케첩'],
        '해산물': ['게', '연어', '오징어', '참치', '새우'],
        '육류': ['소고기', '돼지고기', '닭고기', '오리고기'],
        '가공식품': ['두부', '베이컨', '소시지', '어묵', '햄'],
        '과일': ['사과', '망고', '바나나', '아보카도', '레몬']
    }
    # 화면을 보여주는 역할만 수행합니다.
    return render(request, 'my_django/ingredient_select.html', {'sample_data': sample_data})

# 3. 실제 재료 추가 처리 (POST 요청 전용)
def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        
        # 기본 유통기한을 오늘 기준 +7일로 설정하여 저장
        Ingredient.objects.create(
            name=name,
            category=category,
            expiry_date=timezone.now().date() + timedelta(days=7)
        )
    # 처리가 끝나면 메인 화면으로 리다이렉트
    return redirect('my_django:fridge_main')

# 4. 유통기한 날짜 수정
def update_expiry(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Ingredient, pk=pk)
        expiry_date = request.POST.get('expiry_date')
        if expiry_date:
            item.expiry_date = expiry_date
            item.save()
    return redirect('my_django:fridge_main')

# 5. 재료 삭제
def delete_ingredient(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Ingredient, pk=pk)
        item.delete()
    return redirect('my_django:fridge_main')