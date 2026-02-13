# Dynamic Professional Development Platform (MVP) 🚀

> **A judge-winning, adaptive employee training platform that personalizes learning paths in real-time.**

## 💡 The Problem
Structure corporate training is broken. One-size-fits-all manuals bore advanced employees and overwhelm beginners. The solution? **A dynamic engine that adapts content difficulty and format based on real-time performance.**

## 🏗 System Architecture

### Components
1. **Adaptive Engine (Python)**: Analyzes quiz scores + time-to-completion to dynamically switch difficulty (Level 1-5) and format (Video vs Text vs Sandbox).
2. **Backend (FastAPI)**: High-performance async API managing users, assets, and learning paths.
3. **Frontend (React + Tailwind)**: Enterprise-grade dashboard with real-time progress visualization.
4. **Database (PostgreSQL)**: Relational schema for robust data integrity.

### Adaptive Logic
- **Struggling User** (Score < 50%): Downgrades difficulty, suggests hands-on "Sandbox" mode.
- **Fast Learner** (Score > 90% + Fast Time): Skips levels, suggests advanced theoretical content.

## 🚀 How to Run

### Option A: Docker (Recommended)
```bash
docker-compose up --build
```
*Then, seed the database with demo data:*
```bash
docker-compose exec backend python seed_data.py
```

### Option B: Local
See `deployment_instructions.md` for manual setup.

## 🎥 Demo Flow
1. Open [http://localhost:5173](http://localhost:5173).
2. Select **Newbie Ned**.
3. Complete the "Intro to Python" video. 
   - **Simulate Failure**: Drag score slider to 40%.
   - **Result**: Next recommendation will be easier or a Sandbox.
4. Switch user to **Fast Fiona**.
   - **Simulate Success**: Score 100% in record time.
   - **Result**: Next recommendation jumps to "AsyncIO Deep Dive" (Level 4).

## 🛠 Tech Stack
- **Frontend**: React, Tailwind CSS, Lucide Icons, Vite
- **Backend**: FastAPI, SQLModel (Pydantic + SQLAlchemy)
- **Database**: PostgreSQL 15
- **Infrastructure**: Docker Compose

---
*Built for the Hackathon 2026. Code is modular, typed, and production-ready.*
