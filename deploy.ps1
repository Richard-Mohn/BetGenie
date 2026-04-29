# BetGenie Deployment Script (PowerShell)
# Deploys the web app to Firebase Hosting

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  BetGenie Deployment Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if firebase CLI is installed
try {
    $firebaseVersion = firebase --version 2>$null
    Write-Host "✅ Firebase CLI found (v$firebaseVersion)" -ForegroundColor Green
} catch {
    Write-Host "❌ Firebase CLI not found" -ForegroundColor Red
    Write-Host "Install with: npm install -g firebase-tools"
    exit 1
}

# Check if user is logged in
Write-Host ""
Write-Host "Checking Firebase login status..."
try {
    $projects = firebase projects:list 2>$null
    Write-Host "✅ Firebase authenticated" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Not logged in to Firebase" -ForegroundColor Yellow
    Write-Host "Running: firebase login"
    firebase login
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Build the web app
Write-Host ""
Write-Host "📦 Building Next.js web app..."
Set-Location apps/web
npm install
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build complete" -ForegroundColor Green

# Return to root
Set-Location $scriptDir

# Check for service account key
if (Test-Path "firebase-service-account.json") {
    Write-Host "✅ Service account key found" -ForegroundColor Green
    $env:GOOGLE_APPLICATION_CREDENTIALS = "./firebase-service-account.json"
} else {
    Write-Host "⚠️  Service account key not found" -ForegroundColor Yellow
    Write-Host "Download from: https://console.firebase.google.com/project/betgenie-ai/settings/serviceaccounts/adminsdk"
    Write-Host "Save as: firebase-service-account.json"
}

# Deploy to Firebase
Write-Host ""
Write-Host "🚀 Deploying to Firebase..." -ForegroundColor Cyan
Write-Host ""

# Deploy hosting
firebase deploy --only hosting --project betgenie-ai

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  ✅ Deployment Complete!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Website URL: https://betgenie-ai.web.app"
    Write-Host "📊 Firebase Console: https://console.firebase.google.com/project/betgenie-ai"
    Write-Host ""
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}
