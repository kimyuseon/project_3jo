from django.contrib import admin
from .models import MasterIngredient, Ingredient

@admin.register(MasterIngredient)
class MasterIngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_category', 'quantity', 'expiry_date', 'user')
    list_filter = ('master_ingredient__category', 'expiry_date') 

    def get_name(self, obj):
        return obj.master_ingredient.name
    get_name.short_description = '재료명'

    def get_category(self, obj):
        return obj.master_ingredient.category
    get_category.short_description = '카테고리'