import google.generativeai as genai
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import RecipeForm
from .models import Recipe

#목록
def recipe_list(request):
    search_query = request.GET.get('q', '')
    ai_recommendation = ""
    
    if search_query:
        recipes = Recipe.objects.filter(Q(title__icontains=search_query) | Q(ingredients__icontains=search_query)).order_by('-id')
        
        if request.GET.get('recommend') == 'true' or '추천' in request.GET:
            #내 구글제미나이 API키
            genai.configure(api_key="AIzaSyCuQtKtBYAfYSHtOBsWps3bTSggP8-tJSY")            
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            #내가 입력한문장대로 정해주니까 이거 수정하면 됨.
            prompt = f"{search_query} 관련된 레시피를 제목, 재료, 순서로 짧고 간결하게 한국어로 추천해줘"
            
            try:
                response = model.generate_content(prompt)
                ai_recommendation = response.text
            except Exception as e:
                ai_recommendation = "죄송합니다. AI 추천 기능을 현재 사용할 수 없습니다." #f"에러발생 원인: {str(e)}"
    else:
        recipes = Recipe.objects.all().order_by('-id')

    return render(request, 'my_recipe/recipe_list.html', {
        'recipes': recipes, 
        'search_query': search_query,
        'ai_recommendation': ai_recommendation
    })

# 등록
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_recipe:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'my_recipe/recipe_add.html', {'form': form})

#상세페이지
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return redirect('my_recipe:recipe_list')
    return render(request, 'my_recipe/recipe_detail.html', {'recipe': recipe})