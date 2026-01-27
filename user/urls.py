from django.urls import re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^SignUp/$', views.SignUp_view, name='SignUp'),
    re_path(r'^login/$', views.login_view, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^index/$', views.main_index, name='index'),
]
