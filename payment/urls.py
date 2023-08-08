from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('card/', views.card, name='card'),
    path('transfer/', views.transfer, name='transfer'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('cancel/', views.cancel, name='cancel'),
]
