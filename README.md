# Movie Recommendation System

A full-stack Movie Recommendation System that helps users discover movies through search, personalized recommendations, movie details, and ratings.

## Features

- Browse and search movies by title.
- View movie details and genres.
- Submit movie ratings.
- Get personalized movie recommendations.
- Provide popular movie recommendations for new users.
- User registration and login with JWT authentication.
- PostgreSQL database integration.
- REST APIs built with FastAPI.
- React-based frontend.
- Docker and Docker Compose configuration.

## Tech Stack

**Backend:** Python, FastAPI, Pydantic, SQLAlchemy

**Frontend:** React, Vite, JavaScript, CSS

**Database:** PostgreSQL (Neon)

**Machine Learning:** Python, Pandas, NumPy, Scikit-learn, Joblib

**Authentication:** JWT, password hashing

**Testing:** Pytest

**Deployment:** Render, Docker, Docker Compose

## Project Structure

```text
Movie-Recommendation-System/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── recommendation.py
│   ├── test_main.py
│   ├── Dockerfile
│   └── migrations/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── models/
│   └── recommender_model.joblib
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Manasa-Pandranki/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_database_url
DATABASE_URL_POOLED=your_pooled_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

Use your own database credentials and secret key. Never commit `.env` to GitHub.

### 5. Run the backend

```bash
python -m uvicorn backend.main:app --reload
```

Backend API: http://127.0.0.1:8000

Swagger documentation: http://127.0.0.1:8000/docs

### 6. Run the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Run Tests

From the project root, run:

```bash
python -m pytest backend/test_main.py -v
```

## Docker

Build and start the application:

```bash
docker compose build
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

## Deployment

**Frontend:** https://movie-recommendation-frontend-mp1u.onrender.com

**Backend API:** https://movie-recommendation-api-xlny.onrender.com

**API Documentation:** https://movie-recommendation-api-xlny.onrender.com/docs

## Author

Manasa Pandranki

B.Tech – Artificial Intelligence and Data Science
