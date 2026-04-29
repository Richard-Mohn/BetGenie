#!/bin/bash

# BetGenie — Complete Setup & Deployment Script
# This script sets up and deploys BetGenie to Firebase App Hosting
# Run this to get everything live in one command

set -e

echo "=========================================="
echo "  BetGenie — Complete Setup & Deploy"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_ID="betgenie-ai"
REGION="us-central1"

# Function to print status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check gcloud
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI not installed"
        echo "Install from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Check firebase
    if ! command -v firebase &> /dev/null; then
        print_error "Firebase CLI not installed"
        echo "Install with: npm install -g firebase-tools"
        exit 1
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        print_error "Git not installed"
        exit 1
    fi
    
    print_success "All prerequisites found"
}

# Check authentication
check_auth() {
    print_status "Checking authentication..."
    
    # Check gcloud auth
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
        print_warning "Not logged in to gcloud"
        echo "Running: gcloud auth login"
        gcloud auth login
    fi
    
    # Check firebase auth
    if ! firebase projects:list &> /dev/null; then
        print_warning "Not logged in to Firebase"
        echo "Running: firebase login"
        firebase login
    fi
    
    # Set project
    gcloud config set project $PROJECT_ID
    firebase use $PROJECT_ID
    
    print_success "Authentication verified"
}

# Enable required APIs
enable_apis() {
    print_status "Enabling required Google Cloud APIs..."
    
    gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID
    gcloud services enable run.googleapis.com --project=$PROJECT_ID
    gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
    gcloud services enable firebaseapphosting.googleapis.com --project=$PROJECT_ID
    
    print_success "APIs enabled"
}

# Create secrets in Secret Manager
create_secrets() {
    print_status "Setting up Google Secret Manager..."
    
    # List of required secrets
    SECRETS=(
        "firebase-web-api-key:Firebase Web API Key"
        "odds-api-key:The Odds API Key"
        "news-api-key:NewsAPI Key"
        "openai-api-key:OpenAI API Key (optional)"
        "twitter-bearer-token:Twitter API Bearer Token (optional)"
    )
    
    print_status "Creating secrets (you'll be prompted for values)..."
    
    for secret_info in "${SECRETS[@]}"; do
        IFS=":" read -r secret_name description <<< "$secret_info"
        
        # Check if secret exists
        if gcloud secrets describe $secret_name --project=$PROJECT_ID &> /dev/null; then
            print_warning "Secret '$secret_name' already exists, skipping"
        else
            echo ""
            echo "Enter value for $description (or press Enter to skip):"
            read -s secret_value
            
            if [ -n "$secret_value" ]; then
                echo -n "$secret_value" | gcloud secrets create $secret_name \
                    --project=$PROJECT_ID \
                    --replication-policy="automatic" \
                    --data-file=-
                print_success "Created secret: $secret_name"
            else
                print_warning "Skipped $secret_name"
            fi
        fi
    done
}

# Grant IAM permissions
setup_iam() {
    print_status "Setting up IAM permissions..."
    
    # Get the default service account
    SERVICE_ACCOUNT="$PROJECT_ID@appspot.gserviceaccount.com"
    
    # Grant Secret Manager access
    for secret in firebase-web-api-key odds-api-key news-api-key; do
        if gcloud secrets describe $secret --project=$PROJECT_ID &> /dev/null; then
            gcloud secrets add-iam-policy-binding $secret \
                --project=$PROJECT_ID \
                --member="serviceAccount:$SERVICE_ACCOUNT" \
                --role="roles/secretmanager.secretAccessor" 2>/dev/null || true
        fi
    done
    
    print_success "IAM permissions configured"
}

# Initialize Firebase App Hosting
init_app_hosting() {
    print_status "Initializing Firebase App Hosting..."
    
    # Enable experiment
    firebase experiments:enable apphosting 2>/dev/null || true
    
    # Check if backend exists
    if firebase apphosting:backends:list --project=$PROJECT_ID 2>/dev/null | grep -q "betgenie"; then
        print_success "Firebase App Hosting backend already exists"
    else
        print_status "Creating Firebase App Hosting backend..."
        firebase apphosting:backends:create \
            --project=$PROJECT_ID \
            --region=$REGION \
            --root-directory=apps/web || true
    fi
}

# Build the project
build_project() {
    print_status "Building Next.js app..."
    
    cd apps/web
    npm ci
    npm run build
    cd ../..
    
    print_success "Build completed"
}

# Create GitHub Actions secrets file
create_github_secrets_guide() {
    print_status "Creating GitHub secrets guide..."
    
    cat > GITHUB_SECRETS_SETUP.md << 'EOF'
# GitHub Secrets Setup

Add these secrets to your GitHub repository:

## Required Secrets

1. **GCP_SA_KEY** (Required)
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=betgenie-ai
   - Select service account: `betgenie-ai@appspot.gserviceaccount.com`
   - Click "Keys" → "Add Key" → "Create New Key" → JSON
   - Copy entire JSON content to this secret

## Optional: Repository Variables

Add these as Repository Variables (not secrets, less secure but easier):

- `NEXT_PUBLIC_FIREBASE_API_KEY` - From Firebase Console
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` - betgenie-ai.firebaseapp.com
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID` - betgenie-ai
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` - betgenie-ai.appspot.com

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
EOF

    print_success "Created GITHUB_SECRETS_SETUP.md"
}

# Commit and push
commit_and_push() {
    print_status "Committing changes..."
    
    git add -A
    git commit -m "Setup Firebase App Hosting deployment configuration

- Added apphosting.yaml for Firebase App Hosting
- Updated firebase.json (removed hosting)
- Added GitHub Actions workflow
- Created deployment scripts and documentation
- Configured Google Secret Manager integration

Ready for automatic deployment on push to main branch." || true
    
    print_status "Pushing to GitHub..."
    git push origin main || print_warning "Push failed - may need to pull first"
    
    print_success "Code pushed to GitHub"
}

# Trigger deployment
trigger_deploy() {
    print_status "Deployment will trigger automatically via GitHub Actions..."
    print_status "Check status at: https://github.com/richardmohn/BetGenie/actions"
    
    echo ""
    echo "=========================================="
    echo "  🎉 SETUP COMPLETE!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Add GCP_SA_KEY secret to GitHub (see GITHUB_SECRETS_SETUP.md)"
    echo "2. Push will trigger automatic deployment"
    echo "3. Site will be live at: https://betgenie-ai.web.app"
    echo ""
    echo "Monitor deployment:"
    echo "  https://github.com/richardmohn/BetGenie/actions"
    echo ""
    echo "Firebase Console:"
    echo "  https://console.firebase.google.com/project/betgenie-ai/apphosting"
    echo ""
}

# Main execution
main() {
    echo "This script will:"
    echo "  1. Check prerequisites (gcloud, firebase, git)"
    echo "  2. Enable required Google Cloud APIs"
    echo "  3. Set up Google Secret Manager"
    echo "  4. Configure IAM permissions"
    echo "  5. Initialize Firebase App Hosting"
    echo "  6. Build the project"
    echo "  7. Commit and push to GitHub"
    echo ""
    echo "Continue? (y/n)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        check_prerequisites
        check_auth
        enable_apis
        create_secrets
        setup_iam
        init_app_hosting
        build_project
        create_github_secrets_guide
        commit_and_push
        trigger_deploy
    else
        echo "Setup cancelled."
        exit 0
    fi
}

# Run main
main
