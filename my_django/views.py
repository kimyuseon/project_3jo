from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import MasterIngredient, Ingredient
from .services import extract_receipt_data_langchain, get_recipe_recommendations_langchain

@login_required
def fridge_main(request):
    ingredients = Ingredient.objects.filter(user=request.user).order_by('master_ingredient__category', '-added_at')
    return render(request, 'my_django/fridge_main.html', {'ingredients': ingredients})

@login_required
def ingredient_select(request):
    masters = MasterIngredient.objects.all()
    organized_data = {}
    for item in masters:
        if item.category not in organized_data:
            organized_data[item.category] = []
        organized_data[item.category].append(item)
    return render(request, 'my_django/ingredient_select.html', {'organized_data': organized_data})

@login_required
def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity', 1)) 
        master_item = get_object_or_404(MasterIngredient, name=name)
        ingredient, created = Ingredient.objects.get_or_create(
            user=request.user, master_ingredient=master_item,
            defaults={'quantity': quantity, 'expiry_date': timezone.now().date() + timedelta(days=7)}
        )
        if not created:
            ingredient.quantity += quantity
            ingredient.save()
    return redirect('my_django:fridge_main')

@login_required
def update_expiry(request, pk):
    item = get_object_or_404(Ingredient, pk=pk, user=request.user)
    if request.method == "POST" and request.POST.get('expiry_date'):
        item.expiry_date = request.POST.get('expiry_date')
        item.save()
    return redirect('my_django:fridge_main')

@login_required
def delete_ingredient(request, pk):
    item = get_object_or_404(Ingredient, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
    return redirect('my_django:fridge_main')

@login_required
def upload_receipt(request):
    if request.method == 'POST' and request.FILES.get('receipt_image'):
        result = extract_receipt_data_langchain(request.FILES['receipt_image'])
        if result and 'items' in result:
            for item in result['items']:
                name = item.get('name')
                count = item.get('count', 1)
                master_item = MasterIngredient.objects.filter(name__icontains=name).first()
                if master_item:
                    user_ingredient, created = Ingredient.objects.get_or_create(
                        user=request.user, master_ingredient=master_item,
                        defaults={'quantity': count, 'expiry_date': timezone.now().date() + timedelta(days=7)}
                    )
                    if not created:
                        user_ingredient.quantity += int(count)
                        user_ingredient.save()
    return redirect('my_django:fridge_main')

# --- 레시피 추천 뷰 (추가) ---
@login_required
def recommend_recipe(request):
    user_ingredients = Ingredient.objects.filter(user=request.user).values_list('master_ingredient__name', flat=True)
    if not user_ingredients:
        return render(request, 'my_django/recipe_recommend.html', {'error': '냉장고에 재료가 없어요!'})
    try:
        recommendations = get_recipe_recommendations_langchain(list(user_ingredients))
        return render(request, 'my_django/recipe_recommend.html', {'recipes': recommendations.get('recipes', [])})
    except Exception as e:
        # print(f"레시피 추천 에러 발생: {e}")
        return render(request, 'my_django/recipe_recommend.html', {'error': 'AI 서버가 혼잡합니다. 잠시 후 시도해 주세요.'})