@echo off
setlocal

echo ==========================================
echo   AI Resume Screening System - Startup
echo ==========================================

:: Clear ports 8000 (Backend) and 3000 (Frontend)
echo Cleaning existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do taskkill /f /pid %%a 2>nul

:: Start Backend in a new window
echo [1/2] Starting Backend (FastAPI on port 8000)...
start "Backend - AI Resume" cmd /C "echo Starting Backend... && python backend/main.py"

:: Give the backend a second to initialize
timeout /t 2 /nobreak > nul

:: Start Frontend in a new window
echo [2/2] Starting Frontend (Next.js on port 3000)...
start "Frontend - AI Resume" cmd /C "echo Starting Frontend... && cd web-frontend && npm run dev"

echo.
echo ==========================================
echo   All systems are launching!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3000
echo ==========================================
echo.
pause
