from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include

app_name = 'moss'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^special/',views.special, name='special'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^upload_files/$', views.upload_files, name='upload_files'),
]