from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('address/', views.address, name='address'),
    url(r'^logout/$', LogoutView.as_view(),  name='logout'),
]
