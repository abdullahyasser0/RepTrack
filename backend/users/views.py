import sys
import os
from authentication.views import logout_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
from faker import Faker
from .forms import SimpleForm,SignupForm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.DatabaseCreation import DataBase
#Create your views here.
fake = Faker()

DB = DataBase()

# users,admins,coaches,dashboard, userstats,Equip,admins,coaches,dashboard,Payment,salesReport

#stas
def dashboard(request):
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    return render(request, "../templates/Dashboard/Dashboard.html", {'user':user})


#user
def userstats(request):
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    return render(request, "../templates/Dashboard/UserStatistics.html", {'user':user})


#global to gyms
def Payment(request):
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    
    return render(request, "../templates/Admin/Payment.html",{'id':user_id,'user':user})


#global to gyms
def salesReport(request):
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    payments = DB.get_payment()
    print(payments)
    return render(request, "../templates/Admin/SalesReport.html",{'users':users,'id':user_id,'user':user,'payments':payments}) #waiting for report to be passed here 



#users 
@login_required 
def users(request):
    users = DB.get_Users()
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    return render(request, '../templates/profile/ActiveMembers.html', {'users': users, 'id':user_id, 'user':user})

#Coaches
@login_required 
def coaches(request):
    users = DB.get_Coaches()
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    return render(request, '../templates/profile/ActiveCoaches.html', {'users': users , 'id':user_id, 'user':user})

#Admins
@login_required 
def admins(request):
    user_id = request.session.get('user_id')
    users = DB.get_user(user_id)
    return render(request, '../templates/profile/information.html', {'users': users,'id':user_id})




@login_required
def user_dashboard(request):
    # Sample data for user charts
    data = {
        'weekly_activity': [5, 10, 15, 20, 25, 30, 35],
        'task_status': {'Completed': 75, 'Pending': 25},
        'monthly_performance': [50, 60, 70, 80, 90],
    }
    return render(request, 'users/user_dashboard.html', {'data': data})


@login_required
def admin_dashboard(request):
    # Sample data for admin charts
    data = {
        'weekly_users': [10, 20, 15, 25, 30, 35, 40],
        'role_distribution': {'Manager': 10, 'Developer': 15, 'Team Lead': 5},
        'monthly_revenue': [1000, 2000, 3000, 4000, 5000],
    }
    return render(request, 'users/admin_dashboard.html', {'data': data})







@login_required
def sales_report(request):
    # payments = DB.get_payment()
    
    # Prepare the payment data (you can filter or order it if necessary)
    # payment_data = []
    # for payment in payments:
    #     payment_data.append({
    #         'payment_id': payment['payment_id'],
    #         'user_id': payment['user_id'],
    #         'phone_number': payment['phone_number'],
    #         'payment_type': payment['payment_type'],
    #         'created_at': payment['created_at']
    #     })



    # Render the report on the sales_report.html template
    # return render(request, 'sales/sales_report.html', {'payment_data': payment_data})


    # Generate random payment data (simulating data from the database)
    payment_data = []
    for _ in range(20):  # Generate 20 random records
        payment_data.append({
            'payment_id': random.randint(1000, 9999),  # Random payment ID
            'user_id': random.randint(1, 100),  # Random user ID
            'phone_number': fake.phone_number(),  # Random phone number
            'payment_type': random.choice(['Credit Card', 'PayPal', 'Bank Transfer']),  # Random payment type
            'created_at': fake.date_this_year(),  # Random date within this year
        })
    # Render the report on the sales_report.html template
    return render(request, 'users/sales_report.html', {'payment_data': payment_data})  