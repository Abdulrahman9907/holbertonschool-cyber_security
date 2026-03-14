@echo off
REM This script runs after you're logged into the intranet

echo.
echo ================================================
echo STEP 1: PUSHING CODE
echo ================================================
echo.

cd /d "C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"

echo Running: git add -A
git add -A

echo Running: git commit -m a
git commit -m a

echo Running: git push
git push

echo.
echo ================================================
echo STEP 2: RUNNING CORRECTIONS
echo ================================================
echo.

echo Code has been pushed!
echo.
echo Now switch to your intranet browser and:
echo 1. Look for the "Run the correction" button
echo 2. Click it
echo 3. Check for errors
echo 4. Fix any issues if needed
echo 5. Run correction again
echo.
echo Repeat until all tests pass.
echo.
pause
