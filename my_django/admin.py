from django.contrib import admin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'expiry_date', 'added_at')
    list_filter = ('category',)
    search_fields = ('name',)