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
    
    my_recipes = Recipe.objects.filter(user=request.user)
    
    if search_query:
        recipes = my_recipes.filter(Q(title__icontains=search_query) | Q(ingredients__icontains=search_query)).order_by('-id')
        
        if request.GET.get('recommend') == 'true' or '추천' in search_query:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)            
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = (
                    f"사용자가 '{search_query}'와(과) 관련된 요리법을 알고 싶어해. "
                    f"제목, 필요한 재료, 단계별 요리 순서로 나누어서 짧고 간결하게 한국어로 추천해줘.")
                response = model.generate_content(prompt)
                if response and response.text:
                    ai_recommendation = response.text
                
            except Exception as e:
                print(f"오류 원인: {e}")
                ai_recommendation = "AI 추천을 가져오는 중에 문제가 생겼어요. 잠시 후 다시 시도해 주세요!"

    else:
        recipes = my_recipes.order_by('-id')

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
    # 내 글이 아니면 자동으로 404 오류
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    return render(request, 'my_recipe/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_edit(request, pk):
    # 수정 시에도 본인 확인 로직 강화
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
    return redirect('my_recipe:recipe_list')