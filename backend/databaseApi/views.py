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

logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.DatabaseCreation import DataBase
load_dotenv()




DB = DataBase()




def logout_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('profiles')  
        return view_func(request, *args, **kwargs)
    return wrapper

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

            user_data = {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'account_type': account_type,
                'password': make_password(password)
            }
            
            DB.insert_user(user_data)
            return JsonResponse({'message': 'User registered successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@logout_required
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            response = DB.get_user_byEmail(email)
            if response.data:
                user_data = response.data[0]
                stored_password = user_data['password']

                if check_password(password, stored_password):
                    request.session['user_id'] = user_data['user_id']
                    print('User ID inside login function: ', user_data['user_id'])
                    # Create or retrieve the Django user object
                    user, created = User.objects.get_or_create(username=user_data['email'])
                    if created:
                        user.set_unusable_password()
                        user.save()

                    # Specify the backend explicitly
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    
                    # Log the user in
                    auth_login(request, user)
                    
                    return JsonResponse({'success': True, 'redirect_url': reverse('profiles')})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({'success': False, 'error': 'An error occurred'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    


@login_required
def profile_view(request):
    print(request.session.items())
    user_id = request.session.get('user_id')
    if user_id:
        print('User ID: ', user_id)
        return render(request, 'profile/information.html')  
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

def addPost(request):
    id = request.session.get('user_id')
    name = DB.get_userName(id)
    data = json.loads(request.body)
    description = data.get("description")
    photoUrl = data.get("photoURL")
    # name = data.get("posterName")

    update_response = DB.add_post(description,photoUrl,name )
    if update_response:
        return JsonResponse({'success': True })
    else:
        return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)
            
def addComment(request):
    id = request.session.get('user_id')
    name = supabase.table('users').select('name').eq('user_id',id).execute().data
    print(name[0]["name"],"jj")
    data = json.loads(request.body)
    description = data.get("comment")
    postID = data.get("postID")
    print(postID,"efhghghh")
    # name = data.get("posterName")
    update_response = supabase.table('comments').insert({'comment': description,"commentorName":name[0]["name"],"post_id":postID}).execute()
    if update_response:
                    
                    return JsonResponse({'success': True })
    else:
                    return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)
            

def change_Password(request):
    id = request.session.get('user_id')  
    response = DB.get_user(id)
    
    
    if request.method == 'POST':
        data = json.loads(request.body)
        old = data.get('password')
        new = data.get('new_password')
        

        
        if response.data:
            user = response.data[0]
            stored_password = user['password']

            
            if check_password(old, stored_password):
                hashed_new_password = make_password(new)
                update_response = DB.update_password(hashed_new_password,id)

                if update_response:
                    return JsonResponse({'success': True })
                else:
                    return JsonResponse({'success': False, 'error': 'cant update password'}, status=500)
            else:
                return JsonResponse({'success': False, 'error': 'Old password isnt correct'}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=500)

def change_data(request):
    id = request.session.get('user_id')
    data = json.loads(request.body)
    
    # Fetch the user data from the database
    response = DB.get_user(id)
    
    user_data = response.data[0] if response.data else None

    if request.method == 'POST':
        if user_data:  # Ensure the user data exists
            # Get the new values or retain the old ones if the new values are empty
            userName = data.get('username') if data.get('username') else user_data["name"]
            contactInfo = data.get('contactinfo') if data.get('contactinfo') else user_data["phone_number"]
            email = data.get('email') if data.get('email') else user_data["email"]
            
            # Perform the update operation
            update_response = DB.update_userData(userName,contactInfo,email)
            
            # Check the status of the update operation
            if update_response:
                return JsonResponse({'success': True })
            else:
                return JsonResponse({'success': False, 'error': 'Failed to update user data.'}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)


        

@login_required 
def logout_view(request):
    request.session.flush()
    print("User logged out")
    return redirect('login')



def verify_token(request):
    print("im hereeee babay")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")
            if not token:
                print("Token is missing!")
                return JsonResponse({"error": "Token is required."}, status=400)

            SUPABASE_SECRET = "5z/hwxiHipa12UaymEWVVl/B849CCczv6tx92oazDotlUVZhFVoS7SyY2ER7RKyXKFYPJSIRxvGBFnT2aj6Zjg=="

            # Debugging: Decode token without verification
            unverified_token = jwt.decode(token, options={"verify_signature": False})
            print("Decoded Token Payload (Unverified):", unverified_token)

            # Initialize email from the token payload
            email = unverified_token.get("email")
            if not email:
                print("Email is missing in token!")
                return JsonResponse({"error": "Email not found in token."}, status=400)

            # Query the Supabase table
            response = DB.get_user_byEmail(email)
            if not response.data:
                name = unverified_token.get("user_metadata", {}).get("full_name", "Unknown")
                phone_number = unverified_token.get("phone", "")

                # Prepare user data
                user_data = {
                    'name': name,
                    'email': email,
                    'phone_number': phone_number,
                    'account_type': 'trainee',
                    'password': make_password(email)  # Hash the email as a temporary password
                }

                # Insert new user into Supabase
                DB.insert_user(user_data)
                response = DB.get_user_byEmail(email)

            # Store user ID in session
            request.session['user_id'] = response.data[0]['user_id']

            # Create or retrieve the Django user
            user, created = User.objects.get_or_create(username=email)
            if created:
                user.set_unusable_password()
                user.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Log in the user
            auth_login(request, user)

            return JsonResponse({'success': True, 'redirect_url': reverse('profiles')})

        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return JsonResponse({"error": "Token has expired."}, status=401)
        except jwt.InvalidTokenError as e:
            print("Invalid token:", str(e))
            return JsonResponse({"error": "Invalid token."}, status=401)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)





def generate_otp():
    
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email: str, otp: str):
    sender_name = 'RepTrackAdmin'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587

    msg = EmailMessage()
    msg['From'] = f"{sender_name} <{DB.get_smtp_email()}>"
    msg['To'] = email
    msg['Subject'] = "Your OTP Code"
    msg.set_content(f"Hello,\n\nYour Reset Password OTP code is: {otp}\n\nThank you!")

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(DB.get_smtp_email(), DB.get_smtp_password())
            server.send_message(msg)
        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Failed to send OTP to {email}: {e}")
        raise


# Fetch user data, generate OTP, and save to the database
def forget_password(email):
    # Fetch user data from the Supabase table based on the email
    response = DB.get_user_byEmail(email)
    DB.clean__user_otps(email)
    

    if not response.data:
        return {"status": "error", "message": "No user found"}  # No user found
    else:
        # Generate OTP
        
        otp = generate_otp()
        # Calculate expiration time (e.g., 15 minutes from now)
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        # Save OTP to password_resets table
        DB.insert_otp(email,otp,expires_at)
        # Send OTP via email
        send_otp(email, otp)
        return {"status": "success", "message": "OTP generated and saved successfully"}

@csrf_exempt
def forget_password_view(request):
    """
    Handle password reset requests by generating and sending an OTP to the user's email.
    """
    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
        except json.JSONDecodeError:
            print("Invalid JSON received in forget_password_view")
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

        # Validate email presence
        if not email:
            print("Email not provided in forget_password_view")
            return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            print(f"Invalid email format received: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid email format'}, status=400)

        # Call forget_password function
        result = forget_password(email)

        if result['status'] == 'error':
            # To prevent email enumeration, return a generic success message
            print(f"a user tried to reset a password but he is not in the database: {email}")
            return JsonResponse({'erorr': False, 'message': 'Password reset requested for non-existent email: {email}'}, status=400)

        # OTP successfully generated and sent
        return JsonResponse({
            'success': True,
            'message': result['message']
        }, status=200)

    except Exception as e:
        print(f"Unexpected error in forget_password_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

@csrf_exempt
def verify_otp_view(request):
    """
    Verify the OTP entered by the user.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')

        # Validate inputs
        if not email or not otp:
            logger.warning("Email or OTP not provided in verify_otp_view")
            return JsonResponse({'success': False, 'error': 'Email and OTP are required.'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            logger.warning(f"Invalid email format received: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid email format.'}, status=400)

        # Fetch OTP record from password_resets table
        response = DB.get_otp(email,otp )

        if not response.data:
            logger.warning(f"Invalid OTP for email: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP.'}, status=400)

        otp_record = response.data[0]
        expires_at_str = otp_record.get('expires_at')
        if not expires_at_str:
            logger.warning(f"Expiration time missing for OTP: {otp} and email: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP record.'}, status=400)

        expires_at = datetime.fromisoformat(expires_at_str).replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if current_time > expires_at:
            logger.warning(f"OTP expired for email: {email}")
            return JsonResponse({'success': False, 'error': 'OTP has expired.'}, status=400)

        # Optionally, delete or invalidate the OTP after verification to ensure single use
        
        logger.info(f"OTP verified successfully for email: {email}")

        return JsonResponse({'success': True, 'message': 'OTP verified successfully.'}, status=200)

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in verify_otp_view")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in verify_otp_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

@csrf_exempt
def reset_password_view(request):
    """
    Handle password reset by updating the user's password using the OTP.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
    
    try:
        data = json.loads(request.body)
        logger.info(f"Received data in reset_password_view: {data}")  # Log received data
        
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Validate inputs
        if not all([email, otp, new_password, confirm_password]):
            print ("Missing fields in reset_password_view is " + str(email) + str(otp) + str(new_password) + str(confirm_password))
            logger.warning("Missing fields in reset_password_view")
            return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            logger.warning(f"Invalid email format received: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid email format.'}, status=400)

        # Password strength validation
        if len(new_password) < 8:
            return JsonResponse({'success': False, 'error': 'Password must be at least 8 characters long.'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'}, status=400)

        # Fetch the password_resets record using email and otp
        response = DB.get_otp(email,otp)
        if not response.data:
            logger.warning(f"Invalid OTP or email for reset_password_view: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP or email.'}, status=400)

        otp_record = response.data[0]
        expires_at_str = otp_record.get('expires_at')
        if not expires_at_str:
            logger.warning(f"Expiration time missing for OTP: {otp} and email: {email}")
            return JsonResponse({'success': False, 'error': 'Invalid OTP record.'}, status=400)

        expires_at = datetime.fromisoformat(expires_at_str).replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if current_time > expires_at:
            logger.warning(f"OTP expired for email: {email}")
            return JsonResponse({'success': False, 'error': 'OTP has expired.'}, status=400)

        # Hash the new password
        hashed_password = make_password(new_password)

        # Update the user's password in the users table
        DB.updated_restedPassword(hashed_password,current_time,email)

        DB.clean__user_otps(email)
        return JsonResponse({'success': True, 'message': 'Password has been reset successfully.'}, status=200)

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in reset_password_view")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in reset_password_view: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

