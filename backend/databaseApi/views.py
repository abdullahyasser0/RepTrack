from django.shortcuts import render , redirect
from django.urls import reverse
from supabase import create_client, Client
from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

url: str = "https://sodghnhticinsggmbber.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvZGdobmh0aWNpbnNnZ21iYmVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIyODY5MzMsImV4cCI6MjA0Nzg2MjkzM30.dCfS98X9PFoZpBohhf0UdgSvvcwByOlAPki7-BPlExg"
supabase: Client = create_client(url, key)

#for admin
def get_Memberships():
    return supabase.table("memberships").select("*").execute()

#for admin
def get_Profiles():
    return supabase.table("profiles").select("*").execute()

def get_Users():
    return supabase.table("users").select("*").execute()

def signup(request):
    print('I AM IN THE SIGN UPUPUPUP')
    print(json.loads(request.body))
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            name = data.get('username')
            email = data.get('email')
            phone_number = data.get('phoneNumber')
            account_type = data.get('type')
            password = data.get('password')

            # Call the function to insert data into the database
            user_data = {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'account_type': account_type,
                'password': make_password(password)
            }
            print('User data: ', user_data)
            
            # Assuming you're using Supabase or another database for data insertion
            supabase.table('users').insert(user_data).execute()

            # Return success message as a JSON response
            return JsonResponse({'message': 'User registered successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # If method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        response = supabase.table('users').select('*').eq('email', email).execute()

        if response.data:
            user = response.data[0]
            stored_password = user['password']

            if check_password(password, stored_password):
                request.session['user_id'] = user['user_id'] 
                print('I LOGGEDDD IINNNNNNNNNN')
                return render(request, "profile/information.html")
            else:
                return render(request, '', {'error': 'Invalid credentials'})
        else:
            return render(request, '', {'error': 'Invalid credentials'})

    return render(request, '')
    


def get_user(userid):
    response = supabase.table("countries").select("id, name, cities(name)").\
    join("cities", "countries.id", "cities.country_id").execute()

@login_required
def profile_view(request):
    print('I AM IN PROOFIFLEE  VIEW')
    user_id = request.session.get('user_id')
    # if user_id:
    return render(request, 'profile/information.html')  
    # else:
    #     return redirect('Login')

def logout_view(request):
    logout(request)
    return redirect('login')