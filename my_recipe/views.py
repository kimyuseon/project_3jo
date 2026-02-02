import google.generativeai as genai
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe
from django.conf import settings
from my_django.models import Ingredient

def get_recipes_with_match(request, recipes):
    my_ingredients = Ingredient.objects.filter(user=request.user).select_related('master_ingredient')
    my_names = [ing.master_ingredient.name for ing in my_ingredients]

    recipe_data = []
    for recipe in recipes:
        recipe_ingredient_names = [ing.name for ing in recipe.ingredients.all()]
        
        matched_in_recipe = [name for name in my_names if name in recipe_ingredient_names]
        
        recipe_data.append({
            'obj': recipe,
            'matched_list': matched_in_recipe,
            'matched_count': len(matched_in_recipe)
        })
    return recipe_data, my_names

@login_required
def recipe_list(request):
    search_query = request.GET.get('q', '')
    ai_recommendation = ""
    
    recipes = Recipe.objects.filter(
        Q(user__isnull=True) | Q(user__is_superuser=True)
    ).prefetch_related('ingredients')

    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) | Q(ingredients__name__icontains=search_query)
        ).distinct()

    recipe_data, my_names = get_recipes_with_match(request, recipes)

    if request.GET.get('fridge_recommend') == 'true':
        recipe_data.sort(key=lambda x: x['matched_count'], reverse=True)

    if request.GET.get('recommend') == 'true' and search_query:
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash') 
            prompt = f"'{search_query}'를 활용한 요리 레시피를 제목, 재료, 요리 순서로 나누어 짧고 간결하게 한국어로 추천해줘. ***같은 기호는 사용하지마"
            response = model.generate_content(prompt)
            ai_recommendation = response.text
        except Exception as e:
            ai_recommendation = f"AI 추천을 가져오는 중 오류가 발생했습니다: {e}"

    return render(request, 'my_recipe/recipe_list.html', {
        'recipes_with_match': recipe_data,
        'search_query': search_query,
        'ai_recommendation': ai_recommendation,
        'my_names': my_names,
        'is_archive': False,
    })

@login_required
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user 
            recipe.save()
            
            form.save_m2m() 
            
            return redirect('my_recipe:my_recipe_archive')
    else:
        form = RecipeForm()
    return render(request, 'my_recipe/recipe_add.html', {'form': form})

@login_required
def my_recipe_archive(request):
    my_recipes = Recipe.objects.filter(user=request.user).prefetch_related('ingredients').order_by('-id')
    
    recipe_data, _ = get_recipes_with_match(request, my_recipes)

    return render(request, 'my_recipe/recipe_list.html', {
        'recipes_with_match': recipe_data,
        'is_archive': True,
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'my_recipe/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('my_recipe:recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'my_recipe/recipe_edit.html', {'form': form, 'recipe': recipe})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    recipe.delete()
    return redirect('my_recipe:my_recipe_archive')