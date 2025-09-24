from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        # These are the login details for your admin account
        username = "admin"
        email = "christianchinonso000@gmail.com"
        password = "admin123456"  # You'll change this later
        
        # Check if admin user already exists
        if not User.objects.filter(username=username).exists():
            # Create the admin user
            User.objects.create_superuser(username, email, password)
            print(f"✅ Superuser {username} created successfully!")
        else:
            print(f"⚠️ Superuser {username} already exists")