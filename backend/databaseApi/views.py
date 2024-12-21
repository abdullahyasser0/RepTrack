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




    


