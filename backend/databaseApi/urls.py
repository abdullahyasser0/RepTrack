from django.contrib import admin
from django.urls import path, include
from users.views import signup_view , login
from databaseApi.views import profile_view
import views

urlpatterns = [
    path('profile/', views.profile_views, name='profile'),
    path('signup/login/', login, name='login'),  # Login URL
]