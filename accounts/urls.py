from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('change_password/', views.change_password, name='change_password'),
]
