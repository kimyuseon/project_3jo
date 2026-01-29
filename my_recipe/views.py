import google.generativeai as genai
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe
from django.conf import settings


@login_required
def recipe_list(request):
    search_query = request.GET.get('q', '')
    ai_recommendation = ""
    
    if search_query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=search_query) | Q(ingredients__icontains=search_query)
        ).order_by('-id')
        
        if request.GET.get('recommend') == 'true' or '추천' in search_query:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)            
                
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"'{search_query}'와 관련된 요리 레시피를 제목, 재료, 요리 순서로 나누어 짧고 간결하게 한국어로 추천해줘."
                
                response = model.generate_content(prompt)
                ai_recommendation = response.text
                
            except Exception as e:
                ai_recommendation = print(f"AI error: {e}")

    else:
        recipes = Recipe.objects.all().order_by('-id')

    return render(request, 'my_recipe/recipe_list.html', {
        'recipes': recipes, 
        'search_query': search_query,
        'ai_recommendation': ai_recommendation
    })


@login_required
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('my_recipe:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'my_recipe/recipe_add.html', {'form': form})


@login_required
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return redirect('my_recipe:recipe_list')
    return render(request, 'my_recipe/recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.user != request.user:
        return redirect('my_recipe:recipe_detail', pk=pk)

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
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if recipe.user == request.user:
        recipe.delete()
    
    return redirect('my_recipe:recipe_list')

# 익명글 삭제할 때 사용
# def recipe_delete(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
    
#     if request.method == "POST":
#         try:
#             if recipe.user == request.user:
#                 recipe.delete()
#             else:
#                 return redirect('my_recipe:recipe_detail', pk=pk)
#         except:
#             recipe.delete()
            
#         return redirect('my_recipe:recipe_list')
    
#     return redirect('my_recipe:recipe_detail', pk=pk)
