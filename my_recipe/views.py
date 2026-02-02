import google.generativeai as genai
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe
from django.conf import settings
from my_django.models import Ingredient

# 1. 공통 매칭 로직 함수 (코드 중복 방지)
def get_recipes_with_match(request, recipes):
    # 내 냉장고 재료 가져오기
    my_ingredients = Ingredient.objects.filter(user=request.user).select_related('master_ingredient')
    my_names = [ing.master_ingredient.name for ing in my_ingredients]

    recipe_data = []
    for recipe in recipes:
        # 이 레시피에 들어가는 재료 이름 리스트
        recipe_ingredient_names = [ing.name for ing in recipe.ingredients.all()]
        
        # 내 냉장고 재료와 겹치는 것들 추출 (교집합)
        matched_in_recipe = [name for name in my_names if name in recipe_ingredient_names]
        
        recipe_data.append({
            'obj': recipe,
            'matched_list': matched_in_recipe,
            'matched_count': len(matched_in_recipe)
        })
    return recipe_data, my_names

# 2. 공식/추천 레시피 목록
@login_required
def recipe_list(request):
    search_query = request.GET.get('q', '')
    ai_recommendation = ""
    
    # 공식 레시피 필터링 (관리자가 썼거나, 작성자가 없는 시스템 레시피)
    recipes = Recipe.objects.filter(
        Q(user__isnull=True) | Q(user__is_superuser=True)
    ).prefetch_related('ingredients')

    # 검색어가 있으면 필터링
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) | Q(ingredients__name__icontains=search_query)
        ).distinct()

    # 매칭 데이터 계산 (공통 함수 사용)
    recipe_data, my_names = get_recipes_with_match(request, recipes)

    # 냉장고 매칭순 정렬 버튼 클릭 시
    if request.GET.get('fridge_recommend') == 'true':
        recipe_data.sort(key=lambda x: x['matched_count'], reverse=True)

    # AI 추천 로직
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

# 3. 레시피 등록 (여기가 제일 중요했습니다!)
@login_required
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user 
            recipe.save()
            
            # [핵심] ManyToManyField(재료)를 저장하기 위해 반드시 필요합니다.
            form.save_m2m() 
            
            return redirect('my_recipe:my_recipe_archive')
    else:
        form = RecipeForm()
    return render(request, 'my_recipe/recipe_add.html', {'form': form})

# 4. 나만의 레시피 목록 (이제 여기도 매칭 로직 적용됨)
@login_required
def my_recipe_archive(request):
    # 내 레시피 가져오기
    my_recipes = Recipe.objects.filter(user=request.user).prefetch_related('ingredients').order_by('-id')
    
    # [수정] 나만의 레시피 탭에서도 매칭 로직을 적용!
    recipe_data, _ = get_recipes_with_match(request, my_recipes)

    return render(request, 'my_recipe/recipe_list.html', {
        'recipes_with_match': recipe_data,
        'is_archive': True,
    })

# 5. 레시피 상세
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'my_recipe/recipe_detail.html', {'recipe': recipe})

# 6. 레시피 수정
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save() # instance가 있는 폼 저장은 m2m도 자동으로 처리됨
            return redirect('my_recipe:recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'my_recipe/recipe_edit.html', {'form': form, 'recipe': recipe})

# 7. 레시피 삭제
@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    recipe.delete()
    return redirect('my_recipe:my_recipe_archive')