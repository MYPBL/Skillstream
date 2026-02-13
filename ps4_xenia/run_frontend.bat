@echo off
echo Installing frontend dependencies...
cd frontend
call npm install

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:5173
echo.

npm run dev
