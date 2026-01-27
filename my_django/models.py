from django.db import models
from django.contrib.auth.models import User
from datetime import date

class MasterIngredient(models.Model):
    name = models.CharField(max_length=15, unique=True)
    category = models.CharField(max_length=15, choices=[
        ('채소', '채소'),('양념', '양념'),('해산물', '해산물'),('육류', '육류'),

    ])

    def __str__(self):
        return f'[{self.category}] {self.name}'
    
class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_ingredients')
    master_ingredient = models.ForeignKey(MasterIngredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    expiry_date = models.DateField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.user.username}] {self.master_ingredient.name}"
    
    def get_d_day(self):
        if self.expiry_date:
            today = date.today()
            diff = (self.expiry_date - today).days
            if diff == 0: return "D-Day"
            elif diff > 0: return f"D-{diff}"
            else: return "만료"
        return "기한미설정"