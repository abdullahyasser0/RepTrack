from django.urls import path,include
from . import views
from databaseApi.views import signup, login
from databaseApi.views import profile_view
from databaseApi.views import signup,get_Users,get_Profiles,change_data,change_Password,get_Coaches
from users.views import signup_view,users,admins,coaches,dashboard

urlpatterns = [path('login/', views.login, name='login'),
                path('logout/', views.logout_view, name='logout'),
                path("protectedpage/",views.protected_page),
                path("test/",views.home),
                path('form/', views.form_view),
                path('signup/',views.signup),
                path('signupform/',signup, name = 'signupform'),
                path('loginform/',login, name = 'loginform'),
                path('users/',get_Users),
                path('admin/',get_Profiles),
                path('coaches/',get_Coaches),
                path('profilesData/',admins,name='profiles'),
                path('changeDataForm/',change_data, name = 'changeDataForm'),
                path('changePasswordForm/',change_Password, name = 'changePasswordForm'),
                path('Dashoard/',dashboard, name = 'Dashboard'),
                ]
