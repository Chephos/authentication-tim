from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.signup,name='sign_up'),
    path('new-post/', views.create_post,name='create_post'),
    path('<slug:slug>/edit/', views.edit_post, name='edit_post'),

]