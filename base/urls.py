from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlagView.as_view(), name='plag'),
]