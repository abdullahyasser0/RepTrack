import os
from supabase import create_client, Client



class DataBase :
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
    # global SMTP_EMAIL, SMTP_PASSWORD
    # SMTP_EMAIL=os.getenv("SMTP_EMAIL")
    # SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
    def creatSupabase(self):
        supabase: Client = create_client(self.supabase_url, self.supabase_key)
        return supabase