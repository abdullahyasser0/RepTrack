from django.shortcuts import render
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

from Database.DatabaseCreation import DataBase
load_dotenv()

from authentication.services.UserService import UserService
from .services.schedule_service import ScheduleService
from .services.workout_service import WorkoutService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join( '..')))
from users.services.UserServices import UserService
from .repositories import schedule_repository 

logger = logging.getLogger(__name__)


User = UserService()

DB = DataBase()

# change_data,profile_view save_user_days,get_user_schedule,add_workout


def get_all_workouts():
    try:
        response = DB.get_workout()
        return response.data if response else []
    except Exception as e:
        print(f"Error fetching workouts: {e}")
        return []
# Create your views here.


@login_required
def add_workout(request):
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
            response = DB.add_workout(user_id,day,workout_id)

            if response:
                return JsonResponse({'success': True, 'message': 'Workout added successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to add workout.'}, status=500)

        except Exception as e:
            print("Error adding workout:", str(e))
            return JsonResponse({'success': False, 'message': 'An error occurred.'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)    



# @login_required
# def get_user_schedule(request):
#     user_id = request.session.get('user_id')
#     user = DB.get_user(user_id)[0]
#     days = get_user_preferred_days(user_id)
#     days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
#     # Fetch all workouts
#     all_workouts = get_all_workouts()
    
#     if not days:
#         return render(
#             request,
#             "../templates/profile/schedule.html",
#             {
#                 'user': user,
#                 'days': days,
#                 'days_of_week': days_of_week,
#                 'all_workouts': all_workouts
#             }
#         )
    
#     workouts_by_day = {}
    
#     for day in days:
#         # Query trainee_schedule to get workout_ids for the day
#         schedule_response = DB.get_user_train_scheduel(user_id,day)
        
#         schedule_data = schedule_response.data if schedule_response else []
#         if schedule_data:
#             workout_ids = [record['workout_id'] for record in schedule_data]
            
#             # Fetch details of workouts using workout_ids
#             if workout_ids:
#                 workout_details_response = DB.get_workout_byid(workout_ids)
#                 workouts_by_day[day] = workout_details_response.data if workout_details_response else []
#         else:
#             workouts_by_day[day] = []

#     return render(
#         request,
#         "../templates/profile/schedule.html",
#         {
#             'user': user,
#             'days': days,
#             'days_of_week': days_of_week,
#             'workouts_by_day': workouts_by_day,
#             'all_workouts': all_workouts
#         }
#     )

@login_required
def get_user_schedule(request):
    user_id = request.session.get('user_id')
    user =   User.Get_User(user_id)[0]   
    days = ScheduleService.get_user_preferred_days(user_id)
    all_workouts = WorkoutService.get_all_workouts()

    if not days:
        return render(
            request,
            "../templates/profile/schedule.html",
            {
                'user': user,
                'days': days,
                'days_of_week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                'all_workouts': all_workouts,
            }
        )

    workouts_by_day = {}
    for day in days:
        schedule_data = ScheduleService.get_user_schedule(user_id, day)
        
        if schedule_data:
            workout_ids = [record['workout_id'] for record in schedule_data]
            if workout_ids:
                workout_details_response = DB.get_workout_byid(workout_ids)
                workouts_by_day[day] = workout_details_response.data if workout_details_response else []
        else:
            workouts_by_day[day] = []

    return render(
        request,
        "../templates/profile/schedule.html",
        {
            'user': user ,
            'days': days,
            'days_of_week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'workouts_by_day': workouts_by_day,
            'all_workouts': all_workouts,
        }
    )


def save_user_days(request):
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            selected_days = data.get('days', [])

            if not selected_days:
                return redirect('schedule') 

            user_id = request.session.get('user_id')

            DB.delete_pred_day(user_id)
            print('Delete successful')

            day_records = [{'Uid': user_id, 'day': day} for day in selected_days]
            response = DB.insert_pref_day(day_records)

            return render(request, "../templates/profile/schedule.html")

        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return redirect('schedule') 
        except Exception as e:
            logger.error(f"Error saving user days: {e}")
            return redirect('schedule')  

    return redirect('schedule')  



def get_user_preferred_days(user_id):
    try:
        response = DB.get_pref_days(user_id)

        return [row['day'] for row in response.data]

    except Exception as e:
        print(f"Error fetching preferred days: {e}")
        raise



def Equip(request):
    user_id = request.session.get('user_id')
    user = DB.get_user(user_id)[0]
    equipments = DB.get_Equip()
    return render(request, "../templates/Admin/AddEquipment.html",{'id':user_id,'user':user,'equipments':equipments})