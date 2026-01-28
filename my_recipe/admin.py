from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "created_at"]
    search_fields = ["title", "description", "cooking_step"]
    list_filter = ["user", "created_at"]

    ordering = ("-id",)

