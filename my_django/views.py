from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingredient

def fridge_main(request):
    ingredients = Ingredient.objects.all().order_by('category', '-added_at')
    return render(request, 'my_django/fridge_main.html', {'ingredients': ingredients})

def ingredient_select(request):
    sample_data = {
        '채소': ['브로콜리', '감자', '고추', '당근', '오이', '파', '파프리카', '토마토', '버섯', '무', '마늘', '양파', '애호박'],
        '양념': ['와사비', '간장', '고추장', '된장', '마요네즈', '케첩'],
        '해산물': ['게', '연어', '오징어', '참치', '새우'],
        '육류': ['소고기', '돼지고기', '닭고기', '오리고기'],
        '가공식품': ['두부', '베이컨', '소시지', '어묵', '햄'],
        '조미료': ['msg', '고춧가루', '기름', '소금', '후추', '참기름'],
        '과일': ['사과', '망고', '바나나', '아보카도', '레몬']

    }
    if request.method == "POST":
        Ingredient.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category')
        )
        return redirect('fridge_main')
    return render(request, 'my_django/ingredient_select.html', {'sample_data': sample_data})

def update_expiry(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Ingredient, pk=pk)
        expiry_date = request.POST.get('expiry_date')
        if expiry_date:
            item.expiry_date = expiry_date
            item.save()
    return redirect('fridge_main')

def delete_ingredient(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Ingredient, pk=pk)
        item.delete()
    return redirect('fridge_main')