from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ('채소', '채소'),
        ('양념', '양념'),
        ('해산물', '해산물'),
        ('육류', '육류'),
        ('가공식품', '가공식품'),
        ('조미료', '조미료'),
        ('과일', '과일')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='채소')
    quantity = models.IntegerField(default=1)
    expiry_date = models.DateField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_d_day(self):
        if self.expiry_date:
            today = date.today()
            diff = (self.expiry_date - today).days
            if diff == 0: return "D-Day"
            elif diff > 0: return f"D-{diff}"
            else: return "만료"
        return "기한미설정"
    
    def is_expiring_today(self):
        """유통기한이 오늘이거나 지났는지 확인하는 메서드"""
        if self.expiry_date:
            today = date.today()
            diff = (self.expiry_date - today).days
            return diff <= 0 
        return False
