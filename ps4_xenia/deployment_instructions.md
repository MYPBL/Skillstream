# Deployment Instructions

## Prerequisites
- Docker & Docker Compose
- Node.js (Only if running frontend locally outside Docker)

## Quick Start (Docker)

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Seed Data**
   Once the backend is running, open a new terminal and run:
   ```bash
   # Exec into the backend container
   docker-compose exec backend python seed_data.py
   ```

3. **Access the Application**
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development (Manual)

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Demo Walkthrough

1. **Login**: Go to the frontend. You will see a "Select Your Persona" screen.
   - Choose **Newbie Ned** (Video Learner, struggling).
   - Choose **Fast Fiona** (Text Learner, advanced).

2. **Scenario A: Newbie Ned**
   - Click to start his recommended video module (Level 1).
   - In the Asset Viewer, complete the module with a **Low Score** (< 50).
   - Return to Dashboard. Observe that the next recommendation is either same level or switched format (Sandbox), or easier.

3. **Scenario B: Fast Fiona**
   - Select Fiona.
   - Start her Text module.
   - Complete with **High Score** (100) and fast time.
   - Return to Dashboard. Observe the next recommendation is Level 3 or 4 (Advanced).
