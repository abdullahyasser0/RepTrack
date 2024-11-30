from django.shortcuts import render
import os
from supabase import create_client, Client

url: str = "https://sodghnhticinsggmbber.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvZGdobmh0aWNpbnNnZ21iYmVyIiwicm9sZSI6ImFu"
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


