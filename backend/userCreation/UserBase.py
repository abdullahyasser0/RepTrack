import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.DatabaseCreation import DataBase

class UserBase :
    def __init__ (self,UserId):
        self.id = UserId
        self.DataBase = DataBase()
        self.SuperBaseInstance = self.DataBase.creatSupabase()
    
    def get_info(self):
        return self.SuperBaseInstance.table("users").select("*").eq('user_id', self.id).execute().data