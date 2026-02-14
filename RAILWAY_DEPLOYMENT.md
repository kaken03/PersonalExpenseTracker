# Railway Deployment Checklist & Guide

## ✅ Pre-Deployment Configuration Completed

Your project has been updated with the following:

### 1. **Dependencies Added** ✓
- `dj-database-url==2.1.0` - Parse DATABASE_URL for PostgreSQL connection
- `psycopg2-binary==2.9.10` - PostgreSQL database adapter (already present)
- `gunicorn==22.0.0` - Production WSGI server (already present)
- `whitenoise==6.6.0` - Static files serving (already present)

### 2. **Database Configuration** ✓
- **Local Development**: SQLite (default)
- **Production (Railway)**: PostgreSQL via `DATABASE_URL`
- Automatic detection: Uses `DATABASE_URL` if set, otherwise falls back to SQLite

### 3. **Settings.py Updates** ✓
```python
# Automatic database switching:
if config('DATABASE_URL', default=None):
    DATABASES = {...PostgreSQL...}  # Production
else:
    DATABASES = {...SQLite...}      # Development
```

### 4. **Environment Variables** ✓
Updated `.env` file is ready. Railway will automatically provide:
- `DATABASE_URL` - PostgreSQL connection string
- Other variables can be set in Railway dashboard

---

## 📋 Step-by-Step Railway Deployment

### Step 1: Install New Dependencies Locally
```bash
pip install -r requirements.txt
# or
pip install dj-database-url==2.1.0
```

### Step 2: Test Locally with SQLite (No DATABASE_URL)
```bash
# Should work fine with SQLite
python manage.py migrate
python manage.py runserver
```

### Step 3: Create Railway Account & Project
1. Go to [Railway.app](https://railway.app)
2. Sign up or log in
3. Create a new project

### Step 4: Add PostgreSQL Database to Railway
1. In Railway dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway automatically creates `DATABASE_URL` environment variable
4. Copy the connection string for reference (starts with `postgresql://`)

### Step 5: Connect GitHub Repository
1. Create a GitHub repository with your code
2. In Railway, click "Connect GitHub"
3. Choose your repository
4. Railway auto-detects Django project

```bash
# Push your code to GitHub
git add .
git commit -m "Prepare for Railway deployment with PostgreSQL"
git push origin main
```

### Step 6: Configure Railway Environment Variables
In Railway Dashboard → Your Project → Settings:

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | Generate a new secure key | See below for generation |
| `DEBUG` | `False` | Production must be False |
| `ALLOWED_HOSTS` | Your Railway domain | e.g., `myapp.up.railway.app` |
| `DATABASE_URL` | Auto-set by PostgreSQL | Don't edit manually |

### Generate Secure SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and set it in Railway.

### Step 7: Configure Procfile (Already Done)
Your `Procfile` is configured:
```
web: gunicorn config.wsgi
```
This tells Railway how to start your app.

### Step 8: Run Migrations on Production
Railway will deploy automatically. After deployment, run migrations:

**Option A: Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link

# Run migrations
railway run python manage.py migrate
```

**Option B: Railway Dashboard**
1. Go to your app deployments
2. Click on latest deployment
3. Go to "Logs" tab
4. Run command: `python manage.py migrate`

### Step 9: Create Superuser (Admin) on Production
```bash
railway run python manage.py createsuperuser
```

Or via Railway CLI:
```bash
railway run python manage.py createsuperuser
```

### Step 10: Verify Deployment
1. **Check Build Logs**
   - Railway Dashboard → Deployments → View logs
   - Look for: `Collecting dj-database-url` ✓

2. **Check Application Health**
   - Visit your app URL: `https://your-app-name.up.railway.app`
   - Should load without errors

3. **Check Database Connection**
   - Admin should be accessible: `/admin/`
   - Should connect to PostgreSQL

4. **Check Static Files**
   - CSS/JS should load (WhiteNoise handles this)

---

## 🔒 Production Settings Applied

Your settings.py now includes:

```python
# Only applied when DEBUG=False (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True           # Redirect HTTP → HTTPS
    SESSION_COOKIE_SECURE = True         # Cookies over HTTPS only
    CSRF_COOKIE_SECURE = True            # CSRF protection over HTTPS
    CSRF_COOKIE_HTTPONLY = True          # CSRF cookie HTTP-only
    SECURE_HSTS_SECONDS = 31536000       # HSTS for 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True           # Include in HSTS preload list
```

---

## 🔧 Troubleshooting

### Issue: Build fails with "Module not found"
**Solution**: Railway didn't install dependencies
- Check `requirements.txt` is in root directory
- Verify all packages have versions specified
- Railway run: `railway run pip install -r requirements.txt`

### Issue: "Database connection refused"
**Solution**: DATABASE_URL not set or incorrect
- Check Railway PostgreSQL service is running
- Verify `DATABASE_URL` in Railway dashboard
- Check: `railway run python manage.py dbshell`

### Issue: Static files not loading (404 on CSS/JS)
**Solution**: WhiteNoise not serving files
- Verify `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings

### Issue: Admin login not working
**Solution**: Migrations not applied
- Run: `railway run python manage.py migrate`
- Create superuser: `railway run python manage.py createsuperuser`

### Issue: "DEBUG must be False in production"
**Alert**: This is correct! Never set DEBUG=True in production
- Railway will show env var: `DEBUG=False`
- This is automatically True locally (no DATABASE_URL)

---

## 📊 Database Migration Path

```
Local Development          Production (Railway)
───────────────────        ────────────────────
SQLite Database      →      PostgreSQL Database
(db.sqlite3)                (via DATABASE_URL)

Migration command runs automatically:
$ python manage.py migrate
```

---

## 📌 Important Notes

1. **Never commit `.env` to Git**
   - Add to `.gitignore`: `echo ".env" >> .gitignore`
   - Railway reads from Dashboard, not from file

2. **Local vs Production**
   - Locally: No `DATABASE_URL` → Uses SQLite ✓
   - Production: `DATABASE_URL` set → Uses PostgreSQL ✓

3. **Scaling**
   - PostgreSQL supports multiple dynos (Railway instances)
   - SQLite only works for single instance (local development)

4. **Backups**
   - Railway auto-backups PostgreSQL
   - Check Railway Dashboard → Database → Backups

---

## ✨ Quick Commands Reference

```bash
# Local development
python manage.py migrate
python manage.py runserver

# Production (Railway CLI)
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
railway logs                    # View app logs
```

---

## ✅ Deployment Summary

Your project is **100% ready** for Railway with:
- ✓ PostgreSQL support
- ✓ SQLite local development
- ✓ All required dependencies
- ✓ Security settings for production
- ✓ Static files handling with WhiteNoise
- ✓ Proper database configuration

**Next Step**: Follow "Step 5: Connect GitHub Repository" above to deploy!
