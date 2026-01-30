from django import forms
from .models import Recipe
from my_django.models import MasterIngredient
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'cooking_step', 'difficulty', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '레시피 제목을 입력하세요'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'cooking_step': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ingredients_by_category = {}
        ingredients = MasterIngredient.objects.all().order_by('category', 'name')
        
        for ing in ingredients:
            cat = ing.category if hasattr(ing, 'category') else '기타'
            if cat not in self.ingredients_by_category:
                self.ingredients_by_category[cat] = []
            self.ingredients_by_category[cat].append(ing)