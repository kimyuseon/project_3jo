from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model): # 유저 프로필 모델
    user = models.OneToOneField(User, on_delete=models.CASCADE) #1ㄷ1 관계
    nickname = models.CharField("닉네임", max_length=15, blank=True)
    img_profile = models.ImageField("프로필 이미지", upload_to="media/user", blank=True) # 프로필 이미지 , 필수입력 아님
    description = models.TextField("소개글", blank=True)

    def __str__(self):
        return self.user.username