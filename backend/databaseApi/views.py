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



DB = DataBase()




def logout_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('profiles')  
        return view_func(request, *args, **kwargs)
    return wrapper

def get_all_workouts():
    """
    Fetches all workouts from the system_workout table.
    Returns a list of workout records.
    """
    try:
        response = supabase.table('system_workout') \
                           .select('system_workout_id','workout_name, description, duration, difficulty_level, target_muscle_group') \
                           .execute()
        return response.data if response else []
    except Exception as e:
        print(f"Error fetching workouts: {e}")
        return []

@login_required
def add_workout(request):
    print("THE ADD WORKOUT IS BEING CALLED UPON")
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')  # Get the user ID from the session
            data = json.loads(request.body)
            day = data.get('day')
            workout_id = data.get('workout_id')
        

            if not user_id or not day or not workout_id:
                return JsonResponse({'success': False, 'message': 'Missing required parameters.'}, status=400)
            print("THE USER ID IS ",user_id)
            print("the workout id is ",workout_id)
            print('the day is ', day)

            # Insert the new workout into the trainee_schedule table
            response = supabase.table('trainee_schedule').insert({
                'trainee_id': user_id,
                'day': day,
                'workout_id': workout_id
            }).execute()

            if response:
                return JsonResponse({'success': True, 'message': 'Workout added successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to add workout.'}, status=500)

        except Exception as e:
            print("Error adding workout:", str(e))
            return JsonResponse({'success': False, 'message': 'An error occurred.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

@login_required
def get_user_schedule(request):
    user_id = request.session.get('user_id')
    user = get_user1(user_id)[0]
    days = get_user_preferred_days(user_id)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Fetch all workouts
    all_workouts = get_all_workouts()
    
    if not days:
        return render(
            request,
            "../templates/profile/schedule.html",
            {
                'user': user,
                'days': days,
                'days_of_week': days_of_week,
                'all_workouts': all_workouts
            }
        )
    
    workouts_by_day = {}
    
    for day in days:
        # Query trainee_schedule to get workout_ids for the day
        schedule_response = supabase.table('trainee_schedule') \
                                     .select('workout_id') \
                                     .eq('trainee_id', user_id) \
                                     .eq('day', day) \
                                     .execute()
        
        schedule_data = schedule_response.data if schedule_response else []
        if schedule_data:
            workout_ids = [record['workout_id'] for record in schedule_data]
            
            # Fetch details of workouts using workout_ids
            if workout_ids:
                workout_details_response = supabase.table('system_workout') \
                                                    .select('system_workout_id, workout_name, description, duration, difficulty_level, target_muscle_group') \
                                                    .in_('system_workout_id', workout_ids) \
                                                    .execute()
                workouts_by_day[day] = workout_details_response.data if workout_details_response else []
        else:
            workouts_by_day[day] = []

    return render(
        request,
        "../templates/profile/schedule.html",
        {
            'user': user,
            'days': days,
            'days_of_week': days_of_week,
            'workouts_by_day': workouts_by_day,
            'all_workouts': all_workouts
        }
    )



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
                    print('User: ', user)
                    if created:
                        print('its created')
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
    

def save_user_days(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            selected_days = data.get('days', [])

            if not selected_days:
                return redirect('schedule') 

            user_id = request.session.get('user_id')

            supabase.table('user_preferred_days').delete().eq('Uid', user_id).execute()
            print('Delete successful')

            day_records = [{'Uid': user_id, 'day': day} for day in selected_days]
            response = supabase.table('user_preferred_days').insert(day_records).execute()

            return render(request, "../templates/profile/schedule.html")

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return redirect('schedule') 
        except Exception as e:
            logger.error(f"Error saving user days: {e}")
            return redirect('schedule')  

    return redirect('schedule')  

def get_user(userid):
    response = supabase.table("countries").select("id, name, cities(name)").\
    join("cities", "countries.id", "cities.country_id").execute()

@login_required
def profile_view(request):
    print(request.session.items())
    user_id = request.session.get('user_id')
    if user_id:
        print('User ID: ', user_id)
        return render(request, 'profile/information.html')  
    else:
        return redirect('login')


def get_user_preferred_days(user_id):
    try:
        response = supabase.table('user_preferred_days').select('day').eq('Uid', user_id).execute()

        return [row['day'] for row in response.data]

    except Exception as e:
        print(f"Error fetching preferred days: {e}")
        raise



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
