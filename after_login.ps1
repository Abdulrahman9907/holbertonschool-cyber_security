# PowerShell script to run after you're logged into the intranet
# This will:
# 1. Push code with message 'a'
# 2. Help you run corrections

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PUSHING CODE & RUNNING CORRECTIONS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$projectDir = "C:\Users\Admin\Documents\projects\holbertonschool-cyber_security"

Write-Host "`nStep 1: Pushing code with commit 'a'..." -ForegroundColor Yellow
cd $projectDir

Write-Host "  Running: git add -A"
& git add -A

Write-Host "  Running: git commit -m 'a'"
& git commit -m 'a'

Write-Host "  Running: git push"
& git push

Write-Host "`n[OK] Code pushed!" -ForegroundColor Green

Write-Host "`nStep 2: Running corrections on the intranet..." -ForegroundColor Yellow
Write-Host "On the webpage, click the 'Run the correction' button"
Write-Host "Press Enter when done to continue:"
Read-Host

Write-Host "`nDone! Check the intranet page for results." -ForegroundColor Green
