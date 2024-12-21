import os
from supabase import create_client, Client



class DataBase :
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.SMTP_EMAIL=os.getenv("SMTP_EMAIL")
        self.SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
        self.supabase = create_client(self.supabase_url, self.supabase_key)
    
    def get_smtp_email(self):
        return self.SMTP_EMAIL
    
    def get_smtp_password(self):
        return self.SMTP_PASSWORD

    def creatSupabase(self):
        supabase: Client = create_client(self.supabase_url, self.supabase_key)
        return supabase
    
    def get_Memberships(self):
        return self.supabase.table("memberships").select("*").execute().data

    def get_Profiles(self):
        return self.supabase.table("profiles").select("*").execute().data

    def get_Posts(self):
        return self.supabase.table("posts").select("*").execute().data
    
    def get_Comments(self):
        return self.supabase.table("comments").select("*").execute().data

    def get_Users(self):
        return self.supabase.table("users").select("*").execute().data
    
    def get_Coaches(self):
        return self.supabase.table("users").select("*").eq('account_type','coach').execute().data
    
    def get_user_byEmail(self,email):
        return self.supabase.table('users').select('*').eq('email', email).execute()
    
    def get_payment(self):
        return self.supabase.table('payment').select('*').execute().data
    
    def get_user(self,UserID):
        return self.supabase.table("users").select("*").eq('user_id', UserID).execute().data
                           
    def insert_user(self,data):
        return self.supabase.table('users').insert(data).execute()

    def get_userName(self,id):
        return self.supabase.table('users').select('name').eq('user_id',id).execute().data
    
    def add_post(self,description,photoUrl,name ):
        return self.supabase.table('posts').insert({'description': description,"photoUrl":photoUrl,"no_likes":0,"posterName":name[0]["name"]}).execute()

    def update_password(self,hashed_new_password,id):
        return self.supabase.table('users').update({'password': hashed_new_password}).eq('user_id', id).execute()
    
    def update_userData(self,userName,contactInfo,email):
        return self.supabase.table('users').update({
                'name': userName,
                'phone_number': contactInfo,
                'email': email
            }).eq('user_id', id).execute()
    
    def clean__user_otps(self,email):
        return self.supabase.table("password_resets").delete().eq('email', email).execute()
    

    def insert_otp(self,email,otp,expires_at ):
        return self.supabase.table("password_resets").insert({
            "email": email,
            "otp": otp,
            "created_at": "now",  # Ensure your table has this field
            "expires_at": expires_at.isoformat()  # Ensure this field exists in your table
        }).execute()
    
    def get_otp(self,email,otp ):
        return self.supabase.table("password_resets").select("*").eq('email', email).eq('otp', otp).execute()
    
    def updated_restedPassword(self,hashed_password,current_time,email):
        return self.supabase.table("users").update({
            "password": hashed_password,
            "updated_at": current_time.isoformat()
        }).eq('email', email).execute()
    

    def add_comment_to_post(self,description,name,postID):
        return self.supabase.table('comments').insert({'comment': description,"commentorName":name[0]["name"],"post_id":postID}).execute()
