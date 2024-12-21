import os
import sys
import json
import logging
from functools import wraps
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Database.DatabaseCreation import DataBase
load_dotenv()

from authentication.services.UserService import UserService

logger = logging.getLogger(__name__)



DB = DataBase()

# change_data,profile_view save_user_days,get_user_schedule,add_workout


@login_required
def profile_view(request):
    print(request.session.items())
    user_id = request.session.get('user_id')
    if user_id:
        print('User ID: ', user_id)
        return render(request, 'profile/information.html')  
    else:
        return redirect('login')

def workoutview(request):
    user_id = request.session.get('user_id')  
    user = DB.get_user(user_id)[0]
    return render(request, "../templates/Admin/AddWorkout.html", {
                'user': user
            })

def admin_add_workout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            workout_name = data.get('workout_name')
            description = data.get('description')
            duration = data.get('duration')
            difficulty_level = data.get('difficulty_level')
            target_muscle_group = data.get('target_muscle_group')

            # Validate required fields
            if not all([workout_name, description, duration, difficulty_level, target_muscle_group]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Insert into system_workout table
            response = DB.admin_add_workout(workout_name, description, duration, difficulty_level, target_muscle_group)

            if response:
                return JsonResponse({'success': 'Workout added successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Failed to add workout.'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


# auth
def change_data(request):
    id = request.session.get('user_id')
    data = json.loads(request.body)
    
    # Fetch the user data from the database
    response = DB.get_user(id)
    
    user_data = response.data[0] if response.data else None

    if request.method == 'POST':
        if user_data:  
            userName = data.get('username') if data.get('username') else user_data["name"]
            contactInfo = data.get('contactinfo') if data.get('contactinfo') else user_data["phone_number"]
            email = data.get('email') if data.get('email') else user_data["email"]
            
            ChangeDatares = UserService.ChangeData(userName,contactInfo,email)

            if ChangeDatares == 200:
                return JsonResponse({'success': True })
            else:
                return JsonResponse({'success': False, 'error': 'Failed to update user data.'}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)




    


# def get_nutritionist():
#     return supabase.table("users").select("*").eq('account_type','nutritionist').execute().data



@login_required
def check_registered_nutritionist(request):
    user_id = request.session.get('user_id')  # Retrieve the logged-in user's ID
    # user = get_user1(user_id)[0]
    user = DB.get_user(user_id)[0]
    # Check if the user is registered with a nutritionist
    registered_nutritionist_response = DB.user_nutritionist(user_id)
    registered_nutritionist_data = registered_nutritionist_response.data

    if registered_nutritionist_data and len(registered_nutritionist_data) > 0:
        # User is registered with a coach
        nutritionist_id = registered_nutritionist_data[0]['nutritionist_id']

        # Retrieve coach details from the users table
        nutritionist_response = DB.get_nutr_byid(nutritionist_id)
        nutritionist_data = nutritionist_response.data[0] if nutritionist_response.data else {}

        if nutritionist_data:
            nutritionist_name = f"{nutritionist_data['name']}"
            return render(request, "../templates/profile/registernutritionist.html", {
                'has_coach': True,
                'coach_id': nutritionist_id,
                'coach_name': nutritionist_name,
                'coach_number': nutritionist_data['phone_number'],
                'user': user
            })
        else:
            return render(request, "../templates/profile/registernutritionist.html", {
                'has_coach': True,
                'coach_id': nutritionist_id,
                'coach_name': "Unknown Nutritionist"
            })
    else:
        nutritionists = DB.get_nutritionists()

        return render(request, "../templates/profile/registernutritionist.html", {
            'has_coach': False,
            'coaches': nutritionists
        })
@login_required
def register_nutritionist(request):
    print('I AM INSIDE NUTRINISNo REGISTER FUNCITONNO')
    trainee_id = request.session.get('user_id')  

    if request.method == 'POST':
        nutritionist_id = request.POST.get('coach_id') 

        if nutritionist_id:
            response = DB.add_nutri_touser(trainee_id,nutritionist_id)

            if response: 
                return render(request, "../templates/profile/registernutritionist.html")
            else:
                return render(request, "../templates/profile/registernutritionist.html")  
        else:
            return render(request, "../templates/profile/registernutritionist.html")  

    return render(request, "../templates/profile/registernutritionist.html") 




@login_required
def rate_coach(request):
    trainee_id = request.session.get('user_id')  # Get the trainee's user ID

    if request.method == 'POST':
        rating = request.POST.get('rating')

        if not rating:
            return JsonResponse({"message": "Please provide a rating."}, status=400)

        # Fetch the coach_id from the registered_coach table
        registered_coach_response = DB.get_user_coach(trainee_id)
        registered_coach_data = registered_coach_response.data

        if not registered_coach_data or len(registered_coach_data) == 0:
            return JsonResponse({"message": "You are not registered with a coach."}, status=400)

        coach_id = registered_coach_data[0]['coach_id']

        # Insert the rating into the coach_ratings table
        response = DB.add_coach_ratting(trainee_id,coach_id,rating)

        if response:
            return JsonResponse({"message": "Successfully rated your coach!"}, status=200)
        else:
            return JsonResponse({"message": "An error occurred while rating your coach."}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)

@login_required
def rate_nutritionist(request):
    trainee_id = request.session.get('user_id')  # Get the trainee's user ID

    if request.method == 'POST':
        rating = request.POST.get('rating')

        if not rating:
            return JsonResponse({"message": "Please provide a rating."}, status=400)

        # Fetch the coach_id from the registered_coach table
        registered_coach_response = DB.user_nutritionist(trainee_id)
        registered_coach_data = registered_coach_response.data

        if not registered_coach_data or len(registered_coach_data) == 0:
            return JsonResponse({"message": "You are not registered with a coach."}, status=400)

        coach_id = registered_coach_data[0]['nutritionist_id']

        # Insert the rating into the coach_ratings table
        response = DB.rate_nutritionist(trainee_id,coach_id,rating)

        if response:
            return JsonResponse({"message": "Successfully rated your coach!"}, status=200)
        else:
            return JsonResponse({"message": "An error occurred while rating your coach."}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=405)




@login_required
def check_registered_coach(request):
    user_id = request.session.get('user_id')  # Retrieve the logged-in user's ID
    user = DB.get_user(user_id)[0]
    # Check if the user is registered with a coach
    registered_coach_response = DB.get_user_coach(user_id)
    registered_coach_data = registered_coach_response.data

    if registered_coach_data and len(registered_coach_data) > 0:
        # User is registered with a coach
        coach_id = registered_coach_data[0]['coach_id']

        # Retrieve coach details from the users table
        coach_response = DB.get_coach(coach_id)
        coach_data = coach_response.data[0] if coach_response.data else {}
        if coach_data:
            coach_name = f"{coach_data['name']}"
            return render(request, "../templates/profile/registercoach.html", {
                'has_coach': True,
                'coach_id': coach_id,
                'coach_name': coach_name,
                'coach_number': coach_data['phone_number'],
                'user': user
            })
        else:
            # Handle the case where coach details cannot be retrieved
            return render(request, "../templates/profile/registercoach.html", {
                'has_coach': True,
                'coach_id': coach_id,
                'coach_name': "Unknown Coach"
            })
    else:
        # User is not registered with a coach
        # Fetch all available coaches
        coaches = DB.get_Coaches()

        return render(request, "../templates/profile/registercoach.html", {
            'has_coach': False,
            'coaches': coaches
        })
@login_required
def register_coach(request):
    print('I AM INSIDE COAHCOID REGISTER FUNCITONNO')
    # Ensure the user is logged in and has a valid user ID
    trainee_id = request.session.get('user_id')  # Assume trainee_id is stored in the session

    if request.method == 'POST':
        coach_id = request.POST.get('coach_id')

        # Check if the coach_id is provided
        if coach_id:
            # Register the coach for the trainee
            response = DB.add_coach_touser(trainee_id,coach_id)

            if response: 
                # Optional: You can redirect the user to a confirmation page or the same page
                return render(request, "../templates/profile/registercoach.html")
            else:
                # If an error occurs with the registration
                return render(request, "../templates/profile/registercoach.html")
        else:
            # If no coach_id is selected
            return render(request, "../templates/profile/registercoach.html")

    return render(request, "../templates/profile/registercoach.html")