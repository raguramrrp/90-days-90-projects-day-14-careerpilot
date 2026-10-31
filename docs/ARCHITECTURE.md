# CareerPilot — System Architecture & Data Model

## 1. Architectural Design
CareerPilot is architected as a modular Django web application following strict Domain-Driven Design principles, full user data isolation, and a professional enterprise UI design system.

```mermaid
flowchart TD
    User([Candidate / User]) --> AuthMiddleware[Django Auth & Session Middleware]
    AuthMiddleware --> IsolationCheck[Tenant-Level User Ownership Verification]
    
    subgraph Frontend [Presentation Layer]
        UI[Django Templates + Inter Typography]
        CSS[Restrained Enterprise CSS Palette]
        JS[Main.js / Kanban.js / Calendar.js / Chart.js]
    end
    
    subgraph Core [Business Logic & Service Layer]
        OppsModule[Opportunity Engine & Duplicate Checker]
        PipelineModule[10-Stage Pipeline & History Logger]
        InterviewModule[Multi-Round Interview & Checklist Engine]
        PlannerModule[Daily Tasks & Weekly Goal Tracker]
        DocModule[Secure Document Storage & Downloader]
        AnalyticsModule[10 KPI Visualizers & Recommendation Engine]
        ReportModule[Pandas CSV & Excel Exporter]
    end
    
    subgraph Persistence [Database Layer]
        DB[(PostgreSQL Primary / SQLite Local Fallback)]
    end
    
    IsolationCheck --> Core
    Core --> Frontend
    Core --> Persistence
```

---

## 2. Entity-Relationship (ER) Diagram

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

## 3. Application Pipeline State Machine

Applications progress through 10 distinct stages. Any transition triggers an automatic `ApplicationStatusHistory` event with timestamp and transition notes:

```mermaid
stateDiagram-v2
    [*] --> Saved
    Saved --> Interested
    Interested --> Applied
    Applied --> Assessment
    Assessment --> Technical_Interview
    Technical_Interview --> HR_Interview
    HR_Interview --> Offer_Received
    Offer_Received --> Accepted
    
    Applied --> Rejected
    Assessment --> Rejected
    Technical_Interview --> Rejected
    HR_Interview --> Rejected
    
    Saved --> Withdrawn
    Interested --> Withdrawn
    Applied --> Withdrawn
    Assessment --> Withdrawn
    Technical_Interview --> Withdrawn
    HR_Interview --> Withdrawn
    Offer_Received --> Withdrawn

    Accepted --> [*]
    Rejected --> [*]
    Withdrawn --> [*]
```
