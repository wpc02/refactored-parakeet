@echo off
setlocal

cd /d "C:\git repository"

REM Use provided URL, or existing origin, or prompt.
if not "%~1"=="" (
    set "REMOTE_URL=%~1"
) else (
    for /f "delims=" %%i in ('git remote get-url origin 2^>nul') do set "REMOTE_URL=%%i"
)

if "%REMOTE_URL%"=="" (
    echo Usage: push-to-github.bat https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo.
    set /p REMOTE_URL=Please enter GitHub repository URL: 
)

if "%REMOTE_URL%"=="" (
    echo No remote URL provided. Aborting.
    pause
    exit /b 1
)

echo.
echo [1/6] Configuring git user...
git config user.name "GGBond2424648901"
git config user.email "GGBond2424648901@users.noreply.github.com"

echo [2/6] Adding files...
git add .

echo [3/6] Creating initial commit...
git commit -m "Initial commit"

echo [4/6] Setting main branch...
git branch -M main

echo [5/6] Setting remote origin...
git remote remove origin 2>nul
git remote add origin "%REMOTE_URL%"

echo [6/6] Pushing to GitHub...
git push -u origin main

echo.
echo Done. If you see an error, please check the GitHub URL and authentication.
pause
