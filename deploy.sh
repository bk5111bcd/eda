#!/bin/bash

# GitHub Deployment Setup Script for Auto EDA Chatbot
# This script automates GitHub setup after manual repository creation

set -e

echo "🚀 Auto EDA Chatbot - GitHub Deployment"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USER
read -p "Enter repository name (default: auto-eda-chatbot): " REPO_NAME
REPO_NAME=${REPO_NAME:-auto-eda-chatbot}

echo ""
echo "📋 Configuration Summary:"
echo "  GitHub User: $GITHUB_USER"
echo "  Repository: $REPO_NAME"
echo "  Remote URL: https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Check current git status
echo ""
echo "📊 Current Git Status:"
git status --short

echo ""
echo "⚙️  Setting up GitHub remote..."

# Remove existing remote if it exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "  ⚠️  Remote 'origin' already exists"
    read -p "  Replace it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
        echo "  ✓ Removed old remote"
    fi
fi

# Add remote
REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
    echo "  ✓ Updated remote URL"
else
    git remote add origin "$REMOTE_URL"
    echo "  ✓ Added remote origin"
fi

# Verify remote
echo ""
echo "🔗 Remote Configuration:"
git remote -v

# Ask about pushing
echo ""
read -p "Ready to push to GitHub? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏸️  Push cancelled. You can push later with:"
    echo "  git push -u origin main"
    exit 0
fi

echo ""
echo "📤 Pushing to GitHub..."
echo "  Branch: main"
echo "  Remote: origin"
echo ""

# Rename branch if needed
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "  Renaming branch: $CURRENT_BRANCH → main"
    git branch -M main
fi

# Push to GitHub
if git push -u origin main 2>&1; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🎉 Your repository is now live at:"
    echo "  https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "📖 Next steps:"
    echo "  1. Visit your GitHub repository"
    echo "  2. Add repository topics (Settings → About)"
    echo "  3. Enable GitHub Pages (optional)"
    echo "  4. Deploy to Streamlit Cloud (optional)"
    echo ""
    echo "For detailed instructions, see DEPLOYMENT.md"
else
    echo ""
    echo "❌ Push failed. Check your credentials and internet connection."
    echo "   See DEPLOYMENT.md for troubleshooting"
    exit 1
fi

# Optional: Open repository in browser
echo ""
read -p "Open repository in browser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Try different browser commands based on OS
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "https://github.com/$GITHUB_USER/$REPO_NAME"
    elif command -v open >/dev/null 2>&1; then
        open "https://github.com/$GITHUB_USER/$REPO_NAME"
    else
        echo "  Copy this URL to your browser:"
        echo "  https://github.com/$GITHUB_USER/$REPO_NAME"
    fi
fi

echo ""
echo "✨ GitHub deployment complete!"
echo ""
