from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField() # 요리설명
    ingredients = models.TextField(blank=True) #재료!(ai사용할거)
    cooking_step = models.TextField() # 조리순서
    image = models.ImageField(upload_to="my_recipe", blank=True)
    difficulty = models.CharField(max_length=20, choices=[('쉬움','쉬움'), ('보통','보통'),('어려움','어려움')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title