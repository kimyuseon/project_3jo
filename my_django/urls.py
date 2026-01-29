from django.urls import re_path
from . import views


app_name = 'my_django'


urlpatterns = [
    re_path(r'^$', views.fridge_main, name='fridge_main'),
    re_path(r'^select/$', views.ingredient_select, name='ingredient_select'),
    re_path(r'^update/(?P<pk>\d+)/$', views.update_expiry, name='update_expiry'),
    re_path(r'^delete/(?P<pk>\d+)/$', views.delete_ingredient, name='delete_ingredient'),
    re_path(r'^add/$', views.add_ingredient, name='add_ingredient'), 
    re_path(r'^upload-receipt/$', views.upload_receipt, name='upload_receipt'),
]