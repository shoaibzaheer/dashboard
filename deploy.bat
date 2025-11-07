@echo off
REM Streamlit Cloud Deployment Helper Script for Windows
REM This script helps you deploy your dashboard to Streamlit Cloud

echo ==========================================
echo 🚀 Streamlit Cloud Deployment Helper
echo ==========================================
echo.

REM Step 1: Test locally
echo 📝 Step 1: Testing application locally...
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

echo Installing dependencies...
pip install -q -r requirements.txt

echo Running validation tests...
python test_deployment.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Validation failed. Please fix the issues above.
    exit /b 1
)

echo.
echo ✅ Local testing complete!
echo.

REM Step 2: Git setup
echo 📝 Step 2: Git repository setup
echo.

if exist .git (
    echo ⚠️  Git repository already initialized
) else (
    echo Initializing Git repository...
    git init
    echo ✅ Git initialized
)

REM Check if remote exists
git remote | findstr "origin" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Remote 'origin' already exists
    for /f "tokens=*" %%i in ('git remote get-url origin') do set REMOTE_URL=%%i
    echo Current remote: %REMOTE_URL%
) else (
    echo.
    echo Please enter your GitHub repository URL:
    echo Example: https://github.com/username/repo-name.git
    set /p REPO_URL="Repository URL: "
    
    if "%REPO_URL%"=="" (
        echo ❌ No repository URL provided
        exit /b 1
    )
    
    git remote add origin "%REPO_URL%"
    echo ✅ Remote added: %REPO_URL%
)

echo.

REM Step 3: Commit and push
echo 📝 Step 3: Commit and push to GitHub
echo.

echo Adding files...
git add .

echo Creating commit...
git commit -m "Deploy Credit Risk Model Journey to Streamlit Cloud"

echo ✅ Changes committed
echo.

echo Pushing to GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Push failed. Please check your GitHub credentials and repository access.
    exit /b 1
)

echo.
echo ✅ Successfully pushed to GitHub!
echo.

REM Step 4: Instructions for Streamlit Cloud
echo ==========================================
echo 🎉 Ready for Streamlit Cloud Deployment!
echo ==========================================
echo.
echo Next steps:
echo.
echo 1. Go to: https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Click 'New app'
echo 4. Select your repository
echo 5. Set main file: app.py
echo 6. Click 'Deploy'
echo.
echo Your app will be live in 2-3 minutes!
echo.
echo 📚 For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
echo ✅ Deployment preparation complete!

pause
