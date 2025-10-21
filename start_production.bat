@echo off
REM Production startup script for Windows

echo Starting CTI Dashboard in production mode...

REM Create logs directory
if not exist logs mkdir logs

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found
    echo Please create .env file with required configuration
    exit /b 1
)

REM Set production environment
set FLASK_ENV=production

REM Check MongoDB connection
echo Checking MongoDB connection...
python -c "from db.mongo import db_manager; exit(0 if db_manager.connect() else 1)"
if errorlevel 1 (
    echo MongoDB connection failed
    exit /b 1
)
echo MongoDB connected

REM Start with Waitress (Windows-friendly production server)
echo Starting Waitress server...
waitress-serve --port=5000 --threads=4 wsgi:application

REM Alternative: Use Python directly
REM python web\app_enhanced.py
