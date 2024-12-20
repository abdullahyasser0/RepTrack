from backend.userCreation.theadmin import admin
from trainee import trainee
from nutritionist import nutritionist
from coach import coach
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



class UserFactory:
    @staticmethod
    def create_user(user_type, ID):
        if user_type == 'admin':
            return admin(ID)
        elif user_type == 'coach':
            return coach(ID)
        elif user_type == 'nutritionist':
            return nutritionist(ID)
        elif user_type == 'trainee':
            return trainee(ID)
        else:
            raise ValueError("Invalid user type")
        

# trainee = UserFactory.create_user("admin",67)

# print(trainee.get_info())