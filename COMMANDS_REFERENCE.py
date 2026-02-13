#!/usr/bin/env python
"""
Quick Start & Common Commands for Personal Expense Tracker
"""

# ===========================
# 🚀 QUICK START
# ===========================

# 1. ACTIVATE VIRTUAL ENVIRONMENT (Windows)
# .\.venv\Scripts\activate

# 2. START DEVELOPMENT SERVER
# python manage.py runserver

# 3. ACCESS THE APP
# http://localhost:8000/

# ===========================
# 👤 USER MANAGEMENT
# ===========================

# Create superuser (admin account)
# python manage.py createsuperuser

# Create test user (in Django shell)
# python manage.py shell
# >>> from django.contrib.auth.models import User
# >>> User.objects.create_user('testuser', 'test@example.com', 'password123')

# List all users
# python manage.py shell
# >>> from django.contrib.auth.models import User
# >>> User.objects.all()

# Delete a user
# python manage.py shell
# >>> from django.contrib.auth.models import User
# >>> User.objects.get(username='testuser').delete()

# ===========================
# 💾 DATABASE MANAGEMENT
# ===========================

# Make migrations (detect model changes)
# python manage.py makemigrations

# Apply migrations (update database)
# python manage.py migrate

# Create migration for specific app
# python manage.py makemigrations expenses

# Apply migrations for specific app
# python manage.py migrate expenses

# Show migration status
# python manage.py migrate --list

# View SQL for a migration
# python manage.py sqlmigrate expenses 0001

# Reset database (WARNING: deletes all data!)
# python manage.py flush

# ===========================
# 🧪 TESTING & DEBUGGING
# ===========================

# Run Django shell with project context
# python manage.py shell

# Example: Create test expense
# >>> from expenses.models import Expense
# >>> from django.contrib.auth.models import User
# >>> from datetime import date
# >>> user = User.objects.first()
# >>> Expense.objects.create(
# ...     user=user,
# ...     amount=50.00,
# ...     category='Food',
# ...     description='Test expense',
# ...     date=date.today()
# ... )

# Query all expenses for a user
# >>> from expenses.models import Expense
# >>> expenses = Expense.objects.filter(user__username='testuser')
# >>> for exp in expenses:
# ...     print(f"{exp.date}: ${exp.amount} - {exp.category}")

# Calculate total monthly spending
# >>> from django.db.models import Sum
# >>> from datetime import datetime
# >>> today = datetime.now()
# >>> Expense.objects.filter(
# ...     user__username='testuser',
# ...     date__month=today.month
# ... ).aggregate(Sum('amount'))

# Check database file location (SQLite)
# python manage.py shell
# >>> from django.conf import settings
# >>> print(settings.DATABASES['default']['NAME'])

# ===========================
# 🔧 MAINTENANCE
# ===========================

# Collect static files
# python manage.py collectstatic --noinput

# Check for Python/Django issues
# python manage.py check

# Show all installed apps
# python manage.py show_apps

# Generate SECRET_KEY for production
# python manage.py shell
# >>> from django.core.management.utils import get_random_secret_key
# >>> print(get_random_secret_key())

# Clear cache
# python manage.py clear_cache

# ===========================
# 📦 DEPENDENCIES
# ===========================

# Install from requirements.txt
# pip install -r requirements.txt

# Update a package
# pip install --upgrade django

# Freeze current environment
# pip freeze > requirements.txt

# Check outdated packages
# pip list --outdated

# ===========================
# 🚀 DEPLOYMENT COMMANDS
# ===========================

# Generate static files for production
# python manage.py collectstatic --noinput --clear

# Run development server on public IP
# python manage.py runserver 0.0.0.0:8000

# Run with production WSGI
# gunicorn config.wsgi

# Check Django deployment checklist
# python manage.py check --deploy

# ===========================
# 🔐 SECURITY
# ===========================

# Generate new SECRET_KEY
# python manage.py shell
# >>> from django.core.management.utils import get_random_secret_key
# >>> print(get_random_secret_key())

# Change user password
# python manage.py changepassword username

# Create backup of database
# cp db.sqlite3 db.sqlite3.backup

# ===========================
# 📊 USEFUL DJANGO SHELL SNIPPETS
# ===========================

# python manage.py shell

# Import common modules
from django.contrib.auth.models import User
from expenses.models import Expense
from django.db.models import Sum
from datetime import date, timedelta

# Get all expenses for current user
user = User.objects.get(username='testuser')
expenses = Expense.objects.filter(user=user)

# Get expenses from this month
from django.utils import timezone
today = timezone.now().date()
monthly = Expense.objects.filter(
    user=user,
    date__month=today.month,
    date__year=today.year
)

# Calculate monthly total
total = monthly.aggregate(Sum('amount'))['amount__sum'] or 0
print(f"Total this month: ${total}")

# Group by category
from django.db.models import Sum
by_category = monthly.values('category').annotate(
    total=Sum('amount')
).order_by('-total')
for cat in by_category:
    print(f"{cat['category']}: ${cat['total']}")

# Get expenses from last 7 days
from datetime import timedelta
week_ago = today - timedelta(days=7)
last_week = Expense.objects.filter(
    user=user,
    date__gte=week_ago
)

# Delete all expenses for a user (careful!)
Expense.objects.filter(user=user).delete()

# Get recent expenses
recent = Expense.objects.filter(user=user)[:5]

# ===========================
# 🐛 TROUBLESHOOTING
# ===========================

# ModuleNotFoundError: No module named '...'
# Solution: pip install -r requirements.txt

# django.db.utils.OperationalError: no such table
# Solution: python manage.py migrate

# Port 8000 already in use
# Solution: python manage.py runserver 8001

# Static files not loading
# Solution: python manage.py collectstatic

# ALLOWED_HOSTS error
# Solution: Check .env file and ALLOWED_HOSTS setting

# PostgreSQL connection failed
# Solution: Check DATABASE_URL or DB_* variables

# ===========================
# 📚 HELPFUL URLS DURING DEVELOPMENT
# ===========================

# http://localhost:8000/                    - Home
# http://localhost:8000/accounts/register/  - Register
# http://localhost:8000/accounts/login/     - Login
# http://localhost:8000/accounts/logout/    - Logout
# http://localhost:8000/expenses/           - Dashboard
# http://localhost:8000/expenses/list/      - All Expenses
# http://localhost:8000/expenses/create/    - Add Expense
# http://localhost:8000/expenses/1/         - View Expense
# http://localhost:8000/expenses/1/edit/    - Edit Expense
# http://localhost:8000/expenses/1/delete/  - Delete Expense
# http://localhost:8000/admin/              - Admin Panel

# ===========================
# 🎯 ENVIRONMENT VARIABLES
# ===========================

# Edit .env file to change these locally:
# SECRET_KEY=your-secret-key
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
# USE_POSTGRESQL=False

# For production (Railway):
# SECRET_KEY=<secure-generated-key>
# DEBUG=False
# ALLOWED_HOSTS=<your-domain>
# USE_POSTGRESQL=True
# DB_* variables auto-configured

print("""
╔════════════════════════════════════════════════════════════════╗
║     Personal Expense Tracker - Quick Start Guide Ready!        ║
║                                                                ║
║  1. Activate venv: .\.venv\Scripts\activate                    ║
║  2. Run server: python manage.py runserver                     ║
║  3. Visit: http://localhost:8000/                              ║
║  4. Register/Login to start tracking expenses!                 ║
║                                                                ║
║  For more info, see README.md                                  ║
╚════════════════════════════════════════════════════════════════╝
""")
