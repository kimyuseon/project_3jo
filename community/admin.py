from django.contrib import admin
from .models import Post, Comment

class MyAdminPost(admin.ModelAdmin):
    list_display = ("id","title") #목록에 아이디, 제목
    search_fields = ("title",) #요리제목 기준으로 검색

class MyAdminComment(admin.ModelAdmin):
    list_display = ("id","post","content") 
    search_fields = ("content",) #댓글내용 검색

admin.site.register(Post, MyAdminPost)
admin.site.register(Comment,MyAdminComment)
