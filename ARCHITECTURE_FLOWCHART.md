# 🗺️ TVET Assessment System - User Flow & Architecture

## 📊 Complete User Journey

### Registration & Login Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Home Page (/home)                        │
│                   [Register] [Login]                        │
└─────────────────────────────────────────────────────────────┘
        │                                    │
        │ Click Register                     │ Click Login
        ▼                                    ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│  Registration Page       │    │   Login Page                 │
│  (/register)             │    │   (/login)                   │
│  - Name                  │    │   - Name                     │
│  - Roll No               │    │   - Email                    │
│  - Email                 │    │   - Registration Code        │
│  - Password              │    └──────────────────────────────┘
│  - Mode (FYP/JOB)        │            │
│                          │            │ Valid Credentials
└──────────────────────────┘            │
        │                               ▼
        │ Success                  ┌────────────────────────────┐
        │                          │  Session Created           │
        ▼                          │  - student_id set          │
┌──────────────────────────┐      │  - student_name set        │
│ Registration Success     │      │  - mode set                │
│ Display Code             │      └────────────────────────────┘
└──────────────────────────┘              │
                                          ▼
                                    ┌─────────────────────────────┐
                                    │ QUESTIONNAIRE HOME (NEW!)   │
                                    │ /questionnaire_home         │
                                    │                             │
                                    │ [📚 FYP] [💼 JOB]          │
                                    └─────────────────────────────┘
                                         │           │
                     Click FYP           │           │  Click JOB
                                         ▼           ▼
                              Path Selection Completed
```

---

## 🎯 Assessment Flow (FYP Example)

```
┌──────────────────────────────────────────────────────────────┐
│         Questionnaire Home (questionnaire_home.html)         │
│                                                              │
│     ┌──────────────────────────┐  ┌──────────────────────┐  │
│     │     📚 FYP PATH          │  │     💼 JOB PATH      │  │
│     │ Research-oriented eval   │  │ Industry-ready eval  │  │
│     │ ✓ Project-based          │  │ ✓ Practical aptitude │  │
│     │ ✓ Academic skills        │  │ ✓ Employment ready   │  │
│     │ ✓ Innovation analysis    │  │ ✓ Career guidance    │  │
│     │  [Start FYP →]           │  │  [Start JOB →]       │  │
│     └──────────────────────────┘  └──────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                         │
                         │ Click "Start FYP"
                         ▼
         ┌────────────────────────────────────────┐
         │   FYP Questionnaire (questionnaire.html) │
         │                                         │
         │  Header:                                │
         │  ┌─────────────────────────────────┐   │
         │  │ FYP Assessment                  │   │
         │  │ Progress: 5/50                  │   │
         │  │ Time: 43:25                     │   │
         │  │ [Progress Bar: ████░░░░]        │   │
         │  └─────────────────────────────────┘   │
         │                                         │
         │  Questions:                             │
         │  Q1. Question text here?                │
         │      ◯ Option A                        │
         │      ◯ Option B                        │
         │      ◯ Option C                        │
         │      ...                               │
         │                                         │
         │  Q2. Another question?                 │
         │      ◯ Option A                        │
         │      ◯ Option B                        │
         │      ...                               │
         │                                         │
         │  [← Back] [Submit Assessment ✓]        │
         └────────────────────────────────────────┘
                  │                    │
    Answer all    │                    │ Click Submit
    questions     │                    ▼
                  │        ┌──────────────────────────┐
                  │        │  Backend Processing      │
                  │        │  - Collect answers       │
                  │        │  - Calculate scores      │
                  │        │  - Update DB             │
                  │        │  - Send email            │
                  │        └──────────────────────────┘
                  │                    │
                  └────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────────────┐
         │         Dashboard (dashboard.html)      │
         │  ✅ SUCCESS - Results Submitted!       │
         │                                         │
         │  Student: John Doe (SE-1001)            │
         │  Email: john@email.com                 │
         │  Roll: 1001                            │
         │                                         │
         │  📊 Assessment Progress:                │
         │                                         │
         │  📚 FYP Assessment                      │
         │     Status: ✓ COMPLETED                │
         │     Score: 78.5/100                    │
         │     Completed: 2026-03-20 14:30:45     │
         │     [Progress: ████████████]           │
         │                                         │
         │  💼 JOB Assessment                      │
         │     Status: ⏳ PENDING                  │
         │     [Progress: ░░░░░░░░░░]             │
         │                                         │
         │  ⚡ Quick Actions:                      │
         │     [📚 View FYP Results]               │
         │     [💼 Start JOB Assessment]           │
         │                                         │
         │  📈 Summary:                            │
         │     Assessments Completed: 1/2         │
         │     FYP Score: 78.5                    │
         │     Next Step: Complete JOB Assessment │
         │                                         │
         │  [← Back to Tests] [Logout]             │
         └────────────────────────────────────────┘
                          │
    Continue to JOB?      │
                          │
                          ▼
         ┌────────────────────────────────────────┐
         │  Back to Questionnaire Home             │
         │  [📚 View FYP Results] [💼 Start JOB] │
         │                                         │
         │  Click "Start JOB Assessment"           │
         │           │                             │
         │           ▼ (Same flow as FYP)         │
         │  JOB Questionnaire Form                │
         │  Answer all questions → Submit         │
         │           │                             │
         │           ▼                             │
         │  Update Dashboard                      │
         │  Both FYP & JOB completed              │
         │  Compare scores                        │
         └────────────────────────────────────────┘
```

---

## 🔄 Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Frontend)                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │  Register  │  │   Login    │  │ Dashboard  │             │
│  │  Template  │  │  Template  │  │  Template  │             │
│  └────────────┘  └────────────┘  └────────────┘             │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        ││
│  │  │Question.   │  │Questionnaire│ │Dashboard   │        ││
│  │  │Home Template│  │Template     │ │Template    │        ││
│  │  └────────────┘  └────────────┘  └────────────┘        ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
         │                                    │
         │ HTTP Requests                      │ Display
         │                                    │
         ▼                                    ▼
┌──────────────────────────────────────────────────────────────┐
│              FLASK APPLICATION (Backend Routes)              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  /register      → register_student_web()              │ │
│  │  /login         → login_student_web_with_code()       │ │
│  │  /questionnaire_home → render questionnaire_home      │ │
│  │  /questionnaire/<path> → render questionnaire form    │ │
│  │  /submit_questionnaire → process responses            │ │
│  │  /dashboard     → render dashboard with progress      │ │
│  │  /api/student_progress → return JSON progress        │ │
│  │  /logout        → clear session                       │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
         │                                    │
         │                                    │
         ▼                                    ▼
┌──────────────────────────────────────────────────────────────┐
│           BACKEND LOGIC (backend_logic.py)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Core Functions:                                       │ │
│  │  - register_student_web()                              │ │
│  │  - login_student_web_with_code()                       │ │
│  │  - load_questions(mode)                                │ │
│  │  - compute_scores(df)                                  │ │
│  │  - compute_tvet_index(scores)                          │ │
│  │                                                        │ │
│  │  NEW Functions:                                        │ │
│  │  - get_student_progress(student_id)                    │ │
│  │  - update_questionnaire_status()                       │ │
│  │  - init_questionnaire_progress_db()                    │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
         │                                    │
         │                                    │
         ▼                                    ▼
┌──────────────────────────────────────────────────────────────┐
│              DATA STORAGE (CSV Files)                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  PRIMARY DATA:                                          ││
│  │  - users_db.csv          (Student registrations)      ││
│  │  - fyp_results.csv        (FYP responses)              ││
│  │  - job_results.csv        (JOB responses)              ││
│  │  - score_summaries.csv    (Final scores)               ││
│  │                                                        ││
│  │  NEW DATA:                                             ││
│  │  - questionnaire_progress.csv (Progress tracking)      ││
│  │                                                        ││
│  │  QUESTION DATA:                                        ││
│  │  - full_question_bank_with_responses.csv               ││
│  └─────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 Database Relationships

```
┌──────────────────────────┐
│      users_db.csv        │
├──────────────────────────┤
│ student_id (PK)          │◄─┐
│ roll_no                  │  │
│ name                     │  │
│ email                    │  │
│ mode (FYP/JOB)           │  │
│ password                 │  │
│ registration_code        │  │
└──────────────────────────┘  │
                              │
                              │ 1:1 Relationship
                              │
                    ┌─────────┴────────┐
                    │                  │
                    ▼                  ▼
    ┌──────────────────────────┐  ┌──────────────────────────┐
    │  fyp_results.csv         │  │  job_results.csv         │
    ├──────────────────────────┤  ├──────────────────────────┤
    │ student_id               │  │ student_id               │
    │ question_id              │  │ question_id              │
    │ section                  │  │ section                  │
    │ answer (1-5)             │  │ answer (1-5)             │
    │ timestamp                │  │ timestamp                │
    └──────────────────────────┘  └──────────────────────────┘
                                            │
                                            │
                                            ▼
                              ┌──────────────────────────┐
                              │ score_summaries.csv      │
                              ├──────────────────────────┤
                              │ student_id (FK)          │
                              │ mode (FYP/JOB)           │
                              │ tvet_index               │
                              │ tvet_label               │
                              │ recommended_domain       │
                              │ domain_scores            │
                              └──────────────────────────┘
                                            │
                                            │
                  ┌─────────────────────────┴──────────────────┐
                  │                                            │
                  ▼                                            ▼
    ┌──────────────────────────┐  ┌──────────────────────────┐
    │questionnaire_progress.csv│  │ (Auto-generated)         │
    ├──────────────────────────┤  ├──────────────────────────┤
    │ student_id (FK)          │  │ Links to user via        │
    │ fyp_completed (Bool)     │  │ student_id               │
    │ job_completed (Bool)     │  │                          │
    │ fyp_completion_date      │  │ Tracks both FYP & JOB   │
    │ job_completion_date      │  │ completion status        │
    │ fyp_score (Float)        │  │                          │
    │ job_score (Float)        │  │                          │
    └──────────────────────────┘  └──────────────────────────┘
```

---

## 📡 Session & State Management

```
┌────────────────────────────────────────┐
│        LOGIN SUCCESSFUL                │
└────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│      SESSION CREATED & STORED          │
│                                        │
│  session = {                           │
│    'student_id': 'SE-1001',            │
│    'student_name': 'John Doe',        │
│    'mode': 'FYP',                      │
│    'session_token': 'abc123...',       │
│    'submission_code': (optional)       │
│  }                                     │
└────────────────────────────────────────┘
           │
    Maintained across requests
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
    ▼             ▼              ▼
FYP Path     Dashboard      Logout
    │             │              │
    └──────┬──────┴────┬─────────┘
           │           │
           ▼           ▼
    ┌─────────────────────────────┐
    │  SESSION CLEARED            │
    │  (on logout or expiration)  │
    └─────────────────────────────┘
```

---

## 🔐 Security & Validation Flow

```
┌─────────────────────────────────────┐
│    INCOMING REQUEST                 │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  CHECK AUTHENTICATION               │
│  (session['student_id'] exists?)    │
├─────────────────────────────────────┤
│  NO ──────→ Redirect to /login      │
│  YES ──────→ Continue               │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  VALIDATE REQUEST PARAMETERS        │
│  (path, student_id, etc.)           │
├─────────────────────────────────────┤
│  INVALID ──→ Show error message     │
│  VALID ─────→ Continue              │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  PROCESS REQUEST                    │
│  - Load data                        │
│  - Calculate results                │
│  - Update database                  │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  RETURN RESPONSE                    │
│  - Render template                  │
│  - Redirect or JSON                 │
└─────────────────────────────────────┘
```

---

## 📊 Progress Tracking Flow

```
┌─────────────────────────────────┐
│  Student Starts FYP             │
│  /questionnaire/fyp             │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Load Questions                 │
│  Display Form                   │
│  Timer Starts (45 min)          │
└─────────────────────────────────┘
           │
    Student answering...
           │
           ▼
┌─────────────────────────────────┐
│  All Questions Answered         │
│  Submit Form                    │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Backend Processing:            │
│  1. Collect responses           │
│  2. Save to fyp_results.csv     │
│  3. Calculate scores            │
│  4. Compute TVET index          │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Update Progress Database:      │
│  questionnaire_progress.csv     │
│  - Set fyp_completed = TRUE     │
│  - Set fyp_completion_date      │
│  - Set fyp_score                │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Send Email Notification        │
│  With Results PDF               │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Redirect to Dashboard          │
│  /dashboard                     │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Dashboard Displays:            │
│  - FYP: ✓ COMPLETED             │
│  - FYP Score: 78.5              │
│  - Completion: 2026-03-20 ...   │
│  - JOB: ⏳ PENDING              │
│                                 │
│  Option: Start JOB Assessment   │
└─────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

```
┌────────────────────────────────────────────────────────────┐
│                  PRODUCTION DEPLOYMENT                      │
└────────────────────────────────────────────────────────────┘
           │
    ┌──────┴──────┬──────────────┬──────────────┐
    │             │              │              │
    ▼             ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌────────────┐  ┌─────────┐
│ Flask   │  │ Python  │  │ CSV Files  │  │ Email   │
│ Server  │  │ Backend │  │ (Database) │  │ SMTP    │
└─────────┘  └─────────┘  └────────────┘  └─────────┘
    │             │              │              │
    └──────┬──────┴──────┬───────┴──────┬───────┘
           │             │              │
           ▼             ▼              ▼
       Routes       Functions      Data Storage
      (7 new)      (3 new)         (1 new CSV)
```

---

## ✅ Component Checklist

```
Frontend Templates:
├── ✅ questionnaire_home.html (Path selection)
├── ✅ questionnaire.html (Form with timer)
└── ✅ dashboard.html (Results & progress)

Backend Functions:
├── ✅ get_student_progress()
├── ✅ update_questionnaire_status()
└── ✅ init_questionnaire_progress_db()

Routes:
├── ✅ /questionnaire_home
├── ✅ /questionnaire/<path>
├── ✅ /submit_questionnaire
├── ✅ /dashboard
├── ✅ /api/student_progress
├── ✅ /logout
└── ✅ Updated /login

Database:
├── ✅ questionnaire_progress.csv (Schema)
└── ✅ Integration with existing CSV files

Documentation:
├── ✅ IMPLEMENTATION_GUIDE.md
├── ✅ QUICKSTART.md
├── ✅ CHANGELOG.md
└── ✅ IMPLEMENTATION_SUMMARY.md
```

---

**Architecture Diagram Version: 1.0**
**Last Updated: March 20, 2026**
**Status: Ready for Reference**
