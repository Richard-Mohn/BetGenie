# BetGenie — Complete Setup & Deployment Script (PowerShell)
# This script sets up and deploys BetGenie to Firebase App Hosting
# Run this to get everything live in one command

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  BetGenie — Complete Setup & Deploy" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "betgenie-ai"
$REGION = "us-central1"

# Check prerequisites
function Check-Prerequisites {
    Write-Host "[INFO] Checking prerequisites..." -ForegroundColor Blue
    
    # Check gcloud
    try {
        $gcloudVersion = gcloud --version 2>$null
        Write-Host "[SUCCESS] gcloud CLI found" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] gcloud CLI not installed" -ForegroundColor Red
        Write-Host "Install from: https://cloud.google.com/sdk/docs/install"
        exit 1
    }
    
    # Check firebase
    try {
        $firebaseVersion = firebase --version 2>$null
        Write-Host "[SUCCESS] Firebase CLI found" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Firebase CLI not installed" -ForegroundColor Red
        Write-Host "Install with: npm install -g firebase-tools"
        exit 1
    }
    
    # Check git
    try {
        $gitVersion = git --version 2>$null
        Write-Host "[SUCCESS] Git found" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Git not installed" -ForegroundColor Red
        exit 1
    }
}

# Check authentication
function Check-Auth {
    Write-Host "[INFO] Checking authentication..." -ForegroundColor Blue
    
    # Check gcloud auth
    $gcloudAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
    if (-not $gcloudAccount) {
        Write-Host "[WARNING] Not logged in to gcloud" -ForegroundColor Yellow
        Write-Host "Running: gcloud auth login"
        gcloud auth login
    }
    
    # Check firebase auth
    try {
        firebase projects:list 2>$null | Out-Null
    } catch {
        Write-Host "[WARNING] Not logged in to Firebase" -ForegroundColor Yellow
        Write-Host "Running: firebase login"
        firebase login
    }
    
    # Set project
    gcloud config set project $PROJECT_ID
    firebase use $PROJECT_ID
    
    Write-Host "[SUCCESS] Authentication verified" -ForegroundColor Green
}

# Enable required APIs
function Enable-APIs {
    Write-Host "[INFO] Enabling required Google Cloud APIs..." -ForegroundColor Blue
    
    gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID
    gcloud services enable run.googleapis.com --project=$PROJECT_ID
    gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
    gcloud services enable firebaseapphosting.googleapis.com --project=$PROJECT_ID
    
    Write-Host "[SUCCESS] APIs enabled" -ForegroundColor Green
}

# Create secrets
function Create-Secrets {
    Write-Host "[INFO] Setting up Google Secret Manager..." -ForegroundColor Blue
    
    $secrets = @(
        @{Name="firebase-web-api-key"; Description="Firebase Web API Key"},
        @{Name="odds-api-key"; Description="The Odds API Key"},
        @{Name="news-api-key"; Description="NewsAPI Key"},
        @{Name="openai-api-key"; Description="OpenAI API Key (optional)"},
        @{Name="twitter-bearer-token"; Description="Twitter API Bearer Token (optional)"}
    )
    
    foreach ($secret in $secrets) {
        $name = $secret.Name
        $desc = $secret.Description
        
        # Check if secret exists
        $exists = gcloud secrets describe $name --project=$PROJECT_ID 2>$null
        if ($exists) {
            Write-Host "[WARNING] Secret '$name' already exists, skipping" -ForegroundColor Yellow
        } else {
            Write-Host ""
            $value = Read-Host -AsSecureString "Enter value for $desc (or press Enter to skip)"
            
            if ($value.Length -gt 0) {
                $plainValue = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
                    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($value)
                )
                $plainValue | gcloud secrets create $name --project=$PROJECT_ID --replication-policy="automatic" --data-file=-
                Write-Host "[SUCCESS] Created secret: $name" -ForegroundColor Green
            } else {
                Write-Host "[WARNING] Skipped $name" -ForegroundColor Yellow
            }
        }
    }
}

# Setup IAM
function Setup-IAM {
    Write-Host "[INFO] Setting up IAM permissions..." -ForegroundColor Blue
    
    $SERVICE_ACCOUNT = "$PROJECT_ID@appspot.gserviceaccount.com"
    
    $secrets = @("firebase-web-api-key", "odds-api-key", "news-api-key")
    foreach ($secret in $secrets) {
        try {
            gcloud secrets add-iam-policy-binding $secret --project=$PROJECT_ID `
                --member="serviceAccount:$SERVICE_ACCOUNT" `
                --role="roles/secretmanager.secretAccessor" 2>$null
        } catch {
            # Ignore errors
        }
    }
    
    Write-Host "[SUCCESS] IAM permissions configured" -ForegroundColor Green
}

# Initialize Firebase App Hosting
function Init-AppHosting {
    Write-Host "[INFO] Initializing Firebase App Hosting..." -ForegroundColor Blue
    
    firebase experiments:enable apphosting 2>$null
    
    $backends = firebase apphosting:backends:list --project=$PROJECT_ID 2>$null
    if ($backends -match "betgenie") {
        Write-Host "[SUCCESS] Firebase App Hosting backend already exists" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Creating Firebase App Hosting backend..." -ForegroundColor Blue
        firebase apphosting:backends:create --project=$PROJECT_ID --region=$REGION --root-directory=apps/web
    }
}

# Build project
function Build-Project {
    Write-Host "[INFO] Building Next.js app..." -ForegroundColor Blue
    
    Set-Location apps/web
    npm ci
    npm run build
    Set-Location ../..
    
    Write-Host "[SUCCESS] Build completed" -ForegroundColor Green
}

# Create GitHub secrets guide
function Create-GitHubSecretsGuide {
    Write-Host "[INFO] Creating GitHub secrets guide..." -ForegroundColor Blue
    
    $guideContent = @"
# GitHub Secrets Setup

Add these secrets to your GitHub repository:

## Required Secrets

1. **GCP_SA_KEY** (Required)
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=betgenie-ai
   - Select service account: `betgenie-ai@appspot.gserviceaccount.com`
   - Click "Keys" → "Add Key" → "Create New Key" → JSON
   - Copy entire JSON content to this secret

## How to Add Secrets

1. Go to: https://github.com/richardmohn/BetGenie/settings/secrets/actions
2. Click "New repository secret"
3. Name: `GCP_SA_KEY`
4. Value: Paste the entire JSON service account key
5. Click "Add secret"

## Service Account Permissions

The service account needs these roles:
- Firebase Admin
- Cloud Functions Developer
- Cloud Run Admin
- Secret Manager Secret Accessor
- Cloud Build Editor

Add them at: https://console.cloud.google.com/iam-admin/iam?project=betgenie-ai
"@
    
    $guideContent | Out-File -FilePath "GITHUB_SECRETS_SETUP.md" -Encoding utf8
    Write-Host "[SUCCESS] Created GITHUB_SECRETS_SETUP.md" -ForegroundColor Green
}

# Commit and push
function Commit-AndPush {
    Write-Host "[INFO] Committing changes..." -ForegroundColor Blue
    
    git add -A
    git commit -m "Setup Firebase App Hosting deployment configuration" 2>$null || Write-Host "[WARNING] Nothing to commit or commit failed" -ForegroundColor Yellow
    
    Write-Host "[INFO] Pushing to GitHub..." -ForegroundColor Blue
    git push origin main 2>$null || Write-Host "[WARNING] Push failed - may need to pull first" -ForegroundColor Yellow
    
    Write-Host "[SUCCESS] Code pushed to GitHub" -ForegroundColor Green
}

# Main execution
function Main {
    Write-Host "This script will:"
    Write-Host "  1. Check prerequisites (gcloud, firebase, git)"
    Write-Host "  2. Enable required Google Cloud APIs"
    Write-Host "  3. Set up Google Secret Manager"
    Write-Host "  4. Configure IAM permissions"
    Write-Host "  5. Initialize Firebase App Hosting"
    Write-Host "  6. Build the project"
    Write-Host "  7. Commit and push to GitHub"
    Write-Host ""
    
    $response = Read-Host "Continue? (y/n)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        Check-Prerequisites
        Check-Auth
        Enable-APIs
        Create-Secrets
        Setup-IAM
        Init-AppHosting
        Build-Project
        Create-GitHubSecretsGuide
        Commit-AndPush
        
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "  🎉 SETUP COMPLETE!" -ForegroundColor Green
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:"
        Write-Host "1. Add GCP_SA_KEY secret to GitHub (see GITHUB_SECRETS_SETUP.md)"
        Write-Host "2. Push will trigger automatic deployment"
        Write-Host "3. Site will be live at: https://betgenie-ai.web.app"
        Write-Host ""
        Write-Host "Monitor deployment:"
        Write-Host "  https://github.com/richardmohn/BetGenie/actions"
        Write-Host ""
        Write-Host "Firebase Console:"
        Write-Host "  https://console.firebase.google.com/project/betgenie-ai/apphosting"
        Write-Host ""
    } else {
        Write-Host "Setup cancelled."
        exit 0
    }
}

# Run main
Main
