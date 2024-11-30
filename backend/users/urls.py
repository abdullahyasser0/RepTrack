from django.urls import path,include
from . import views
from databaseApi.views import signup

urlpatterns = [path('login/', views.login, name='login'),
                path("logout/", views.logout_view),
                path("protectedpage/",views.protected_page),
                path("test/",views.home),
                path('form/', views.form_view),
                path('signup/',signup),
                path('authenticate/', views.authenticate_user, name='authenticate_user'),
                path('bdany/',views.badny)
                ]
