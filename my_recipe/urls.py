from django.urls import re_path
from . import views


app_name = 'my_recipe'

urlpatterns = [
    re_path(r'^$', views.recipe_list, name='recipe_list'),
    re_path(r'^add/$', views.recipe_add, name='recipe_add'),
    re_path(r'^(?P<pk>\d+)/$', views.recipe_detail, name='recipe_detail'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.recipe_edit, name='recipe_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.recipe_delete, name='recipe_delete'),
    re_path(r'^my-archive/$', views.my_recipe_archive, name='my_recipe_archive'),
]