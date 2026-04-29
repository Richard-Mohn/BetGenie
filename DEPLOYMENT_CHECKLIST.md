# BetGenie — Deployment Checklist

Use this checklist to ensure everything is properly configured for production deployment.

---

## ✅ Pre-Deployment Setup

### 1. Google Cloud Project
- [ ] Firebase project `betgenie-ai` created
- [ ] Billing enabled (pay-as-you-go)
- [ ] Owner permissions confirmed

### 2. Local Prerequisites
- [ ] Node.js 20+ installed
- [ ] `npm` or `pnpm` installed
- [ ] `gcloud` CLI installed and authenticated
- [ ] `firebase` CLI installed (`npm install -g firebase-tools`)
- [ ] `git` installed and configured

### 3. Repository Setup
- [ ] Git repository initialized
- [ ] Remote origin set to GitHub
- [ ] `.gitignore` configured
- [ ] All files committed

---

## 🔑 Authentication & Keys

### 4. Google Cloud Service Account
- [ ] Service account created: `betgenie-ai@appspot.gserviceaccount.com`
- [ ] Key downloaded (JSON format)
- [ ] Key saved securely

### 5. GitHub Secrets (Required)
Go to: https://github.com/richardmohn/BetGenie/settings/secrets/actions

- [ ] `GCP_SA_KEY` — Paste entire service account JSON

### 6. Google Secret Manager (API Keys)
Run these commands to create secrets:

```bash
# Firebase Web API Key (get from Firebase Console > Project Settings > General)
gcloud secrets create firebase-web-api-key \
  --project=betgenie-ai \
  --data-file=<(echo -n "AIza...")

# The Odds API Key (get from https://the-odds-api.com)
gcloud secrets create odds-api-key \
  --project=betgenie-ai \
  --data-file=<(echo -n "your-odds-api-key")

# News API Key (get from https://newsapi.org)
gcloud secrets create news-api-key \
  --project=betgenie-ai \
  --data-file=<(echo -n "your-news-api-key")

# OpenAI API Key (optional, get from https://platform.openai.com)
gcloud secrets create openai-api-key \
  --project=betgenie-ai \
  --data-file=<(echo -n "sk-...")
```

- [ ] `firebase-web-api-key` created
- [ ] `odds-api-key` created
- [ ] `news-api-key` created
- [ ] `openai-api-key` created (optional)

### 7. IAM Permissions
Grant service account access to secrets:

```bash
SERVICE_ACCOUNT="betgenie-ai@appspot.gserviceaccount.com"

for SECRET in firebase-web-api-key odds-api-key news-api-key; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --project=betgenie-ai \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
done
```

- [ ] Secret Manager access granted
- [ ] Cloud Run access granted
- [ ] Firebase Admin access granted

---

## 🚀 Firebase App Hosting Setup

### 8. Enable APIs
```bash
gcloud services enable secretmanager.googleapis.com --project=betgenie-ai
gcloud services enable firebaseapphosting.googleapis.com --project=betgenie-ai
gcloud services enable run.googleapis.com --project=betgenie-ai
gcloud services enable cloudbuild.googleapis.com --project=betgenie-ai
```

- [ ] Secret Manager API enabled
- [ ] Firebase App Hosting API enabled
- [ ] Cloud Run API enabled
- [ ] Cloud Build API enabled

### 9. Initialize Firebase App Hosting
```bash
firebase login
firebase experiments:enable apphosting
firebase apphosting:backends:create \
  --project=betgenie-ai \
  --region=us-central1 \
  --root-directory=apps/web
```

- [ ] Firebase CLI authenticated
- [ ] App Hosting experiment enabled
- [ ] Backend created

### 10. Connect GitHub Repository
```bash
firebase apphosting:backends:repo:create \
  --project=betgenie-ai \
  --github-repo=richardmohn/BetGenie
```

Or manually:
1. Go to https://console.firebase.google.com/project/betgenie-ai/apphosting
2. Click "Get Started"
3. Connect GitHub repository

- [ ] GitHub repository connected
- [ ] App Hosting backend visible in console

---

## 🧪 Pre-Deployment Testing

### 11. Local Build Test
```bash
cd apps/web
npm ci
npm run build
```

- [ ] `npm ci` completes without errors
- [ ] `npm run build` succeeds
- [ ] `dist/` folder created with files

### 12. AI Engine Test
```bash
cd ai-engine
python nba_betting_pipeline.py
```

- [ ] Pipeline runs successfully
- [ ] Predictions generated
- [ ] No API errors

---

## 📤 Deployment

### 13. Push to GitHub
```bash
git add .
git commit -m "Production deployment - Firebase App Hosting setup
git push origin main
```

- [ ] All changes committed
- [ ] Pushed to `main` branch
- [ ] GitHub Actions triggered

### 14. Monitor Deployment
- [ ] GitHub Actions workflow running
- [ ] Build step passed
- [ ] Deploy step passed
- [ ] No errors in logs

Check at: https://github.com/richardmohn/BetGenie/actions

---

## 🌐 Post-Deployment Verification

### 15. Website Live
- [ ] Site loads at https://betgenie-ai.web.app
- [ ] No 404 errors
- [ ] Landing page displays correctly
- [ ] Dashboard accessible

### 16. Firebase Services
- [ ] Firestore accessible
- [ ] Cloud Functions deployed
- [ ] Storage rules active

Check at: https://console.firebase.google.com/project/betgenie-ai

### 17. API Endpoints
Test these endpoints:
```bash
curl https://betgenie-ai.web.app/api/health
curl https://betgenie-ai.web.app/api/picks/today
```

- [ ] Health check returns 200
- [ ] API responds with data

### 18. Secrets Working
- [ ] Website can read Firebase config
- [ ] API calls working (no auth errors)
- [ ] No "permission denied" errors

---

## 📊 AI Pipeline Integration

### 19. Run AI Pipeline with Firebase Sync
```bash
cd ai-engine
python nba_betting_pipeline_firebase.py
```

- [ ] Pipeline executes successfully
- [ ] Data synced to Firestore
- [ ] Predictions visible in Realtime Database

### 20. Verify Data in Firebase
- [ ] Players collection populated
- [ ] Games collection populated
- [ ] Predictions collection populated
- [ ] Daily report published

---

## 🔒 Security Checklist

### 21. Security Rules
- [ ] Firestore rules restrict unauthorized access
- [ ] Storage rules limit file uploads
- [ ] API endpoints require authentication (if applicable)

### 22. Secrets Management
- [ ] No secrets in code
- [ ] All API keys in Secret Manager
- [ ] Service account key secured
- [ ] GitHub Secrets properly configured

---

## 📈 Monitoring & Maintenance

### 23. Set Up Monitoring
- [ ] Firebase Analytics enabled
- [ ] Cloud Monitoring dashboard created
- [ ] Error tracking configured (Sentry recommended)

### 24. Cost Monitoring
- [ ] Budget alert set ($50/month recommended)
- [ ] Billing notifications enabled
- [ ] Cost estimation reviewed

---

## ✅ Final Checks

- [ ] Website loads and functions correctly
- [ ] AI pipeline runs and syncs data
- [ ] All secrets working
- [ ] GitHub Actions deploying automatically
- [ ] Firebase App Hosting backend healthy
- [ ] No critical errors in logs
- [ ] Ready for public access

---

## 🆘 Troubleshooting

### Common Issues

**"Backend not found"**
```bash
firebase apphosting:backends:create --project=betgenie-ai
```

**"Permission denied on secret"**
```bash
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --project=betgenie-ai \
  --member="serviceAccount:betgenie-ai@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**"Build failed"**
```bash
cd apps/web
rm -rf node_modules dist .next
npm ci
npm run build
```

**"GitHub Actions not triggering"**
- Check `.github/workflows/firebase-apphosting-deploy.yml` exists
- Verify `GCP_SA_KEY` secret is added
- Check Actions tab for error logs

---

## 🎉 Success!

Once all items are checked:
- ✅ BetGenie is live at https://betgenie-ai.web.app
- ✅ Automatic deployments on every push to `main`
- ✅ AI pipeline syncing real picks to Firebase
- ✅ Professional GitHub repository with CI/CD

**Share the URL:** https://betgenie-ai.web.app
