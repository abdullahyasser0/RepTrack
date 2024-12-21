from django.urls import path,include
from . import views
from databaseApi.views import change_data,profile_view
from users.views import admins,coaches,dashboard,Payment,salesReport
from authentication.views import signup,change_Password,verify_token,signup,login, loginForm,logout_view,form_view
from feed.views import addPost,addComment
from Gym.views import Equip
urlpatterns = [
                path('login/', loginForm, name='login'),
                path('logout/', logout_view, name='logout'),
                path('form/', form_view),
                path('signup/',signup),
                path('signupform/',signup, name = 'signupform'),
                path('loginform/',login, name = 'loginform'),
                # path('users/',get_Users),
                # path('admin/',get_Profiles),
                # path('coaches/',get_Coaches),
                path('profilesData/',admins,name='profiles'),
                path('changeDataForm/',change_data, name = 'changeDataForm'),
                path('changePasswordForm/',change_Password, name = 'changePasswordForm'),
                
                path('verify-token/', verify_token, name='verify_token'),
                path('Dashoard/',views.user_dashboard, name = 'Dashboard'),
                path('Equip/',Equip, name = 'Equip'),
                path('payment/',Payment, name = 'payment'),
                path('addPost/',addPost, name = 'addPost'),
                path('addComment/',addComment, name = 'addComment'),
                path('salesReport/',salesReport, name = 'salesReport'),
                path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
                path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
                path('sales-report/', views.sales_report, name='sales_report'),

                ]
