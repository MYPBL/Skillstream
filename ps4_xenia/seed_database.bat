@echo off
echo Seeding database with demo data...
cd backend
python seed_data.py
echo.
echo Database seeded successfully!
echo You can now login as:
echo   - Newbie Ned (newbie@example.com)
echo   - Fast Fiona (fast@example.com)
pause
