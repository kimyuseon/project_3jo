from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from my_django.models import MasterIngredient 

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        MasterIngredient, 
        related_name='recipes', 
        verbose_name="필요한 재료",
        blank=True
    )
    
    cooking_step = models.TextField()
    image = models.ImageField(upload_to="my_recipe", blank=True)
    difficulty = models.CharField(
        max_length=20, 
        choices=[('쉬움','쉬움'), ('보통','보통'),('어려움','어려움')],
        default='보통'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.title