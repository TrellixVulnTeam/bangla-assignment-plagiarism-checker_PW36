from django.urls import path
from . import views

path('users/', views.UserList.as_view(), name="users"),
path('users/<int:pk>/', views.UserDetail.as_view(), name="single-user"),