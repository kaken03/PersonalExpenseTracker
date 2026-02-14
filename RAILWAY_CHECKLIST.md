# 🚀 RAILWAY DEPLOYMENT CHECKLIST - Step by Step

## Phase 1: Local Preparation (Your Computer)

### ✓ Install Dependencies
```bash
pip install dj-database-url==2.1.0
pip install -r requirements.txt
```

### ✓ Test Locally with SQLite
```bash
# This should work without DATABASE_URL
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- [ ] Visit http://localhost:8000 - **Should load**
- [ ] Admin at http://localhost:8000/admin - **Should work**
- [ ] App functionality working - **Confirm**

### ✓ Verify Configuration
```bash
# Check settings.py has dj_database_url import
grep "dj_database_url" config/settings.py

# Should show both SQLite and PostgreSQL conditions
grep -A 10 "if config('DATABASE_URL'" config/settings.py
```

### ✓ Update Git
```bash
git add .
git commit -m "Configure for Railway deployment with PostgreSQL"
git push origin main
```
- [ ] All changes committed
- [ ] Code pushed to GitHub main branch

---

## Phase 2: Railway Setup (railway.app)

### Step 1: Create Railway Account
- [ ] Go to https://railway.app
- [ ] Sign up with GitHub (easiest)
- [ ] Create new project

### Step 2: Add PostgreSQL Database
1. [ ] In Railway dashboard, click "+ Add Service"
2. [ ] Select "PostgreSQL"
3. [ ] Railway creates the service automatically
4. [ ] **Copy the generated DATABASE_URL** (you'll need it)

### Step 3: Connect GitHub Repository
1. [ ] In Railway project, click "Connect GitHub"
2. [ ] Select your repository
3. [ ] Select `main` branch (or your default)
4. [ ] Railway will detect it's a Django app (from Procfile)

**At this point:**
- [ ] Build should start automatically
- [ ] You can watch deployment in Logs tab

---

## Phase 3: Environment Variables (Critical!)

### Step 1: Access Environment Variables
In Railway Dashboard:
1. [ ] Go to your project
2. [ ] Click your app service (not PostgreSQL)
3. [ ] Go to "Variables" tab

### Step 2: Set Environment Variables

Add these exact variables:

#### Variable 1: DEBUG
- [ ] **Name:** `DEBUG`
- [ ] **Value:** `False`
- [ ] Click Save

#### Variable 2: SECRET_KEY
1. [ ] Generate secure key locally:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. [ ] Copy the output
3. [ ] [ ] **Name:** `SECRET_KEY`
4. [ ] **Value:** Paste the key
5. [ ] Click Save

#### Variable 3: ALLOWED_HOSTS
After first deployment, you'll get a domain like `myapp-xyz.up.railway.app`

- [ ] **Name:** `ALLOWED_HOSTS`
- [ ] **Value:** `myapp-xyz.up.railway.app` (your actual domain)
- [ ] Click Save

#### Variable 4: DATABASE_URL
- [ ] **Status:** Should be auto-set by PostgreSQL service ✓
- [ ] Don't need to set manually
- [ ] Verify it exists in Variables tab

**Environment Variables Summary:**
```
DEBUG=False
SECRET_KEY=django-insecure-xxxxxxxxxxxxx
ALLOWED_HOSTS=myapp-xyz.up.railway.app
DATABASE_URL=postgresql://user:pass@host:5432/db
```

---

## Phase 4: Run Migrations (Critical!)

**After first deployment, run migrations on production:**

### Option A: Using Railway CLI (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link your Railway project locally
railway link

# Run migrations
railway run python manage.py migrate
```

### Option B: Using Railway Dashboard
1. [ ] Go to Railway Dashboard → Your App → Deployments
2. [ ] Click latest (top) deployment
3. [ ] Go to "Logs" tab
4. [ ] Click command input at bottom
5. [ ] Type: `python manage.py migrate`
6. [ ] Press Enter
7. [ ] Wait for "Operations to perform" message

- [ ] Migrations successful (check output)

### Option C: Using Railway Web Terminal
1. [ ] In Railway, click your app
2. [ ] Find "Terminal" or "Logs" section
3. [ ] Click "Execute" or terminal icon
4. [ ] Run: `python manage.py migrate`
5. [ ] Watch for success output

---

## Phase 5: Create Production Superuser

Run one of these commands:

```bash
railway run python manage.py createsuperuser
```

Or via web terminal:
```
python manage.py createsuperuser
```

Follow prompts:
- [ ] Username: Enter a username
- [ ] Email: Enter admin email
- [ ] Password: Enter secure password (20+ chars)
- [ ] Confirm password

Save these credentials in a secure place! 🔒

---

## Phase 6: Verify Deployment

### Test 1: Check Application Health
- [ ] Visit `https://myapp-xyz.up.railway.app` in browser
- [ ] Should load your home page without errors
- [ ] CSS/JS should load (from WhiteNoise)

### Test 2: Check Static Files
- [ ] Visit `/admin/` URL
- [ ] Admin interface should have styling (CSS loaded)
- [ ] If blank/ugly = static files not loading

### Test 3: Check Database Connection
- [ ] Admin login: `/admin/`
- [ ] Use superuser credentials created above
- [ ] Should log in successfully
- [ ] Browse admin interface (data should load from PostgreSQL)

### Test 4: Check Logs for Errors
In Railway Dashboard:
- [ ] Go to Logs tab
- [ ] Look for red error messages
- [ ] Should see: "Started server process [1]"
- [ ] Should NOT see: database connection errors

---

## Phase 7: Post-Deployment Checks

### ✓ Verify PostgreSQL Connected
```bash
railway run python manage.py dbshell
```
Output should show PostgreSQL prompt:
```
psql (version number)
myapp=#
```
- [ ] Connected successfully

### ✓ Verify Django Settings
```bash
railway run python manage.py shell
```
Then in Python:
```python
from django.conf import settings
print(settings.DATABASES)
# Should show PostgreSQL engine
print(settings.DEBUG)
# Should show False
```
- [ ] PostgreSQL shows as engine
- [ ] DEBUG is False

### ✓ Check Static Files Collected
```bash
railway run python manage.py collectstatic --noinput
```
- [ ] Should complete without errors

---

## Troubleshooting Checklist

### 🔴 Build Failed - Module Not Found
```
ModuleNotFoundError: No module named 'dj_database_url'
```
**Solution:**
- [ ] Add `dj-database-url==2.1.0` to requirements.txt
- [ ] Commit and push to GitHub
- [ ] Railway will auto-redeploy

### 🔴 Database Connection Error
```
OperationalError: could not connect to server
```
**Solution:**
- [ ] Verify PostgreSQL service exists in Railway
- [ ] Check DATABASE_URL variable is set
- [ ] Ensure PostgreSQL service is running (green status)
- [ ] Check credentials in DATABASE_URL

### 🔴 Admin Page Shows No CSS
`Static files not loading`
**Solution:**
- [ ] Run: `railway run python manage.py collectstatic --noinput`
- [ ] Check: `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
- [ ] Restart app (redeploy)

### 🔴 500 Error on Load
**Solution:**
- [ ] Check Railway Logs tab
- [ ] Look for specific error message
- [ ] Common: migrations not run → run `railway run python manage.py migrate`
- [ ] Common: SECRET_KEY not set → set in Variables

### 🔴 Migrations Never Applied
```
django.db.utils.ProgrammingError: relation "auth_user" does not exist
```
**Solution:**
- [ ] Run: `railway run python manage.py migrate`
- [ ] Check output for "Apply all migrations"
- [ ] Retry: `railway run python manage.py migrate --run-syncdb`

### 🔴 Cannot Login to Admin
**Solution:**
- [ ] Superuser not created: `railway run python manage.py createsuperuser`
- [ ] Check credentials are correct
- [ ] Try different browser/incognito
- [ ] Check database is PostgreSQL (not SQLite)

---

## Success Indicators ✅

Your deployment is successful when:

1. ✅ Railway shows "UP" status (green checkmark)
2. ✅ App loads at `https://myapp-xyz.up.railway.app` 
3. ✅ Admin page at `/admin/` has styling and loads
4. ✅ Can log in with superuser credentials
5. ✅ Railway Logs show "Started server process"
6. ✅ No red error messages in logs
7. ✅ Database commands work: `railway run python manage.py shell`
8. ✅ PostgreSQL shows in: `python manage.py dbshell`

---

## Maintenance Commands

```bash
# View logs
railway logs

# Run Django management commands
railway run python manage.py <command>

# Create backup of PostgreSQL (Railway does this automatically)
# Check Dashboard → Database → Backups

# SSH into app container (if needed)
railway shell

# Stop/restart app
Railway Dashboard → Your App → More → Restart
```

---

## Important Notes

⚠️ **Never commit .env file** - Add to .gitignore:
```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore .env file"
```

⚠️ **DEBUG must be False in production** - This is a security requirement

⚠️ **SECRET_KEY must be unique and secure** - Generate new for production

⚠️ **DATABASE_URL is secret** - Never share or commit it

⚠️ **PostgreSQL DATABASE_URL format:**
```
postgresql://username:password@host:port/database

Example:
postgresql://admin:xyz123@brevnob.railway.internal:5432/railway
```

---

## Quick Summary

1. **Install locally:** `pip install dj-database-url`
2. **Test locally:** `python manage.py migrate && python manage.py runserver`
3. **Push to GitHub:** `git push origin main`
4. **Railway setup:** Add PostgreSQL service
5. **Set variables:** DEBUG=False, SECRET_KEY=xxx, ALLOWED_HOSTS=xxx
6. **Run migrations:** `railway run python manage.py migrate`
7. **Create admin:** `railway run python manage.py createsuperuser`
8. **Verify:** Visit app URL and log in to admin ✅

---

## Your Contact References

- Railway Docs: https://docs.railway.app
- Django PostgreSQL: https://docs.djangoproject.com/en/6.0/backends/postgresql
- dj-database-url: https://github.com/jacobian/dj-database-url
- Railway CLI: https://docs.railway.app/reference/cli

---

**Status: Your project is 100% ready for deployment! 🚀**
