# from django.contrib import admin
# from .models import Ingredient, Recipe, RecipeIngredient, RefrigeratorIngredient

# #재료관리하기(사용자이름/재료)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#     search_fields = ("name",)

# #레시피 관리하기
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "difficulty", "prep_time", "created_by")
#     search_fields = ("title", "instructions") # 제목,조리방법으로 검색 가능
#     list_filter = ("difficulty",) # 난이도별로모아보기 필터

# #레시피-재료 중간 테이블 관리하기
# class RecipeIngredientAdmin(admin.ModelAdmin):
#     list_display = ("id", "recipe", "ingredient", "quantity", "is_optional")
#     search_fields = ("recipe__title", "ingredient__name") 
# #사용자 냉장고 재료 관리하기
# class RefrigeratorIngredientAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "ingredient", "quantity", "expiry_date")
#     list_filter = ("expiry_date", "user") #유통기한, 유저별 필터

# admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
# admin.site.register(RefrigeratorIngredient, RefrigeratorIngredientAdmin)