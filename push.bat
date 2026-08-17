@echo off
cd /d "C:\git repository"
if exist ".git\pushing" del ".git\pushing"
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
pause
