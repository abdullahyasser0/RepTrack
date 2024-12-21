from Database.DatabaseCreation import DataBase

DB = DataBase()

class WorkoutRepository:
    @staticmethod
    def get_all_workouts():
        return DB.get_workout()

    @staticmethod
    def get_workout_by_ids(workout_ids):
        return DB.get_workout_byid(workout_ids)