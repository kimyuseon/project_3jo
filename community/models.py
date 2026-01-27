from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) #제목
    content = models.TextField() #내용 저장될 곳
    thumbnail = models.ImageField(upload_to="community", blank=True, null=True) #이미지 저장될 곳(여기서 pip install Pillow)
    created_at = models.DateTimeField(auto_now_add=True) #글작성시간 자동 저장

    def __str__(self): 
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #댓글 작성 시간

    def __str__(self):
        return f"{self.post.title}의 댓글 ID {self.id}"