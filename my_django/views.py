from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Ingredient
# from .forms import IngredientForm 
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import MasterIngredient, Ingredient
from .services import extract_receipt_data_langchain

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

from django.shortcuts import render, redirect
from .models import MasterIngredient, Ingredient

@login_required
def add_ingredient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity', 1)) 
        
        master_item = get_object_or_404(MasterIngredient, name=name)
        
        ingredient, created = Ingredient.objects.get_or_create(
            user=request.user,
            master_ingredient=master_item,
            defaults={
                'quantity': quantity,
                'expiry_date': timezone.now().date() + timedelta(days=7)
            }
        )
        
        if not created:
            ingredient.quantity += quantity
            ingredient.save()
            
        return redirect('my_django:fridge_main')
    return redirect('my_django:fridge_main')

@login_required
def update_expiry(request, pk):
    item = get_object_or_404(Ingredient, pk=pk, user=request.user)
    if request.method == "POST":
        new_expiry = request.POST.get('expiry_date')
        if new_expiry:
            item.expiry_date = new_expiry
            item.save()
            
    return redirect('my_django:fridge_main')

# 5. 재료 삭제 - 로그인 필요
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
                        user=request.user,
                        master_ingredient=master_item,
                        defaults={'quantity': count, 'expiry_date': timezone.now().date() + timedelta(days=7)}
                    )
                    if not created:
                        user_ingredient.quantity += int(count)
                        user_ingredient.save()
            return redirect('my_django:fridge_main')
            
    return render(request, 'index.html')
    #     # 본인의 재료만 삭제 가능
    #     item = get_object_or_404(Ingredient, pk=pk, user=request.user)
    #     item.delete()
    # return redirect('my_django:fridge_main')
