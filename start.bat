@echo off
title EduPlay - UnityLearn Backend Server
color 0B

echo ======================================================================
echo           EduPlay - UnityLearn: Gamified Learning Platform
echo ======================================================================
echo.

cd /d "%~dp0backend"

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Creating Python virtual environment...
    python -m venv venv
    echo       Done!
) else (
    echo [1/3] Virtual environment found.
)

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/3] Checking Supabase database migrations...
python manage.py migrate --no-input

echo.
echo ======================================================================
echo  [SERVER READY] Starting Django Development Server...
echo  * Backend API:  http://127.0.0.1:8000/api/
echo  * Admin Panel:  http://127.0.0.1:8000/admin/
echo.
echo  Demo Logins:
echo   - Admin:   admin     / eduplay123
echo   - Student: alice_dev / eduplay123
echo.
echo  Open frontend\index.html in your browser!
echo ======================================================================
echo.

python manage.py runserver 127.0.0.1:8000
pause
