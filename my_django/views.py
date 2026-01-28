from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingredient
from .forms import IngredientForm
from django.utils import timezone
from datetime import timedelta

# 1. 냉장고 메인 화면 (재료 목록 표시)
def fridge_main(request):
    # 카테고리별 정렬 및 최근 추가 순서
    ingredients = Ingredient.objects.all().order_by('category', '-added_at')
    return render(request, 'my_django/fridge_main.html', {'ingredients': ingredients})

# 2. 재료 선택 및 추가 화면 (폼 사용)
def ingredient_select(request):
    sample_data = {
        '채소': ['브로콜리', '감자', '고추', '당근', '오이', '파', '파프리카', '토마토', '버섯', '무', '마늘', '양파', '애호박'],
        '양념': ['와사비', '간장', '고추장', '된장', '마요네즈', '케첩'],
        '해산물': ['게', '연어', '오징어', '참치', '새우'],
        '육류': ['소고기', '돼지고기', '닭고기', '오리고기'],
        '가공식품': ['두부', '베이컨', '소시지', '어묵', '햄'],
        '과일': ['사과', '망고', '바나나', '아보카도', '레몬']
    }
    
    # GET 요청 시 빈 폼을 함께 전달하여 화면에서 사용할 수 있게 함
    form = IngredientForm()
    context = {
        'sample_data': sample_data,
        'form': form
    }
    return render(request, 'my_django/ingredient_select.html', context)

# 3. 실제 재료 추가 처리 (IngredientForm 활용)
def add_ingredient(request):
    if request.method == "POST":
        # 폼을 통해 데이터 받기 (name, category, quantity, expiry_date 포함)
        form = IngredientForm(request.POST)
        
        if form.is_valid():
            # 유효성 검사 통과 시 바로 저장
            form.save()
        else:
            # 만약 폼이 유효하지 않은데 직접 입력값이 들어온 경우 (예비 로직)
            name = request.POST.get('name')
            category = request.POST.get('category')
            quantity = request.POST.get('quantity', 1)
            
            Ingredient.objects.create(
                name=name,
                category=category,
                quantity=quantity,
                expiry_date=timezone.now().date() + timedelta(days=7)
            )
            
    return redirect('my_django:fridge_main')

# 4. 유통기한 날짜 및 정보 수정
def update_expiry(request, pk):
    item = get_object_or_404(Ingredient, pk=pk)
    if request.method == "POST":
        # 기존 데이터를 폼에 넣고 수정된 내용만 반영
        form = IngredientForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            
    return redirect('my_django:fridge_main')

# 5. 재료 삭제
def delete_ingredient(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Ingredient, pk=pk)
        item.delete()
    return redirect('my_django:fridge_main')