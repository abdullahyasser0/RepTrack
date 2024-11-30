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


# Create your views here.


def home(request):
    return render(request, "test.html")


def logout_view(request):
    logout(request)
    return redirect("/main")

@login_required
def protected_page(request):
    return render(request, "protected_page.html")


def login(request):
    return render(request,"login.html")

def form_view(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            return HttpResponse(f"Thank you, {name}! Your email is {email}.")
    else:
        form = SimpleForm()
    
    return render(request, 'myform/form.html', {'form': form})



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




import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

SUPABASE_API_URL = 'https://sodghnhticinsggmbber.supabase.co/auth/v1/user'

def authenticate_user(request):
    # Extract JWT token from the Authorization header
    jwt_token = request.headers.get('Authorization')

    if not jwt_token:
        return JsonResponse({'error': 'No JWT token provided'}, status=400)

    try:
        # Verify the JWT token by sending it to Supabase
        response = requests.get(SUPABASE_API_URL, headers={'Authorization': f'Bearer {jwt_token}'})

        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        # Extract user data from the response
        user_data = response.json()
        user_id = user_data.get('id')
        email = user_data.get('email')

        # Check if the user exists in your Django database
        user, created = User.objects.get_or_create(email=email)

        # Optionally, associate additional user info in a profile model
        user_profile, profile_created = UserProfile.objects.get_or_create(user=user)
        user_profile.supabase_user_id = user_id
        user_profile.save()

        # Respond with user data
        return JsonResponse({'message': 'User authenticated successfully', 'user_id': user.id})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error verifying token: {str(e)}'}, status=500)
    


def badny(request):
    return render(request,"test.html")
