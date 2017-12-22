from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('interface/book_info', views.book_info, name='book_info'),
    path('interface/user_info', views.user_info, name='user_info'),
]
