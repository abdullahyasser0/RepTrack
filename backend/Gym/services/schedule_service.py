import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join( '..')))
from Gym.repositories.schedule_repository import ScheduleRepository
import logging

logger = logging.getLogger(__name__)

class ScheduleService:
    @staticmethod
    def get_user_preferred_days(user_id):
        try:
            response = ScheduleRepository.get_preferred_days(user_id)
            return [row['day'] for row in response.data]
        except Exception as e:
            logger.error(f"Error fetching preferred days: {e}")
            return []

    @staticmethod
    def save_user_days(user_id, selected_days):
        try:
            ScheduleRepository.delete_preferred_days(user_id)
            day_records = [{'Uid': user_id, 'day': day} for day in selected_days]
            ScheduleRepository.insert_preferred_days(day_records)
            return True
        except Exception as e:
            logger.error(f"Error saving user days: {e}")
            return False
        
    @staticmethod
    def get_user_schedule(user_id, day):
        res =  ScheduleRepository.get_user_schedule(user_id, day)
        return res.data if res else []