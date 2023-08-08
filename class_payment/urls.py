from django.urls import path
from . import views

urlpatterns = [
    path('', views.class_index),
    path('card/', views.class_card, name='gym_card'),
    path('transfer/', views.class_transfer, name='gym_transfer'),
    path('success/', views.class_success, name='gym_success'),
    path('fail/', views.class_fail, name='gym_fail'),
    path('ancel/', views.class_cancel, name='gym_cancel'),
]
