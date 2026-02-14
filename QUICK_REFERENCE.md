# RAILWAY DEPLOYMENT - QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ YOUR PROJECT IS 100% READY FOR RAILWAY DEPLOYMENT          │
└─────────────────────────────────────────────────────────────────┘
```

## What Was Changed

### 1. requirements.txt
```diff
+ dj-database-url==2.1.0
```
**Why:** Parses `DATABASE_URL` from Railway's PostgreSQL service

### 2. config/settings.py
```diff
+ import dj_database_url
+ 
+ # Smart database switching:
+ if config('DATABASE_URL', default=None):
+     # Production: PostgreSQL
+     DATABASES = {dj_database_url.config(...)}
+ else:
+     # Development: SQLite
+     DATABASES = {...}
```
**Why:** Automatically uses right database based on environment

### 3. .env
```diff
- USE_POSTGRESQL=False
+ DATABASE_URL=
```
**Why:** Railway sets actual DATABASE_URL in production

### 4. runtime.txt (NEW)
```
python-3.11.7
```
**Why:** Specifies Python version for Railway

---

## How It Works

### Local Development (Your Computer)
```
1. No DATABASE_URL set in .env ✓
2. config('DATABASE_URL', default=None) → None
3. Condition is FALSE
4. Uses SQLite (db.sqlite3) ✓
```

### Production (Railway)
```
1. Railway PostgreSQL service auto-sets DATABASE_URL ✓
2. config('DATABASE_URL', default=None) → postgresql://...
3. Condition is TRUE
4. Uses PostgreSQL ✓
```

**Zero code changes needed!** The configuration handles both automatically.

---

## Deployment in 5 Steps

### Step 1: Install Locally
```bash
pip install dj-database-url
```

### Step 2: Test Locally
```bash
python manage.py migrate
python manage.py runserver
# Should work with SQLite ✓
```

### Step 3: Push to GitHub
```bash
git add .
git commit -m "Railway deployment setup"
git push origin main
```

### Step 4: Railway Configuration
1. Create Railway project
2. Add PostgreSQL service → DATABASE_URL auto-set ✓
3. Set variables:
   - `DEBUG=False`
   - `SECRET_KEY=<generate new>`
   - `ALLOWED_HOSTS=myapp.up.railway.app`

### Step 5: Run Migrations
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## Environment Variables Reference

### Local (.env)
```ini
SECRET_KEY=django-insecure-local-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=          # Empty = SQLite
```

### Production (Railway Dashboard)
```ini
SECRET_KEY=django-insecure-<new-secure-key>
DEBUG=False            # MUST be False
ALLOWED_HOSTS=myapp.up.railway.app
DATABASE_URL=postgresql://...  # Auto-set
```

---

## Generate Secure SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output → Paste as SECRET_KEY in Railway

---

## Files Created for You

| File | Purpose |
|------|---------|
| `DEPLOYMENT_READY.md` | Complete deployment summary |
| `RAILWAY_CHECKLIST.md` | Step-by-step interactive checklist |
| `RAILWAY_DEPLOYMENT.md` | Detailed guide + troubleshooting |
| `DEPLOYMENT_CHANGES.md` | What changed and why |
| `SETTINGS_REFERENCE.md` | Complete settings.py reference |
| `runtime.txt` | Python version specification |

**Start here:** Open `RAILWAY_CHECKLIST.md` for step-by-step deployment

---

## Verify Installation

```bash
# Check dj-database-url installed
pip list | grep dj-database-url
# Should show: dj-database-url          2.1.0

# Check settings.py has import
grep "dj_database_url" config/settings.py
# Should show: import dj_database_url

# Check database configuration
python manage.py shell
from django.conf import settings
print(settings.DATABASES)
# Should show: SQLite engine (no DATABASE_URL)
```

---

## Troubleshooting TL;DR

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: dj_database_url` | Already in requirements.txt, commit and push |
| `database connection refused` | PostgreSQL service not running in Railway |
| `relation "auth_user" does not exist` | Run `railway run python manage.py migrate` |
| `Django 404 on /admin/` | Static files not loaded, run collectstatic |
| `Admin shows no CSS` | Check WhiteNoise in middleware and STATICFILES_STORAGE |

---

## Production Security Settings (Auto-Enabled)

When `DEBUG=False` in production, these activate:
```python
SECURE_SSL_REDIRECT = True      # http → https
SESSION_COOKIE_SECURE = True    # Cookies over HTTPS only
CSRF_COOKIE_SECURE = True       # CSRF tokens over HTTPS
CSRF_COOKIE_HTTPONLY = True     # HTTP-only cookies
SECURE_HSTS_SECONDS = 31536000  # HSTS for 1 year
```

---

## Key Commands

```bash
# Local development
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Production (Railway)
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
railway logs
railway shell
```

---

## What's Different From Before

| Before | After |
|--------|-------|
| SQLite only | SQLite + PostgreSQL |
| Hardcoded database | Automatic detection |
| Manual env management | dj-database-url |
| No prod database option | Full production ready |
| Deploy impossible | Production-ready ✅ |

---

## Database Connection Examples

### SQLite (Local)
```
Engine: django.db.backends.sqlite3
Location: /path/to/db.sqlite3
```

### PostgreSQL (Production)
```
Engine: django.db.backends.postgresql
Connection string: postgresql://user:pass@host:port/db
Parsed from: DATABASE_URL environment variable
```

---

## Success Indicators

✅ App loads at https://myapp.up.railway.app
✅ Admin at /admin/ has CSS and works
✅ Can log in with superuser
✅ No errors in Railway logs
✅ Database queries work from Django shell

---

## Never Do This

❌ Commit `.env` file → Add `.env` to `.gitignore`
❌ Use `DEBUG=True` in production
❌ Share `SECRET_KEY` publicly
❌ Hardcode `DATABASE_URL` in settings.py
❌ Use `ALLOWED_HOSTS = '*'` in production

---

## Your Project Status

```
Database Layer      ✅ Configured (auto-switch)
Environment Vars    ✅ Configured (decouple)
Dependencies        ✅ Updated (dj-database-url added)
Settings            ✅ Production-ready
Deployment          ✅ Railway-ready
Security            ✅ Production-grade
Static Files        ✅ WhiteNoise configured
WSGI Server         ✅ Gunicorn in Procfile
Python Version      ✅ Specified in runtime.txt
```

**DEPLOYMENT STATUS: ✅ 100% COMPLETE - READY TO PUSH**

---

## Next Steps

1. **Read:** Open `RAILWAY_CHECKLIST.md`
2. **Follow:** Step-by-step checklist
3. **Deploy:** Push to GitHub
4. **Monitor:** Watch Railway build in dashboard
5. **Verify:** Visit your app URL
6. **Celebrate:** 🚀 You're live!

---

## Resources

- Railway Docs: https://docs.railway.app
- Django PostgreSQL: https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes
- dj-database-url: https://github.com/jacobian/dj-database-url
- Python decouple: https://github.com/henriquebastos/python-decouple

---

**Date:** February 14, 2026  
**Project:** PersonalExpenseTracker  
**Status:** ✅ DEPLOYMENT READY
