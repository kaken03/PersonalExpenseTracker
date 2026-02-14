import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django BEFORE importing models
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
else:
    User.objects.create_superuser(username, email, password)
    print(f"✓ Superuser '{username}' created successfully!")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
