import os
import jwt
import sys
import json
import string
import random
import smtplib
import logging
from functools import wraps
from dotenv import load_dotenv
from django.urls import reverse
from django.http import JsonResponse
from email.message import EmailMessage
from supabase import create_client, Client
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime, timedelta,timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as auth_login, authenticate, logout
from Database.DatabaseCreation import DataBase
from .services.OTPService import OTPService
from .services.UserService import UserService
from .forms import SimpleForm,SignupForm
from django.http import HttpResponse

# UserService = UserService()
OTP = OTPService()

logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join( '..')))

DB = DataBase()

def logout_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('profiles')  
        return view_func(request, *args, **kwargs)
    return wrapper
# 

def form_view(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            return HttpResponse(f"Thank you, {name}! Your email is {email}.")
    else:
        form = SimpleForm()


# done
@logout_required
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phoneNumber')
            account_type = data.get('type')
            password = data.get('password')

            responce = UserService.create_user(name,email,phone_number,account_type,password)

            if responce == 200 :
                return JsonResponse({'message': 'User registered successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@logout_required
def loginForm(request):
    return render(request,"login/Login.html")
# done
@logout_required
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            User = UserService.authenticate_user(email, password,request)

            if User == 200 :
                return JsonResponse({'success': True, 'redirect_url': reverse('profiles')})
            elif User == 401 :
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)  
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)
    print("YASSSATER")
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    


#done
def change_Password(request):
    id = request.session.get('user_id')  
    
    if request.method == 'POST':
        data = json.loads(request.body)
        old = data.get('password')
        new = data.get('new_password')
    
        response = UserService.changePassowrd(id,new,old)

        if response == 200: 
            return JsonResponse({'success': True })
        elif response == 401:
            return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)
        elif response == 402 :
            return JsonResponse({'success': False, 'error': 'Old password isnt correct'}, status=500)
        else :
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=500)
        



@login_required 
def logout_view(request):
    request.session.flush()
    return redirect('login')


# auth
def verify_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")
            if not token:
                return JsonResponse({"error": "Token is required."}, status=400)
            unverified_token = jwt.decode(token, options={"verify_signature": False})

            email = unverified_token.get("email")
            if not email:
                return JsonResponse({"error": "Email not found in token."}, status=400)

            response = DB.get_user_byEmail(email)
            if not response.data:
                name = unverified_token.get("user_metadata", {}).get("full_name", "Unknown")
                phone_number = unverified_token.get("phone", "")


                UserService.create_user(name,email,phone_number,'trainee',email)

          
            request.session['user_id'] = response.data[0]['user_id']  # Store user ID in session

            
            user, created = User.objects.get_or_create(username=email)# Createthe Django user
            if created:
                user.set_unusable_password()
                user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth_login(request, user)            # Log in the user


            return JsonResponse({'success': True, 'redirect_url': reverse('profiles')})

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired."}, status=401)
        
        except jwt.InvalidTokenError as e:
            return JsonResponse({"error": "Invalid token."}, status=401)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)




# auth
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))



def forget_password(email):
    response = DB.get_user_byEmail(email) # Fetch user data from the Supabase table based on the email
    DB.clean__user_otps(email)

    if not response.data:
        return {"status": "error", "message": "No user found"}  # No user found
    else:
        otp = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        DB.insert_otp(email,otp,expires_at)
        OTP.send_otp(email, otp)
        return {"status": "success", "message": "OTP generated and saved successfully"}
    
# auth
@csrf_exempt
def forget_password_view(request):
    try:
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)  # print("Invalid JSON received in forget_password_view")
        if not email:
            print("Email not provided in forget_password_view")
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400) # Validate email presence

        try:
            validate_email(email) # Validate email format
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Invalid email format'}, status=400)

        
        result = forget_password(email) # Call forget_password function

        if result['status'] == 'error':
            # print(f"a user tried to reset a password but he is not in the database: {email}")
            return JsonResponse({'erorr': False, 'message': 'Password reset requested for non-existent email: {email}'}, status=400) # To prevent email enumeration, return a generic success message
            

        return JsonResponse({'success': True,'message': result['message']}, status=200)        # OTP successfully generated and sent


    except Exception as e:
        # print(f"Unexpected error in forget_password_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

# done
@csrf_exempt
def verify_otp_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')

        if not email or not otp:
            logger.warning("Email or OTP not provided in verify_otp_view")
            return JsonResponse({'success': False, 'error': 'Email and OTP are required.'}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            logger.warning(f"Invalid email format received: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid email format.'}, status=400)
        
        is_valid_otp = OTPService.verify_otp(email, otp)

        if not is_valid_otp:
            logger.warning(f"Invalid or expired OTP for email: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid or expired OTP.'}, status=400)

        logger.info(f"OTP verified successfully for email: {email}")

        return JsonResponse({'success': True, 'message': 'OTP verified successfully.'}, status=200)

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in verify_otp_view")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in verify_otp_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)


# auth done
@csrf_exempt
def reset_password_view(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
    
    try:
        data = json.loads(request.body)
        logger.info(f"Received data in reset_password_view: {data}")  # Log received data
        
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not all([email, otp, new_password, confirm_password]):
            logger.warning("Missing fields in reset_password_view")
            return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            logger.warning(f"Invalid email format received: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid email format.'}, status=400)


        if len(new_password) < 8:
            return JsonResponse({'success': False, 'error': 'Password must be at least 8 characters long.'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'}, status=400)



        Resetreponce =UserService.resetPassowrd(email,new_password,otp)

        if Resetreponce == 403 :
            logger.warning(f"Invalid OTP or email for reset_password_view: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP or email.'}, status=400)

        elif Resetreponce == 405:
            logger.warning(f"Expiration time missing for OTP: {otp} and email: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP record.'}, status=400)

        elif Resetreponce == "expired":
            logger.warning(f"OTP expired for email: {email}")
            return JsonResponse({'success': False, 'error': 'OTP has expired.'}, status=400)
        else :
            return JsonResponse({'success': True, 'message': 'Password has been reset successfully.'}, status=200)

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in reset_password_view")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in reset_password_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)



def logout_view(request):
    logout(request)
    return redirect('login')



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