# BetGenie Deployment Guide

This guide covers deploying BetGenie to Firebase App Hosting and Google Cloud Run services.

## Prerequisites

1. **Firebase Project Setup**
   - Create Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
   - Project ID: `betgenie-ai` (production) or `betgenie-ai-staging` (staging)
   - Enable: Firestore, Storage, Cloud Functions, Hosting

2. **Google Cloud Setup**
   - Enable Cloud Run API
   - Enable Cloud Build API
   - Create service account with:
     - Cloud Run Admin
     - Cloud Functions Developer
     - Firebase Admin
     - Storage Admin

3. **Local Setup**
   ```bash
   npm install -g firebase-tools
   npm install -g gcloud
   gcloud auth login
   firebase login
   ```

## Firebase Configuration

### 1. Project Configuration

The `.firebaserc` file defines project aliases:
```json
{
  "projects": {
    "default": "betgenie-ai",
    "production": "betgenie-ai",
    "staging": "betgenie-ai-staging"
  }
}
```

### 2. Firebase Services

**Firestore** (`firebase/firestore.rules`, `firebase/firestore.indexes.json`)
- Collections: games, players, odds, picks, parlays, news_events, etc.
- Security rules control read/write access

**Storage** (`firebase/storage.rules`)
- Buckets: profile-images, logos, reports, assets, temp

**Cloud Functions** (`services/functions/`)
- API endpoints for picks, parlays, games, news
- Firestore triggers for automated processing
- Scheduled functions for daily reports

**Hosting** (`firebase.json`)
- Serves Next.js static build from `website/dist`
- Rewrites API routes to Cloud Functions

## Local Development

### Start Firebase Emulators
```bash
npm run emulators
```

This starts:
- Firestore emulator (port 8080)
- Functions emulator (port 5001)
- Hosting emulator (port 5000)
- Storage emulator (port 9199)

### Build Website
```bash
cd website
npm install
npm run build
```

### Build Cloud Functions
```bash
cd services/functions
npm install
npm run build
```

## Deployment

### Option 1: Manual Deployment

#### Deploy Firebase Services
```bash
# Deploy everything
firebase deploy

# Deploy specific services
firebase deploy --only hosting
firebase deploy --only functions
firebase deploy --only firestore:rules,firestore:indexes
firebase deploy --only storage:rules
```

#### Deploy Cloud Run Services
```bash
# Build and deploy each service
cd cloud-services/nba_data_ingestion
gcloud builds submit --tag gcr.io/betgenie-ai/nba_data_ingestion
gcloud run deploy nba_data_ingestion \
  --image gcr.io/betgenie-ai/nba_data_ingestion \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Repeat for other services:
# - odds_aggregation
# - news_monitoring
# - ai_analysis
```

### Option 2: Firebase App Hosting (Native GitHub Integration)

Firebase App Hosting has built-in GitHub integration - no GitHub Actions needed.

#### Setup Firebase App Hosting GitHub Connection

1. **Enable Firebase App Hosting**
   ```bash
   firebase experiments:enable apphosting
   ```

2. **Connect GitHub Repository**
   - Go to Firebase Console: https://console.firebase.google.com/project/betgenie-ai/apphosting
   - Click "Get Started"
   - Click "Connect GitHub"
   - Authorize Firebase to access your GitHub
   - Select repository: `Richard-Mohn/BetGenie`
   - Select branch: `master`

3. **Automatic Deployment**
   - Firebase App Hosting watches your GitHub repository
   - Every push to `master` triggers automatic build and deploy
   - Uses `apphosting.yaml` for configuration
   - No GitHub Actions workflow needed

#### Manual Deployment (via Firebase CLI)
   ```bash
   # Deploy Firebase App Hosting
   firebase apphosting:backends:create --project betgenie-ai --region us-central1 --root-directory apps/web

   # Deploy Firebase Services (Functions, Firestore, Storage)
   firebase deploy --only functions,firestore,storage --project betgenie-ai
   ```

## Environment Variables

### Firebase Web App Config
Add to `.env.local` in website directory:
```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=betgenie-ai
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=your_measurement_id
```

### Cloud Run Environment Variables
Set via `--set-env-vars` in deployment:
```bash
--set-env-vars GCP_PROJECT_ID=betgenie-ai
--set-env-vars ODDS_API_KEY=your_odds_api_key
--set-env-vars BALLDONTLIE_API_KEY=your_balldontlie_key
```

## Cloud Run Services

### 1. NBA Data Ingestion
- **Purpose**: Fetches NBA games, players, stats
- **Endpoint**: `/fetch-games`, `/fetch-players`, `/fetch-player-stats`
- **Schedule**: Run hourly via Cloud Scheduler

### 2. Odds Aggregation
- **Purpose**: Aggregates odds from multiple sportsbooks
- **Endpoint**: `/fetch-odds`
- **Schedule**: Run every 30 minutes

### 3. News Monitoring
- **Purpose**: Monitors RSS feeds for player news
- **Endpoint**: `/fetch-news`
- **Schedule**: Run every 15 minutes

### 4. AI Analysis
- **Purpose**: Runs AI analysis on data
- **Endpoint**: `/analyze`, `/generate-daily-report`
- **Schedule**: Run daily at 6 AM EST

## Verification

### Check Firebase Deployment
```bash
firebase deploy --only hosting
# Visit: https://betgenie-ai.web.app
```

### Check Cloud Functions
```bash
firebase functions:log
```

### Check Cloud Run Services
```bash
gcloud run services list
gcloud run services describe nba_data_ingestion --region us-central1
```

### Test API Endpoints
```bash
# Test health check
curl https://betgenie-ai.web.app/api/health

# Test picks endpoint
curl https://betgenie-ai.web.app/api/picks/today
```

## Monitoring

### Firebase Console
- Realtime Database viewer
- Cloud Functions logs
- Analytics

### Google Cloud Console
- Cloud Run logs
- Error Reporting
- Cloud Monitoring

## Troubleshooting

### Build Errors
```bash
# Clear Next.js cache
cd website
rm -rf .next
npm run build
```

### Deployment Errors
```bash
# Check Firebase project
firebase projects:list

# Check GCP project
gcloud config list
```

### Cloud Run Errors
```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision"
```

## Cost Estimates

**Firebase Hosting**: Free tier sufficient for most use cases
**Cloud Functions**: Pay per invocation (~$0.40/million)
**Cloud Run**: 
- 4 services × $0.40/GB-hour
- Estimate: $50-100/month depending on traffic
**Firestore**: $0.18/GB stored + $0.06/100K reads

## Next Steps

1. Set up Firebase project and get config values
2. Add environment variables to `.env.local`
3. Test local development with emulators
4. Deploy to staging first
5. Set up GitHub Actions for CI/CD
6. Monitor and optimize costs
