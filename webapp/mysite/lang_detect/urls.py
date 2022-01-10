from django.urls.conf import path
from django.urls import re_path
from lang_detect import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^get_lang/$', views.get_lang, name='get_lang'),
]