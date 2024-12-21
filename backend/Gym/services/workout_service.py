from repositories.workout_repository import WorkoutRepository
import logging

logger = logging.getLogger(__name__)

class WorkoutService:
    @staticmethod
    def get_all_workouts():
        try:
            response = WorkoutRepository.get_all_workouts()
            return response.data if response else []
        except Exception as e:
            logger.error(f"Error fetching workouts: {e}")
            return []

    @staticmethod
    def get_workout_details(workout_ids):
        try:
            response = WorkoutRepository.get_workout_by_ids(workout_ids)
            return response.data if response else []
        except Exception as e:
            logger.error(f"Error fetching workout details: {e}")
            return []