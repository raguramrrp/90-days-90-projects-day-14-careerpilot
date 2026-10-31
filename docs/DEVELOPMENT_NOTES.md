# CareerPilot — Development Notes & Implementation Decisions

## 1. Architectural Decisions

### A. Non-Vibe-Coded Design Philosophy
Rather than using generic modern landing page templates with purple gradients and floating cards, CareerPilot was intentionally built with the restrained visual discipline of high-density enterprise desktop tools:
- Palette: `#F5F7FA` base background, `#172B4D` primary text, `#66758A` secondary, `#2869C7` restrained enterprise blue accent.
- Strict rules: Zero emojis, zero artificial animated badges, and small monochrome SVG line icons.
- Inter typography with controlled scale and font weights.
- True dark mode using deep slate/charcoal tones (`#0F172A` / `#1E293B`).

### B. Database Strategy: PostgreSQL Primary with SQLite Zero-Setup Fallback
- PostgreSQL configuration is supported natively via `DATABASE_URL` (e.g. `postgresql://user:pass@host:5432/careerpilot`) or explicit `POSTGRES_DB` environment variables.
- To guarantee zero-friction local execution on Windows without requiring manual PostgreSQL service startup, Django automatically falls back to local `db.sqlite3` when `DATABASE_URL` is omitted.
- The schema is fully ANSI SQL compatible with unique constraints, indexes, and database transactions.

### C. Multi-Tenant User Isolation
Every model query is filtered by `user=request.user`. Views, AJAX endpoints, file download streaming views, and report generators enforce server-side ownership checks, returning HTTP 404 whenever a user attempts to access or modify records belonging to another candidate.

### D. Audit Logging for Application Stages
Application status history is stored in a dedicated `ApplicationStatusHistory` model. Whenever an application status is modified via forms, AJAX, or the Kanban board, a transition entry is recorded with previous status, new status, timestamp, and optional rationale notes, preventing overwrite of past state progressions.

### E. Rule-Based Recommendation Engine
Recommendations are derived deterministically from database records:
1. Approaching application deadlines (&le; 3 days).
2. Interviews scheduled today or tomorrow.
3. Unanswered applications surpassing the candidate's configured follow-up threshold.
4. Overdue recruiter follow-up dates.
5. Saved opportunities matching preferred job roles in the candidate's profile.
6. Same-day interview scheduling conflict warnings.
No paid external APIs or pseudo-AI outputs are used.
