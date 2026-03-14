# PowerShell script for full intranet automation
# No browser window management needed - just opens it naturally

$projectDir = "C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"
Set-Location $projectDir

Write-Host "`n========== HOLBERTON INTRANET AUTOMATION ==========" -ForegroundColor Cyan
Write-Host ""

# Step 1: Open the intranet page in default browser
Write-Host "[STEP 1] Opening intranet project page..." -ForegroundColor Yellow
Start-Process "https://intranet.hbtn.io/projects/3118"

Write-Host "[ACTION] Browser opened. Please log in with your Google account."
Write-Host "[WAIT] Once logged in, click back to this window and press ENTER" -ForegroundColor Green
Read-Host

Write-Host "`n[STEP 2] Pushing code with commit 'a'..." -ForegroundColor Yellow

# Git operations
& git add -A
& git commit -m 'a'
& git push

Write-Host "[OK] Code pushed" -ForegroundColor Green

Write-Host "`n[STEP 3] Running corrections..." -ForegroundColor Yellow
Write-Host "[ACTION] Go back to browser window and click 'Run the correction'" -ForegroundColor Green
Write-Host "[WAIT] Return here after seeing test results and press ENTER" -ForegroundColor Green

$attemptCount = 0
$maxAttempts = 10

while ($attemptCount -lt $maxAttempts) {
    $attemptCount++

    Read-Host "`n[ATTEMPT $attemptCount] Press ENTER after clicking 'Run the correction' in browser"

    Write-Host "[ANALYZING] Check the browser for:"
    Write-Host "  - SUCCESS: All tests passed - you're done!"
    Write-Host "  - ERROR: See error message and fix the code" -ForegroundColor Red

    Write-Host "`n[QUESTION] Did the tests pass? (y/n)"
    $response = Read-Host

    if ($response -eq 'y' -or $response -eq 'yes') {
        Write-Host "`n[SUCCESS] All tests passed!" -ForegroundColor Green
        break
    }

    Write-Host "`n[ACTION] Fix the code based on the error message" -ForegroundColor Yellow
    Write-Host "[WAIT] After fixing, press ENTER to push fixes and retry"
    Read-Host

    Write-Host "[PUSHING] Pushing fixed code..." -ForegroundColor Yellow
    & git add -A
    & git commit -m 'a'
    & git push

    Write-Host "[DONE PUSHING] Go back to browser and click 'Run the correction' again" -ForegroundColor Green
}

Write-Host "`n========== AUTOMATION COMPLETE ==========" -ForegroundColor Cyan
Write-Host "Close the browser window when done." -ForegroundColor Green
Read-Host "Press ENTER to exit"
