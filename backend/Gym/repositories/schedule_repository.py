from Database.DatabaseCreation import DataBase

DB = DataBase()

class ScheduleRepository:
    @staticmethod
    def get_user_schedule(user_id, day):
        return DB.get_user_train_scheduel(user_id, day)

    @staticmethod
    def delete_preferred_days(user_id):
        return DB.delete_pred_day(user_id)

    @staticmethod
    def insert_preferred_days(day_records):
        return DB.insert_pref_day(day_records)

    @staticmethod
    def get_preferred_days(user_id):
        return DB.get_pref_days(user_id)