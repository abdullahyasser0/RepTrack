from django.shortcuts import render
import os
from supabase import create_client, Client
from django.contrib.auth.hashers import make_password,check_password

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

def signup(name,email,phoneNumber,type,password):
    data = {
        'name': name,
        'email': email,
        'phone_number': phoneNumber,
        'account_type': type,
        'password': make_password(password)
    }
    print('user data: ',data)
    supabase.table('users').insert(data).execute()
    return True

#for admin
def get_Profiles():
    return supabase.table("profiles").select("*").execute()

def get_Users():
    return supabase.table("users").select("*").execute()

def signup(name,email,phoneNumber,type,password):
    data = {
        'name': name,
        'email': email,
        'phone_number': phoneNumber,
        'account_type': type,
        'password': make_password(password)
    }
    supabase.table('users').insert(data).execute()
    return True


def login(email,password):
    response = supabase.table('users').select('*').eq('email', email).execute()
    if response.data:
        user = response.data[0]
        stored_password = user['password']

        if check_password(password, stored_password):
            return True
        else:
             return False
    else:
         return False
    


def get_user(userid):
    response = supabase.table("countries").select("id, name, cities(name)").\
    join("cities", "countries.id", "cities.country_id").execute()