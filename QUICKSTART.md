# CareerPilot — Quick Start Guide

Get CareerPilot running locally on Windows in less than 2 minutes.

---

## Method 1: One-Click Windows Automated Setup (Recommended)

1. Double-click or execute in PowerShell:
   ```cmd
   setup.bat
   ```
   This will:
   - Detect Python 3.10+ (preferring Python 3.12).
   - Create a dedicated virtual environment in `.venv`.
   - Install all required dependencies from `requirements.txt`.
   - Initialize the database and run migrations.
   - Populate realistic demonstration data.

2. Launch the server:
   ```cmd
   run.bat
   ```

3. Open your browser:
   `http://127.0.0.1:8000/`

4. Log in:
   - **Demo User:** `demo_user` / `DemoPassword123!`
   - **Admin / Superuser:** `admin` / `AdminPassword123!` (Access Django Admin at `http://127.0.0.1:8000/admin/`)

---

## Method 2: Manual Terminal Setup

```powershell
# 1. Navigate to project root
cd "D:\90 days\90-days-90-projects-day-14-careerpilot"

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment file
Copy-Item .env.example .env

# 6. Run database migrations
python manage.py migrate

# 7. Seed demo candidate workspace
python manage.py load_sample_data

# 8. Start development server
python manage.py runserver 127.0.0.1:8000
```

---

## Automated Test Verification

Run the complete 34-test automated verification suite:

```cmd
test.bat
```
or via Python:
```powershell
.\.venv\Scripts\python.exe manage.py test tests
```
