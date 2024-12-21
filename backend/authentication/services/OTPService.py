
import os
import jwt
import sys
import json
import string
import random
import smtplib
import logging
from email.message import EmailMessage
from datetime import datetime, timedelta,timezone
from Database.DatabaseCreation import DataBase

logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DB = DataBase()

class OTPService:
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp(email: str, otp: str):
        sender_name = 'RepTrackAdmin'
        smtp_host = 'smtp.gmail.com'
        smtp_port = 587
        
        msg = EmailMessage()
        msg['From'] = f"{sender_name} <{DB.get_smtp_email()}>"
        msg['To'] = email
        msg['Subject'] = "Your OTP Code"
        msg.set_content(f"Hello,\n\nYour Reset Password OTP code is: {otp}\n\nThank you!")

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(DB.get_smtp_email(), DB.get_smtp_password())
                server.send_message(msg)
        except Exception as e:
            raise
    
    @staticmethod
    def generate_otp(email):
        otp = OTPService.generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        DB.insert_otp(email, otp, expires_at)
        OTPService.send_otp(email, otp)
        return otp


    @staticmethod
    def verify_otp(email, otp):
        response = DB.get_otp(email, otp)
        if not response.data:
            return False
        otp_record = response.data[0]
        expires_at = datetime.fromisoformat(otp_record['expires_at']).replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) <= expires_at