
from Database.DatabaseCreation import DataBase

class trainee :
    def __init__(self, id):
        DB = DataBase
        self.supabase = DB.creatSupabase()
        self.traineee_Id = id
    
    def get_user_data(self):
        response = self.supabase.table("users").select("*").eq('user_id', self.traineee_Id).execute().data
        return response