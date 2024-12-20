import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from UserBase import UserBase

class admin(UserBase) :
    def __init__(self, id):
        super().__init__(id)