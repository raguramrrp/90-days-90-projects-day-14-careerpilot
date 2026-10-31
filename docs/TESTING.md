# CareerPilot — Automated Testing & Quality Assurance

## 1. Test Suite Overview
CareerPilot includes an end-to-end automated test suite covering all core business domains, security boundaries, and user isolation constraints.

Total tests implemented: **32 tests**  
Test result: **32 passed (100% PASS, 0 failures, 0 errors)**

---

## 2. Test Coverage Breakdown

| Test Module | Test Class / Scope | Key Verifications | Result |
|-------------|-------------------|-------------------|--------|
| `test_auth.py` | `AuthTests` | User registration, login, logout, unauthorized redirection, profile updates | **PASS** |
| `test_opportunities.py` | `OpportunityTests` | Create opportunity, edit, delete, search query filtering, category filters, duplicate check API | **PASS** |
| `test_applications.py` | `ApplicationTests` | Application tracking, initial history logging, status transition via AJAX API, Kanban board rendering | **PASS** |
| `test_interviews.py` | `InterviewTests` | Round creation, automatic checklist item seeding, checklist toggle API, retrospective archive view | **PASS** |
| `test_reminders.py` | `ReminderTests` | Reminder creation, completion toggle API, overdue date detection | **PASS** |
| `test_documents.py` | `DocumentTests` | File upload validation, format checking, rejection of dangerous extensions (.exe), secure download | **PASS** |
| `test_planner.py` | `PlannerTests` | Daily task creation, task completion toggle API, real database goal progress calculation | **PASS** |
| `test_analytics.py` | `AnalyticsTests` | KPI metric calculations, honest conversion formulas, 10 chart structures, rule-based recommendation engine | **PASS** |
| `test_reports.py` | `ReportTests` | CSV application export, Excel (.xlsx) export with openpyxl/pandas | **PASS** |
| `test_user_isolation.py` | `UserIsolationTests` | Cross-tenant data isolation: User B cannot view, edit, download, or export User A's data | **PASS** |

---

## 3. How to Execute the Tests

### Via Windows Command:
```cmd
test.bat
```

### Via PowerShell / Python:
```powershell
.\.venv\Scripts\python.exe manage.py test tests --verbosity=2
```
