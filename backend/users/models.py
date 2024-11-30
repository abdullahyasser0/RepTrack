from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supabase_user_id = models.CharField(max_length=255, unique=True)  # Supabase user ID
    google_name = models.CharField(max_length=255, null=True, blank=True)  # Google user's name
    google_picture = models.URLField(null=True, blank=True)  # URL for profile picture
    membership_status = models.CharField(max_length=100, default='inactive')  # Gym membership status (e.g., active, inactive)
    membership_type = models.CharField(max_length=100, default='basic')  # Membership type (e.g., basic, premium)
    # Other gym-specific fields can be added here (e.g., workout goals, progress, etc.)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # You can add additional methods if needed to handle user-specific logic
    def is_active_member(self):
        return self.membership_status == 'active'

    def update_membership(self, new_status, new_type):
        self.membership_status = new_status
        self.membership_type = new_type
        self.save()
