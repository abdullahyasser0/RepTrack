import os
import jwt
import sys
import json
import string
import random
import smtplib
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  check_password
from Database.DatabaseCreation import DataBase
logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DB = DataBase()
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta,timezone

class UserService:
    @staticmethod
    def create_user(name,email,phone_number,account_type,password):
        user_data = {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'account_type': account_type,
                'password': make_password(password)
            }
        DB.insert_user(user_data)
        return 200
        

    @staticmethod
    def authenticate_user(email, password,request):
        response = DB.get_user_byEmail(email)
        if response.data:
            user_data = response.data[0]
            stored_password = user_data['password']

            if check_password(password, stored_password):
                request.session['user_id'] = user_data['user_id']

                user, created = User.objects.get_or_create(username=user_data['email'])
                if created:
                    user.set_unusable_password()
                    user.save()

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                
                auth_login(request, user)
                
                return 200
            else:
                return 401
        else:
            return 401
        
    @staticmethod
    def changePassowrd(id,newPassword,oldPassword):
        response = DB.get_user(id)
        if response.data:
            user = response.data[0]
            stored_password = user['password']

            if check_password(oldPassword, stored_password):
                hashed_new_password = make_password(newPassword)
                update_response = DB.update_password(hashed_new_password,id)
                if update_response :
                    return 200
                else:
                    return 401
            return 402
        return 403
    
    @staticmethod
    def resetPassowrd(email,newPassword,otp):
        response = DB.get_otp(email,otp)
        if not response.data :
            return 403
        
        otp_record = response.data[0]
        expires_at_str = otp_record.get('expires_at')
        if not expires_at_str :
            return 405
        
        expires_at = datetime.fromisoformat(expires_at_str).replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if current_time > expires_at:
            return "expired"
        
        hashed_password = make_password(newPassword)

        # Update the user's password in the users table
        DB.updated_restedPassword(hashed_password,current_time,email)

        DB.clean__user_otps(email)

        return 200
    

    @staticmethod
    def ChangeData (userName,contactInfo,email):
        update_response = DB.update_userData(userName,contactInfo,email)
        if update_response:
            return 200
        return 400