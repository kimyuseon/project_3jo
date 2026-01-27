from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'cooking_step', 'difficulty', 'image']
        labels = {'title': '레시피 제목','description': '설명', 'ingredients': '필요한 재료','cooking_step':'요리순서','difficulty': '난이도 선택','image': '요리사진'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '요리를 검색하세요'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '예: 양파 1개, 감자 2개, 우유 200ml'}),
            'cooking_step': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }