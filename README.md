# 🎮 EduPlay - UnityLearn
### Gamified Learning Experience Platform

> A full-stack college project — Django REST Framework backend + pure HTML/CSS/JS frontend + Supabase PostgreSQL — covering 6 educational modules with gamification, simulations, analytics, and collaborative features.

---

## ✨ Features at a Glance

| Module | Description | Key Tech |
|--------|-------------|----------|
| 🎮 **Game-Based Learning** | Quizzes, XP, badges, leaderboards | Django, DRF, JWT |
| 🔬 **Interactive Simulations** | Physics/Chem/Bio/Math virtual labs | HTML5 Canvas, JS |
| 📚 **Adaptive Learning Paths** | Courses, enrollments, skill assessments | DRF ModelViewSet |
| 🤝 **Collaborative Learning** | Study groups, forum, peer reviews | Django Signals |
| 📊 **Performance Analytics** | Charts, heatmaps, weekly reports | Chart.js |
| ✍️ **Content Authoring** | Quiz builder, drafts, media library | DRF + JSONField |

---

## 🗂️ Project Structure

```
eduplay-unitylearn/
├── backend/                    # Django Backend
│   ├── eduplay/               # Core settings & URLs
│   │   ├── settings.py        # Supabase DB, JWT, CORS config
│   │   └── urls.py            # Main API router
│   ├── accounts/              # User auth, profiles, XP, badges
│   ├── gamebased/             # Quizzes, questions, scoring
│   ├── simulations/           # Virtual lab experiments
│   ├── learningpaths/         # Courses, lessons, enrollment
│   ├── collaborative/         # Groups, forum, peer review
│   ├── analytics/             # Activity logs, dashboard stats
│   ├── authoring/             # Content templates, quiz builder
│   ├── requirements.txt       # Python dependencies
│   └── manage.py
│
└── frontend/                  # HTML/CSS/JS Frontend
    ├── index.html             # Landing page
    ├── login.html             # Login (JWT + demo mode)
    ├── register.html          # Registration + password strength
    ├── dashboard.html         # Student command center
    ├── css/
    │   └── main.css           # Glassmorphism design system
    ├── js/
    │   ├── api.js             # Centralized API client + mock data
    │   ├── auth.js            # JWT auth helpers + toast system
    │   └── dashboard.js       # Dashboard logic
    └── pages/
        ├── game-learning.html  # Module 1 - Interactive quizzes
        ├── simulations.html    # Module 2 - Virtual labs
        ├── learning-paths.html # Module 3 - Course catalog
        ├── collaborative.html  # Module 4 - Study groups & forum
        ├── analytics.html      # Module 5 - Charts & progress
        └── authoring.html      # Module 6 - Content builder
```

---

## 🚀 Quick Start

### Option 1 — One-Click (Windows)
```
Double-click start.bat
```
This automatically creates a virtual environment, installs dependencies, runs migrations, and starts the server.

### Option 2 — Manual Setup

**Step 1: Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**Step 2: Configure Supabase**
1. Go to [supabase.com](https://supabase.com) and create a free project
2. Go to **Project Settings → Database → Connection pooling**
3. Edit `backend/eduplay/settings.py` and update the `DATABASES` block:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.YOUR_PROJECT_REF',    # ← paste yours
        'PASSWORD': 'YOUR_SUPABASE_PASSWORD',    # ← paste yours
        'HOST': 'aws-0-ap-south-1.pooler.supabase.com',
        'PORT': '6543',
    }
}
```

**Step 3: Migrate & Seed**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data          # loads demo data for all 6 modules
```

**Step 4: Create Admin**
```bash
python manage.py createsuperuser
```

**Step 5: Run Server**
```bash
python manage.py runserver
```

**Step 6: Open Frontend**
Open `frontend/index.html` directly in your browser — or use VS Code Live Server.

---

## 🔑 Demo Credentials

After running `seed_data`:

| Username | Password | Role |
|----------|----------|------|
| `admin` | `eduplay123` | Superuser |
| `alice_dev` | `eduplay123` | Student (Level 7) |
| `bob_learn` | `eduplay123` | Student (Level 4) |

> **No backend?** The frontend has full mock-data fallback. Click **"Quick Demo Login"** on the login page — everything works offline.

---

## 🌐 API Endpoints

```
Auth
  POST  /api/token/                   # Obtain JWT tokens
  POST  /api/token/refresh/           # Refresh access token

Accounts (Module 0 — Auth)
  POST  /api/accounts/register/       # Register user
  GET   /api/accounts/profile/        # Get user profile + XP
  GET   /api/accounts/leaderboard/    # Global XP leaderboard

Game-Based Learning (Module 1)
  GET   /api/gamebased/quizzes/       # List quizzes (filter by category)
  POST  /api/gamebased/quizzes/{id}/start/   # Start attempt
  POST  /api/gamebased/quizzes/{id}/submit/  # Submit & get score
  GET   /api/gamebased/leaderboard/   # Quiz leaderboard

Simulations (Module 2)
  GET   /api/simulations/             # List simulations
  POST  /api/simulations/{id}/start/  # Start simulation
  POST  /api/simulations/{id}/complete/ # Complete & earn XP

Learning Paths (Module 3)
  GET   /api/learningpaths/courses/   # Course catalog
  POST  /api/learningpaths/courses/{id}/enroll/  # Enroll
  GET   /api/learningpaths/my-enrollments/        # My courses

Collaborative (Module 4)
  GET   /api/collaborative/groups/    # Study groups
  POST  /api/collaborative/groups/{id}/join/  # Join group
  GET   /api/collaborative/forum/posts/        # Forum posts
  POST  /api/collaborative/forum/posts/{id}/like/ # Like post

Analytics (Module 5)
  GET   /api/analytics/dashboard/     # Full dashboard stats
  GET   /api/analytics/activity/      # Activity log
  GET   /api/analytics/performance/   # Subject-wise quiz scores

Authoring (Module 6)
  GET   /api/authoring/templates/     # Content templates
  POST  /api/authoring/quiz-builder/  # Create custom quiz
  POST  /api/authoring/quiz-builder/{id}/publish/  # Publish quiz
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3 (Glassmorphism), Vanilla JavaScript |
| Backend | Python 3.11, Django 5.x |
| REST API | Django REST Framework + SimpleJWT |
| Database | Supabase PostgreSQL (pg 15) |
| Charts | Chart.js 4 |
| Auth | JWT (Access + Refresh tokens) |

---

## 📸 Screenshots

| Page | Description |
|------|-------------|
| `index.html` | Animated landing page with particle canvas |
| `dashboard.html` | Student command center with XP counters |
| `pages/game-learning.html` | Interactive quiz modal with live timer |
| `pages/simulations.html` | Newton's Law, Ohm's Law, Pendulum, Cell Bio labs |
| `pages/analytics.html` | Chart.js visualizations + study heatmap |
| `pages/authoring.html` | Drag-and-drop quiz builder |

---

## 👨‍💻 Development Notes

- **CORS** is fully configured — frontend can call backend from any origin during development.
- **JWT tokens** are stored in `localStorage`. Refresh is automatic on 401.
- The `seed_data` command creates realistic data for all 6 modules.
- Admin panel is at `/admin/` — all models are registered.
- All API views use `IsAuthenticated` permissions.

---

## 📄 License

This project is for educational/college purposes.

---

*Built with ❤️ using Django + Vanilla JS — EduPlay UnityLearn © 2024*
