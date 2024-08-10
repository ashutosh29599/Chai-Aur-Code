from django.urls import path

from . import views

urlpatterns = [
    path('<int:user_id>/profile/', views.profile, name='profile'),
    path('<int:user_id>/edit_profile/', views.edit_profile, name='edit_profile'),
] 
