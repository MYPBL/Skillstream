# Local Development Setup (Without Docker)

Since Docker is not installed, follow these steps to run the application locally:

## Quick Start

### 1. Start the Backend (Terminal 1)
```bash
run_backend.bat
```
Wait for the message: `Application startup complete.`

### 2. Seed the Database (Terminal 2 - One Time Only)
```bash
seed_database.bat
```

### 3. Start the Frontend (Terminal 3)
```bash
run_frontend.bat
```

### 4. Open the Application
- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs

## Demo Flow

1. Select **Newbie Ned** from the persona screen
2. Complete a module with a **low score** (< 50%)
3. Return to dashboard and observe the next recommendation is easier/different format
4. Switch to **Fast Fiona**
5. Complete a module with a **high score** (100%)
6. Observe the next recommendation jumps to advanced content

## Troubleshooting

**If backend fails to start:**
- Make sure you're in the project root directory
- Check that Python 3.11+ is installed: `python --version`

**If frontend fails to start:**
- Make sure Node.js is installed: `node --version`
- Delete `frontend/node_modules` and run `run_frontend.bat` again
