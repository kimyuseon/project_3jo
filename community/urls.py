from django.urls import re_path
from . import views

app_name = "community"

urlpatterns = [
    re_path("^$", views.index, name="index"), #주소창에 아무것도 안쳤을 때 홈
    re_path(r'^login/$', views.login_view, name='login'),
    re_path("^posts/$", views.post_list, name="post_list"), #게시글 목록 페이지
    re_path(r"^posts/(?P<post_id>\d+)/$", views.post_detail, name="post_detail"),#상세페이지
    re_path("^posts/add/$", views.post_add, name="post_add"), #게시글 작성
    re_path(r"^posts/(?P<post_id>\d+)/delete/$", views.post_delete, name="post_delete"), #삭제
    re_path(r'^posts/(?P<post_id>\d+)/edit/$', views.post_edit, name='post_edit'), #수정
    re_path(r"^(?P<post_id>\d+)/like/$", views.post_like, name="post_like"),
    re_path(r'^post/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    re_path(r'^post/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/delete/$',views.comment_delete, name='comment_delete'),
]