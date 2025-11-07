#!/bin/bash

# Streamlit Cloud Deployment Helper Script
# This script helps you deploy your dashboard to Streamlit Cloud

set -e  # Exit on error

echo "=========================================="
echo "🚀 Streamlit Cloud Deployment Helper"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Test locally
echo "📝 Step 1: Testing application locally..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running validation tests..."
python3 test_deployment.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Validation failed. Please fix the issues above.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Local testing complete!${NC}"
echo ""

# Step 2: Git setup
echo "📝 Step 2: Git repository setup"
echo ""

if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git repository already initialized${NC}"
else
    echo "Initializing Git repository..."
    git init
    echo -e "${GREEN}✅ Git initialized${NC}"
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}⚠️  Remote 'origin' already exists${NC}"
    REMOTE_URL=$(git remote get-url origin)
    echo "Current remote: $REMOTE_URL"
else
    echo ""
    echo "Please enter your GitHub repository URL:"
    echo "Example: https://github.com/username/repo-name.git"
    read -p "Repository URL: " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo -e "${RED}❌ No repository URL provided${NC}"
        exit 1
    fi
    
    git remote add origin "$REPO_URL"
    echo -e "${GREEN}✅ Remote added: $REPO_URL${NC}"
fi

echo ""

# Step 3: Commit and push
echo "📝 Step 3: Commit and push to GitHub"
echo ""

# Check for changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
else
    echo "Adding files..."
    git add .
    
    echo "Creating commit..."
    git commit -m "Deploy Credit Risk Model Journey to Streamlit Cloud"
    
    echo -e "${GREEN}✅ Changes committed${NC}"
fi

echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Push failed. Please check your GitHub credentials and repository access.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
echo ""

# Step 4: Instructions for Streamlit Cloud
echo "=========================================="
echo "🎉 Ready for Streamlit Cloud Deployment!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository"
echo "5. Set main file: app.py"
echo "6. Click 'Deploy'"
echo ""
echo "Your app will be live in 2-3 minutes!"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo -e "${GREEN}✅ Deployment preparation complete!${NC}"
