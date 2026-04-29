#!/bin/bash

# BetGenie Deployment Script
# Deploys the web app to Firebase Hosting

set -e

echo "=========================================="
echo "  BetGenie Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo -e "${RED}❌ Firebase CLI not found${NC}"
    echo "Install with: npm install -g firebase-tools"
    exit 1
fi

echo -e "${GREEN}✅ Firebase CLI found${NC}"

# Check if user is logged in
echo ""
echo "Checking Firebase login status..."
if ! firebase projects:list &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Firebase${NC}"
    echo "Running: firebase login"
    firebase login
fi

echo -e "${GREEN}✅ Firebase authenticated${NC}"

# Navigate to project root
cd "$(dirname "$0")"

# Build the web app
echo ""
echo "📦 Building Next.js web app..."
cd apps/web
npm install
npm run build

echo -e "${GREEN}✅ Build complete${NC}"

# Return to root
cd ../..

# Check for service account key
if [ -f "firebase-service-account.json" ]; then
    echo -e "${GREEN}✅ Service account key found${NC}"
    export GOOGLE_APPLICATION_CREDENTIALS="./firebase-service-account.json"
else
    echo -e "${YELLOW}⚠️  Service account key not found${NC}"
    echo "Download from: https://console.firebase.google.com/project/betgenie-ai/settings/serviceaccounts/adminsdk"
    echo "Save as: firebase-service-account.json"
fi

# Deploy to Firebase
echo ""
echo "🚀 Deploying to Firebase..."
echo ""

# Deploy hosting
echo "Deploying Hosting..."
firebase deploy --only hosting --project betgenie-ai

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}  ✅ Deployment Complete!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo "🌐 Website URL: https://betgenie-ai.web.app"
echo "📊 Firebase Console: https://console.firebase.google.com/project/betgenie-ai"
echo ""
