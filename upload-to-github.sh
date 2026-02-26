#!/bin/bash
# ===========================================
# MeetingMind AI - Upload to GitHub
# ===========================================
# Usage: ./upload-to-github.sh YOUR_USERNAME
# ===========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🚀 MeetingMind AI - Upload to GitHub"
echo "======================================"

# Check if username provided
if [ -z "$1" ]; then
    echo -e "${RED}❗ Usage: $0 YOUR_GITHUB_USERNAME${NC}"
    echo ""
    echo "Example: $0 john-doe"
    echo ""
    echo "Or manually:"
    echo "1. Go to https://github.com/new"
    echo "2. Create repository: meetingmind"
    echo "3. Copy the remote URL"
    echo "4. Run: git remote add origin https://github.com/YOUR_USERNAME/meetingmind.git"
    echo "5. Run: git push -u origin main"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="meetingmind"
REMOTE_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo -e "${YELLOW}📝 Repository URL:${NC}"
echo "   ${REMOTE_URL}"
echo ""

# Check if remote already exists
if git remote | grep -q "^origin$"; then
    echo -e "${YELLOW}⚠️  Remote 'origin' already exists${NC}"
    echo "Removing existing remote..."
    git remote remove origin
fi

# Add remote
echo "➕ Adding remote..."
git remote add origin "${REMOTE_URL}"
echo -e "${GREEN}✅ Remote added${NC}"

# Verify remote
echo ""
echo "📋 Verifying remote..."
git remote -v

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
echo -e "${YELLOW}⚠️  You may be asked for your GitHub credentials${NC}"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Successfully uploaded to GitHub!${NC}"
    echo ""
    echo "📍 Your repository:"
    echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo ""
    echo "🎉 Next steps:"
    echo "   1. Open your repository on GitHub"
    echo "   2. Add description and topics"
    echo "   3. Set up GitHub Actions (optional)"
    echo "   4. Share with the world!"
else
    echo ""
    echo -e "${RED}❌ Push failed!${NC}"
    echo ""
    echo "Possible solutions:"
    echo "1. Make sure you created the repository on GitHub first"
    echo "2. Check your GitHub credentials"
    echo "3. Use SSH instead:"
    echo "   git remote set-url origin git@github.com:${GITHUB_USERNAME}/${REPO_NAME}.git"
    echo "   git push -u origin main"
    exit 1
fi
