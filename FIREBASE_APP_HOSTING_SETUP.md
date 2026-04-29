# Firebase App Hosting — Complete Setup Guide

This guide walks you through deploying BetGenie using **Firebase App Hosting** with automatic GitHub deployments.

---

## 🎯 What is Firebase App Hosting?

Firebase App Hosting is Google's modern hosting solution that:
- Automatically builds & deploys on every push to GitHub
- Provides CI/CD out of the box
- Supports Next.js with SSR/SSG
- Global CDN with edge caching
- Automatic HTTPS & custom domains

**Your deployment URL:** `https://betgenie-ai.web.app`

---

## 📋 Prerequisites

### 1. GitHub Repository
- Repository must be connected to Firebase
- GitHub Actions enabled

### 2. Firebase Project
- Project ID: `betgenie-ai`
- Billing enabled (pay-as-you-go required for App Hosting)
- Firebase App Hosting enabled in console

### 3. Required Tools (on your machine)
```bash
# Firebase CLI
npm install -g firebase-tools

# Google Cloud CLI
npm install -g gcloud

# Login to both
firebase login
gcloud auth login
```

---

## 🔑 Step 1: Create GitHub Secrets

Go to your GitHub repository: **Settings → Secrets and variables → Actions**

Add these secrets:

### Required Secrets

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `GCP_SA_KEY` | Service account JSON | Firebase Console → Project Settings → Service Accounts → Generate new private key |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Web API Key | Firebase Console → Project Settings → General → Web API Key |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Auth domain | `betgenie-ai.firebaseapp.com` |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Project ID | `betgenie-ai` |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Storage bucket | `betgenie-ai.appspot.com` |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Sender ID | Firebase Console → Project Settings → Cloud Messaging |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | App ID | Firebase Console → Project Settings → General → Your apps |
| `NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID` | Measurement ID | Firebase Console → Project Settings → General → Your apps |

### Optional Secrets (for full functionality)
- `ODDS_API_KEY` - From https://the-odds-api.com
- `NEWS_API_KEY` - From https://newsapi.org
- `OPENAI_API_KEY` - From https://platform.openai.com

---

## 🔧 Step 2: Enable Firebase App Hosting

### In Firebase Console:
1. Go to https://console.firebase.google.com/project/betgenie-ai/apphosting
2. Click **"Get started"**
3. Connect your GitHub repository
4. Select the repository: `richardmohn/BetGenie`
5. Configure build:
   - Root directory: `apps/web`
   - Build command: `npm run build`
   - Output directory: `dist`

### Or use Firebase CLI:
```bash
# Enable App Hosting APIs
firebase experiments:enable apphosting

# Initialize App Hosting
firebase apphosting:backends:create
```

---

## 🚀 Step 3: Deploy (3 Ways)

### Option A: Push to GitHub (Automatic)
```bash
# Add all files
git add .

# Commit
git commit -m "Setup Firebase App Hosting deployment"

# Push to main - triggers automatic deployment
git push origin main
```

The GitHub Action will:
1. Build Next.js app
2. Deploy to Firebase App Hosting
3. Deploy Firebase Functions
4. Deploy Firestore rules
5. Deploy Cloud Run services

### Option B: Manual GitHub Action Trigger
1. Go to GitHub → Actions → "Deploy to Firebase App Hosting"
2. Click **"Run workflow"**
3. Select branch: `main`
4. Click **"Run workflow"**

### Option C: Firebase CLI (Local)
```bash
# Deploy everything
firebase deploy

# Deploy only hosting
firebase deploy --only hosting

# Deploy specific services
firebase deploy --only functions
firebase deploy --only firestore:rules
```

---

## 📁 File Structure for Deployment

```
BetGenie/
├── .github/
│   └── workflows/
│       ├── firebase-apphosting-deploy.yml  # Main deployment workflow
│       └── firebase-deploy.yml             # Legacy (kept for reference)
├── apps/
│   └── web/
│       ├── next.config.ts          # Already configured for export
│       ├── dist/                   # Build output (generated)
│       └── package.json
├── apphosting.yaml                 # Firebase App Hosting config
├── firebase.json                   # Firebase services config
├── .firebaserc                     # Project aliases
└── README.md
```

---

## 🔍 Monitoring Deployments

### GitHub Actions
- Go to: https://github.com/richardmohn/BetGenie/actions
- View live deployment logs
- See build status and errors

### Firebase Console
- **App Hosting:** https://console.firebase.google.com/project/betgenie-ai/apphosting
- **Functions:** https://console.firebase.google.com/project/betgenie-ai/functions
- **Firestore:** https://console.firebase.google.com/project/betgenie-ai/firestore
- **Hosting:** https://console.firebase.google.com/project/betgenie-ai/hosting

### Google Cloud Console
- **Cloud Run:** https://console.cloud.google.com/run?project=betgenie-ai
- **Build History:** https://console.cloud.google.com/cloud-build/builds?project=betgenie-ai

---

## 🔄 Continuous Deployment

### Automatic Triggers
The workflow triggers on:
- ✅ Push to `main` branch
- ✅ Push to `production` branch
- ✅ Manual trigger (workflow_dispatch)

### Rollbacks
If a deployment fails:
1. Go to Firebase Console → App Hosting
2. View **Rollouts**
3. Click on previous successful version
4. Click **"Roll back to this version"**

---

## 🛠️ Troubleshooting

### Build Fails in GitHub Actions
```bash
# Test build locally first
cd apps/web
npm install
npm run build

# Check for errors
```

### "Permission denied" errors
- Check `GCP_SA_KEY` secret is valid
- Service account needs:
  - Firebase Admin
  - Cloud Run Admin
  - Cloud Build Editor
  - Service Account User

### App Hosting not appearing in console
```bash
# Enable experiment
firebase experiments:enable apphosting

# Check backends
firebase apphosting:backends:list
```

### Website shows 404
- Check `dist/index.html` exists after build
- Verify `output: 'export'` in `next.config.ts`
- Check Firebase Hosting rewrites in `firebase.json`

---

## 💰 Cost Estimates

Firebase App Hosting pricing:

| Tier | Cost | Includes |
|------|------|----------|
| **Spark (Free)** | $0 | 10GB bandwidth, 1GB storage, 100K requests/day |
| **Blaze (Pay-as-you-go)** | ~$10-50/mo | Based on usage |

**Typical costs for BetGenie:**
- Firebase App Hosting: $0-20/month
- Firebase Functions: $0-10/month
- Firestore: $0-5/month
- Cloud Run: $10-30/month
- **Total: $10-65/month**

---

## 🎉 After Deployment

### Verify Everything Works

1. **Check website:**
   ```bash
   curl https://betgenie-ai.web.app
   ```

2. **Check API:**
   ```bash
   curl https://api-betgenie-ai.web.app/api/health
   ```

3. **Check Firebase Console:**
   - Go to https://console.firebase.google.com/project/betgenie-ai/apphosting
   - View deployment history
   - Check logs

4. **Run AI Pipeline:**
   ```bash
   cd ai-engine
   python nba_betting_pipeline_firebase.py
   ```
   This syncs picks to Firebase for the web app to display.

---

## 📞 Quick Commands Reference

```bash
# Deploy everything from local
firebase deploy

# Deploy only web
firebase deploy --only hosting

# Deploy only functions
firebase deploy --only functions

# Check deployment status
firebase hosting:channel:list

# View logs
firebase functions:log

# Open console
firebase open hosting

# Test locally before deploying
firebase emulators:start
```

---

## ✅ Deployment Checklist

Before pushing to GitHub:

- [ ] All environment variables added to GitHub Secrets
- [ ] `GCP_SA_KEY` service account key is valid
- [ ] Firebase App Hosting enabled in console
- [ ] GitHub repository connected to Firebase
- [ ] Local build passes (`npm run build`)
- [ ] All files committed (`git status` shows clean)

After deployment:

- [ ] Website loads at https://betgenie-ai.web.app
- [ ] Dashboard shows data (run AI pipeline to populate)
- [ ] All API endpoints respond
- [ ] Firebase Console shows successful deployment

---

## 🚀 NEXT STEPS

1. **Add GitHub Secrets** (5 min)
2. **Enable Firebase App Hosting** (2 min)
3. **Push to GitHub** (1 min)
4. **Watch deployment** (5-10 min)
5. **Verify live site** (2 min)

**Total time to go live: ~20 minutes**

---

**Need help?** Check the GitHub Actions logs for detailed error messages.
