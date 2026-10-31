# CareerPilot — Intelligent Career & Job Application Management System

> **Day 14 of the 90 Days – 90 Projects Challenge**  
> *Developed by Ragu Ram P — Final-Year B.Tech Artificial Intelligence & Data Science Student*

![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=flat&logo=postgresql&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-FF6384?style=flat&logo=chartdotjs&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-34%20Passed%20(100%25)-16856B?style=flat)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)

---

## 1. Project Overview & Motivation

Searching for internships and full-time software engineering roles is often chaotic: opportunities are scattered across spreadsheets, notes, chat threads, and emails. Candidates frequently miss critical application deadlines, forget to follow up with recruiters, lose track of which customized resume version was submitted to which employer, and enter technical interviews without structured preparation or feedback notes.

**CareerPilot** is an intelligent, centralized personal career workspace and job-application CRM designed specifically for students, fresh graduates, and active job seekers. It eliminates scattered spreadsheets and manual reminders by providing:
- Structured pre-application opportunity tracking with real-time duplicate detection.
- A 10-stage interactive application pipeline (Table and Kanban views) with an automatic, non-destructive audit history.
- A focused **"My Day"** daily career operating system tracking urgent follow-ups, habit milestones, and immediate 48-hour interview rounds.
- Multi-round interview management equipped with interactive 8-step prep checklists and a past-interview technical questions retrospective archive.
- Tailored resume and document management ensuring candidates know exactly which CV version was provided to each employer.
- 10 real-time analytics charts and filterable Excel/CSV data exports with strict tenant-level user data isolation.

---

## 2. Intended Users & Daily Workflow

CareerPilot is built for:
- **Final-Year Students & Fresh Graduates:** Managing campus recruitment drives, off-campus referrals, and competitive coding milestones.
- **Internship & Co-op Seekers:** Juggling multiple fast-moving recruitment cycles and assessment deadlines.
- **Active Software Engineers:** Organizing career transitions, target compensation bands, and multi-round technical interviews.

### The CareerPilot Core Workflow:
```
Open CareerPilot → Understand today's priorities ("My Day") → Take action → 
Update application pipeline → Prepare for interview with interactive checklists → 
Record round feedback → Track weekly goal progress → Refine application strategy.
```

---

## 3. Key Features by Module

### Module A — User Authentication & Profile
- Full authentication lifecycle: Registration, Login, Logout, and Password Change.
- Comprehensive candidate profile: Target roles, preferred work modes (*Remote, Hybrid, On-site*), employment types, target compensation, technical skill pills, and career goals.
- Custom follow-up configuration (user-defined default interval, e.g. 7 days).
- Theme persistence (Light and Dark modes).

### Module B — Opportunity Management
- Save and evaluate opportunities prior to applying.
- Company details, job titles, descriptions, salary ranges, required skills, and direct portal links.
- Real-time client-side and server-side **duplicate opportunity detection** preventing accidental duplicate outreach.
- Interest statuses: *Saved, Interested, Not Interested, Archived*.

### Module C — 10-Stage Application Pipeline
- Connects directly to saved opportunities.
- **10 Application Stages:**
  1. `Saved` &bull; 2. `Interested` &bull; 3. `Applied` &bull; 4. `Assessment` &bull; 5. `Technical Interview` &bull; 6. `HR Interview` &bull; 7. `Offer Received` &bull; 8. `Accepted` &bull; 9. `Rejected` &bull; 10. `Withdrawn`
- **Dual Pipeline Views:** High-density data table view and drag-and-drop Kanban board.
- **Application Status History:** Automatically logs previous stage, new stage, timestamp, and transition notes without overwriting past history.

### Module D — Reminders & Follow-up Center
- Tracks 7 reminder types: *Application follow-up, Interview reminder, Assessment deadline, Job application deadline, Recruiter follow-up, Document submission, Custom reminder*.
- Tabbed views: *Upcoming, Today, Overdue, Completed, All*.
- In-app notification bell in top navigation displaying pending and overdue counts.
- Real-time AJAX checkbox toggling.

### Module E — Interview Management & Preparation Checklists
- Supports multiple rounds per employer (Coding, System Design, Behavioral, Bar Raiser).
- Automatically seeds an interactive **8-step preparation checklist** with dynamic percentage progress.
- Post-interview retrospective archive storing questions asked, algorithms used, and areas for improvement.

### Module F — Resume & Document Manager
- Upload and manage resumes categorized by target specialization (*Software Engineer, Python Developer, Data Analyst, General*).
- Validates file extensions (`.pdf`, `.docx`, `.doc`, `.txt`) and restricts uploads to 5 MB.
- Documents are served through protected views enforcing strict user ownership (HTTP 404 on unauthorized access attempts).
- Tracks and displays which resume version was submitted to each application.

### Module G — Daily Career Operating System ("My Day")
- Dedicated morning command view summarizing:
  - Overdue and today's priority tasks.
  - Interviews scheduled in the next 48 hours.
  - Recruiter follow-ups that have surpassed their target dates.
  - Active assessments currently in progress.
  - Daily and weekly target goal progress bars calculated from database records.

### Module H — Interactive Schedule Calendar
- Displays application deadlines, interview rounds, reminders, and career tasks with distinct restrained visual indicators.
- Toggle between Month, Week, and Day Agenda views.

### Module I — Career Analytics Dashboard
- Calculated exclusively from real database records (no hard-coded or fabricated metrics).
- **10 Responsive Visual Charts:**
  1. Applications by Month &bull; 2. Pipeline Stage Distribution &bull; 3. Applications by Job Category &bull; 4. Employment Type Breakdown &bull; 5. Work Mode Breakdown &bull; 6. Discovery Source Yield &bull; 7. Interview Outcomes &bull; 8. Monthly Activity Trends &bull; 9. Offer Conversion Funnel &bull; 10. Pipeline Health Ratio.
- Plain-language strategy insights highlighting top discovery channels and conversion bottlenecks.

### Module J — Rule-Based Career Recommendations
- Transparent recommendations derived deterministically from candidate records:
  - Application deadlines approaching within 3 days.
  - Interviews scheduled today or tomorrow.
  - Overdue recruiter follow-up targets.
  - Unanswered applications surpassing the candidate's configured follow-up threshold.
  - Saved opportunities matching preferred job roles in the candidate's profile.
  - Same-day interview scheduling conflict warnings.

### Module K — Filterable Reports & Data Exports
- On-demand exports in CSV and Microsoft Excel (`.xlsx`) formats.
- Pre-filtered exports for Applications, Opportunities, and Interview logs.
- Strict multi-tenant isolation guaranteeing zero cross-user data leakage.

---

## 4. UI/UX Design System: Professional Editorial Workspace

CareerPilot intentionally avoids generic templates, purple gradients, and neon animations. The interface follows the visual discipline of modern enterprise productivity tools:
- **Palette:**
  - Base Application Background: `#F5F7FA`
  - Sidebar & Surface: `#FFFFFF`
  - Primary Typography: `#172B4D`
  - Secondary Supporting Text: `#66758A`
  - Primary Accent: `#2869C7` (Restrained Enterprise Blue)
  - Success: `#16856B` | Warning: `#C58A25` | Danger: `#C74E58`
- **Dark Theme:** Deep slate/charcoal tones (`#0F172A` / `#1E293B`) maintaining strict WCAG contrast and readability.
- **Iconography:** Small monochrome SVG line icons. Zero emojis anywhere in the interface.

---

## 5. System Architecture

```mermaid
flowchart TD
    Candidate([Candidate / User]) --> Auth[Django Authentication & Session Layer]
    Auth --> Guard[Tenant-Level User Ownership Verification]
    
    subgraph UI [Enterprise Workspace UI]
        Templates[Django Templates + Inter Font]
        CSS[Restrained CSS Design System]
        JS[Main.js / Kanban.js / Calendar.js / Chart.js]
    end
    
    subgraph Modules [Application Core Logic]
        Opps[Opportunity Discovery & Duplicate Checker]
        Pipeline[10-Stage Pipeline & History Logger]
        Interview[Interview Round & Checklist Manager]
        MyDay[Daily Planner & Goal Calculator]
        Docs[Secure Resume & Document Storage]
        Analytics[10 Visual Charts & Recommendation Engine]
        Exports[CSV & OpenPyXL Excel Exporter]
    end
    
    subgraph Database [Persistence Engine]
        Postgres[(PostgreSQL Primary / SQLite Local Fallback)]
    end
    
    Guard --> Modules
    Modules --> UI
    Modules --> Database
```

---

## 6. Database Schema (Entity-Relationship Diagram)

```mermaid
erDiagram
    User ||--o{ UserProfile : has
    User ||--o{ Company : owns
    User ||--o{ Opportunity : tracks
    User ||--o{ Application : submits
    User ||--o{ Interview : attends
    User ||--o{ Reminder : configures
    User ||--o{ Document : stores
    User ||--o{ CareerTask : executes
    User ||--o{ CareerGoal : targets

    Company ||--o{ Opportunity : offers
    Opportunity ||--o{ Application : receives
    Opportunity ||--o{ Reminder : links
    Opportunity ||--o{ CareerTask : references

    Application ||--o{ ApplicationStatusHistory : records
    Application ||--o{ ApplicationNote : logs
    Application ||--o{ Interview : schedules
    Application ||--o{ Reminder : triggers
    Application ||--o{ CareerTask : spawns
    Application }o--o| Document : submits_resume

    Interview ||--o{ InterviewChecklistItem : requires
```

---

## 7. Technology Stack

- **Backend Framework:** Python 3.12, Django 5.1 (ORM, Auth, Forms, Messages)
- **Database:** PostgreSQL (primary target via `psycopg2` & `DATABASE_URL`); SQLite (automatic zero-setup local fallback)
- **Frontend:** Django Templates, HTML5, CSS3 Custom Properties, Vanilla JavaScript (ES6+)
- **Visualization:** Chart.js 4.4 (10 responsive charts with full offline resilience)
- **Data Processing & Export:** Pandas, OpenPyXL (Excel `.xlsx` generation), Python `csv`
- **File Handling:** Pillow, Django File Storage with extension and size validation
- **Testing:** Django TestCase (34 automated unit, integration, and security tests)

---

## 8. Project Structure

```
90-days-90-projects-day-14-careerpilot/
├── manage.py
├── setup.bat                     # Windows 1-click automated setup
├── run.bat                       # Windows server startup script
├── test.bat                      # Windows automated test runner
├── requirements.txt              # Pinned Python dependencies
├── pyproject.toml                # Project metadata & pytest configuration
├── LICENSE                       # MIT License
├── README.md                     # Recruiter-facing documentation
├── QUICKSTART.md                 # Fast setup reference
├── DEMO_SCRIPT.md                # 90-second portfolio presentation script
├── .env.example                  # Environment template
├── .gitignore
├── config/                       # Project configuration & settings
│   ├── settings.py               # Database URL parser, security & apps
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                     # Candidate profiles & preferences
├── opportunities/                # Opportunities & duplicate prevention
├── applications/                 # 10-stage pipeline, Kanban & history
├── interviews/                   # Multi-round interviews & prep checklists
├── reminders/                    # Follow-up center & notification bell
├── documents/                    # Resume versions & document store
├── planner/                      # Daily tasks & weekly goals
├── analytics/                    # 10 Chart.js charts & recommendation engine
├── reports/                      # Excel & CSV report exporters
├── core/                         # Dashboard, My Day, Calendar & search
│   ├── context_processors.py     # Global notification count & theme
│   ├── views.py
│   └── management/commands/
│       └── load_sample_data.py   # Demonstration data loader
├── templates/                    # Semantic Django templates
│   ├── base.html
│   ├── partials/
│   │   ├── sidebar.html
│   │   ├── header.html
│   │   └── messages.html
│   ├── accounts/
│   ├── core/
│   ├── opportunities/
│   ├── applications/
│   ├── interviews/
│   ├── reminders/
│   ├── documents/
│   ├── planner/
│   ├── analytics/
│   └── reports/
├── static/
│   ├── css/main.css              # Editorial Workspace CSS design system
│   └── js/
│       ├── main.js               # Theme, AJAX toggles, hotkeys
│       ├── kanban.js             # Drag-and-drop pipeline engine
│       └── calendar.js           # Multi-view schedule renderer
├── media/                        # User uploaded documents & resumes
├── docs/                         # In-depth architectural documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPMENT_NOTES.md
│   ├── TESTING.md
│   └── TROUBLESHOOTING.md
├── data/
│   └── README.md
├── screenshots/
│   └── README.md                 # UI preview capture guide
└── tests/                        # Comprehensive 32-test automated suite
    ├── test_auth.py
    ├── test_opportunities.py
    ├── test_applications.py
    ├── test_interviews.py
    ├── test_reminders.py
    ├── test_documents.py
    ├── test_planner.py
    ├── test_analytics.py
    ├── test_reports.py
    └── test_user_isolation.py
```

---

## 9. Windows Installation & Setup Guide

### Prerequisites
- Windows 10 or 11
- Python 3.10+ (Python 3.12 recommended)
- PostgreSQL (Optional: SQLite is used automatically if PostgreSQL is not active)

### Step 1: Clone or Navigate to the Project
```powershell
cd "D:\90 days\90-days-90-projects-day-14-careerpilot"
```

### Step 2: Run Automated Windows Setup
Execute `setup.bat` by double-clicking it in File Explorer or running in PowerShell:
```cmd
.\setup.bat
```
This script automatically:
1. Detects Python 3.12 / 3.10+.
2. Creates the `.venv` virtual environment.
3. Installs dependencies from `requirements.txt`.
4. Copies `.env.example` to `.env`.
5. Applies all database migrations.
6. Seeds the demonstration candidate account (`demo_user`).

### Step 3: Start the Application
```cmd
.\run.bat
```
Open your browser and navigate to:
`http://127.0.0.1:8000/`

---

## 10. Demonstration Credentials

A fully populated candidate workspace is provided for immediate demonstration:
- **Demo Candidate Account:** `demo_user` / `DemoPassword123!`
- **Administrator / Superuser Account:** `admin` / `AdminPassword123!` (Access Django Admin at `http://127.0.0.1:8000/admin/`)

---

## 11. PostgreSQL Configuration

To connect CareerPilot to a production or local PostgreSQL database:
1. Open `.env` in the project root.
2. Provide your connection string in `DATABASE_URL`:
   ```ini
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/careerpilot
   ```
3. Run migrations:
   ```powershell
   .\.venv\Scripts\python.exe manage.py migrate
   ```

*If `DATABASE_URL` is left blank, CareerPilot automatically defaults to local `db.sqlite3` with zero setup required.*

---

## 12. Automated Testing Status

The test suite thoroughly verifies authentication, forms, business logic, multi-stage state transitions, file security, and cross-tenant user isolation.

```cmd
.\test.bat
```

### Actual Test Execution Output:
```
Found 34 test(s).
System check identified no issues (0 silenced).
..................................
----------------------------------------------------------------------
Ran 34 tests in 18.600s

OK
```
**Status: 34/34 PASSED (100% PASS RATE)**

---

## 13. Security & Data Protection

- **Tenant-Level Isolation:** All database selectors filter strictly by `user=request.user`. User B receives an HTTP 404 when attempting to access User A's applications, interviews, documents, or exports.
- **Protected File Downloads:** Document files are never exposed through predictable public static URLs. File streaming endpoints verify user ownership before transmitting bytes.
- **File Validation:** Uploads are restricted to 5 MB and checked against a strict whitelist of safe extensions (`.pdf`, `.docx`, `.doc`, `.txt`, `.png`, `.jpg`).
- **CSRF & Form Validation:** Django CSRF tokens are enforced on all POST forms and AJAX requests.
- **Environment Confidentiality:** Database credentials and secret keys are loaded from `.env` and excluded from version control.

---



## 14. License & Attribution

This project is open-source software licensed under the [MIT License](LICENSE).  
Developed as part of the **90 Days – 90 Projects Challenge** by **Ragu Ram P**.
