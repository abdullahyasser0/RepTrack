from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import SimpleForm,SignupForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User 
from databaseApi.views import get_Users,get_user1,get_Coaches,get_Posts
from databaseApi.views import logout_required


# Create your views here.


def home(request):
    return render(request, "test.html")

def dashboard(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, "../templates/Dashboard/Dashboard.html", {'user':user})

def userstats(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, "../templates/Dashboard/UserStatistics.html", {'user':user})
@login_required 
def logout_view(request):
    request.session.flush()
    return redirect('login')

def Equip(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, "../templates/Admin/AddEquipment.html",{'users':users,'id':user_id,'user':user})

def Payment(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, "../templates/Admin/Payment.html",{'users':users,'id':user_id,'user':user})
def salesReport(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, "../templates/Admin/SalesReport.html",{'users':users,'id':user_id,'user':user}) #waiting for report to be passed here 

def posts(request):
    posts = get_Posts()
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    print(user)
    #print(posts['user_id'])
    return render(request, "../templates/Community/posts.html",{'users':users,'id':user_id,'user':user,'posts':posts}) #waiting for report to be passed here 


@login_required 
def users(request):
    users = get_Users()
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, '../templates/profile/ActiveMembers.html', {'users': users, 'id':user_id, 'user':user})
@login_required 
def coaches(request):
    users = get_Coaches()    
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    return render(request, '../templates/profile/ActiveCoaches.html', {'users': users , 'id':user_id, 'user':user})
@login_required 
def admins(request):
    
    user_id = request.session.get('user_id')
    users = get_user1(user_id)
    return render(request, '../templates/profile/information.html', {'users': users,'id':user_id})

@login_required
def protected_page(request):
    return render(request, "protected_page.html")

@logout_required
def login(request):
    return render(request,"login/Login.html")

def form_view(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            return HttpResponse(f"Thank you, {name}! Your email is {email}.")
    else:
        form = SimpleForm()
    
    return render(request, 'myform/form.html', {'form': form})
@logout_required
def signup(request):
    return render(request, "signup/signup.html")
@logout_required
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Handle form submission
        if form.is_valid():
            # Retrieve form data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            # For now, let's just return a success message
            return HttpResponse(f"Signup successful! Username: {username}, Email: {email}, Phone: {phone}")
    else:
        form = SignupForm()  # Create a new form instance for GET request

    return render(request, 'signup/signup.html', {'form': form})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from supabase import create_client
import random
from faker import Faker
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Initialize Supabase client
supabase_url = "https://sodghnhticinsggmbber.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvZGdobmh0aWNpbnNnZ21iYmVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyODY5MzMsImV4cCI6MjA0Nzg2MjkzM30.dCfS98X9PFoZpBohhf0UdgSvvcwByOlAPki7-BPlExg"
supabase = create_client(supabase_url, supabase_key)

fake = Faker()


@login_required
def sales_report(request):
    # Fetch payment data from Supabase
#    payments = supabase.table('payment').select('*').execute().data
    
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