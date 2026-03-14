@echo off
REM START HERE - Run this batch file

setlocal enabledelayedexpansion

echo.
echo ===========================================================
echo  HOLBERTON SCHOOL - PROJECT 3118 SUBMISSION AUTOMATION
echo ===========================================================
echo.

cd /d "C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"

echo [STEP 1] Opening browser to intranet...
start https://intranet.hbtn.io/projects/3118

timeout /t 5 /nobreak

echo.
echo [STEP 2] Log in to your account in the browser window
echo.
echo    (User guide:)
echo    1. Browser should have opened to project 3118
echo    2. Click "Sign in with Google" (recommended for Holberton accounts)
echo    3. Complete the login process
echo    4. Return here after you see the project page
echo.
echo [ACTION] Press ANY KEY when you are logged in and ready:
pause > nul

echo.
echo [STEP 3] Starting automation script...
echo.

python final_automation.py

echo.
echo [DONE] Completed!
echo.
pause
