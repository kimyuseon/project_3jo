from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['master_ingredient', 'quantity', 'expiry_date']
        # fields = ['name', 'category', 'quantity', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'master_ingredient': '재료 선택',
            'quantity': '수량',
            'expiry_date': '유통기한',
        }