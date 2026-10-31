# CareerPilot — Troubleshooting Guide

Common issues and their resolutions when running CareerPilot locally on Windows:

---

## 1. Port 8000 Already in Use
**Symptom:** `Error: That port is already in use.`  
**Cause:** Another local web server or background process is listening on `127.0.0.1:8000`.  
**Resolution:**
Specify an alternative port:
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8080
```

---

## 2. PostgreSQL Connection Error
**Symptom:** `psycopg2.OperationalError: could not connect to server: Connection refused`  
**Cause:** `DATABASE_URL` is configured in `.env`, but the PostgreSQL server service is stopped or port 5432 is unreachable.  
**Resolution:**
- If PostgreSQL is not running locally, comment out or leave `DATABASE_URL=` empty in `.env`.
- CareerPilot will automatically fall back to the built-in SQLite database (`db.sqlite3`), requiring zero configuration.

---

## 3. PowerShell Execution Policy Restriction
**Symptom:** `.\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`  
**Resolution:**
Run scripts in your current session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Or directly invoke Python without activating the virtual environment:
```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

---

## 4. Resetting or Reloading Sample Data
**Command:**
```powershell
# Reset demonstration data:
.\.venv\Scripts\python.exe manage.py load_sample_data --clear

# Re-populate fresh sample data:
.\.venv\Scripts\python.exe manage.py load_sample_data
```
