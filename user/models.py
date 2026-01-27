# from django.db import models
# from django.contrib.auth.models import User


# class Profile(models.Model):
#     user = models.OneToOneField() #user모델과 1대1로 연결(유저가 삭제되면 프로필도 삭제)
#     image = models.ImageField(upload_to="user", blank=True, null=True)
#     bio = models.TextField(blank=True)

#     def __str__(self): 
#         return f"{self.user.username}입니다."