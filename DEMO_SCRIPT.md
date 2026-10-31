# CareerPilot — 90-Second Demonstration Script

Use this structured walkthrough to demonstrate **CareerPilot** in portfolio reviews, recruiter interviews, or hackathons.

---

## 1. Quick Start (5 Seconds)
1. Launch the application:
   ```powershell
   .\run.bat
   ```
2. Navigate to `http://127.0.0.1:8000/`.
3. Sign in using the pre-seeded demo candidate account:
   - **Username:** `demo_user`
   - **Password:** `DemoPassword123!`

---

## 2. Command Center Overview (20 Seconds)
- **Top Context Bar:** Shows candidate name, current date, and active interview rounds.
- **KPI Metrics:** Point out *Opportunities Saved*, *Active Applications*, *Upcoming Interviews*, and *Offer Conversion Rate (honest conversion metrics)*.
- **Charts:** Highlight the *Application Pipeline Distribution* and *Monthly Activity Trends* (Applications vs. Interviews).
- **Rule-Based Recommendations:** Point out transparent alerts (e.g. *Interview Scheduled Tomorrow for Razorpay*, *Overdue Follow-up for Zoho*).

---

## 3. Dedicated "My Day" Daily Planner (15 Seconds)
- Click **My Day** in the sidebar.
- Show the daily goal progress bar calculated from real records.
- Demonstrate checking off a task (e.g., *"Solve 3 Dynamic Programming problems"*): the task smoothly strikes through and persists via AJAX without full page reload.
- Review immediate 48-hour interview alerts and overdue recruiter follow-ups.

---

## 4. Opportunity Discovery & Duplicate Prevention (15 Seconds)
- Click **All Opportunities**.
- Point out real-time search, category dropdown filters, and salary ranges.
- Click **+ Add Opportunity**: type company *"Google India"* and title *"Software Engineering Intern"*. Point out the real-time duplicate warning alert warning the candidate that this role was already saved.

---

## 5. Interactive 10-Stage Pipeline Kanban Board (20 Seconds)
- Click **Pipeline (Kanban)** under Applications.
- Show the 10 defined stages: *Saved, Interested, Applied, Assessment, Tech Interview, HR Interview, Offer Received, Accepted, Rejected, Withdrawn*.
- Drag an application card or use the quick stage dropdown (e.g., advance an assessment to *"Technical Interview"*).
- Click into the application to show that **ApplicationStatusHistory** automatically logged the previous status, new status, timestamp, and transition note without overwriting history.

---

## 6. Interview Preparation & Questions Archive (10 Seconds)
- Click into an interview round (e.g., *Razorpay Technical Round 1*).
- Show the **Preparation Checklist**: check off items to watch the progress bar dynamically recalculate.
- Navigate to **Preparation Notes**: show the searchable archive of real technical questions asked, algorithms used, and areas to improve from past rounds.

---

## 7. Reports & Data Exports (10 Seconds)
- Click **Reports & Exports**.
- Download **Excel (.xlsx)** or **CSV** of active applications.
- Emphasize that all exports are strictly user-isolated with zero cross-tenant data leakage.
- Click the **Theme Toggle** icon in the header to showcase the deep charcoal dark workspace mode.
