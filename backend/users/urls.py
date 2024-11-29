from django.urls import path,include
from . import views

urlpatterns = [path("login/", views.login),
                path("logout/", views.logout_view),
                path("protectedpage/",views.protected_page),
                path("test/",views.home),
                path('form/', views.form_view),
                path('signup/',views.SignupForm),
                ]
