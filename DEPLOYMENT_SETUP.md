# BetGenie Deployment Setup — Firebase App Hosting + Google Secret Manager

This guide configures deployment using **Firebase App Hosting** with **Google Secret Manager** for API keys and secrets.

---

## 🏗️ Architecture Overview

```
GitHub Push → Firebase App Hosting → Cloud Run → Live Site
     ↓              ↓                    ↓
   Source      apphosting.yaml      Google Secret Manager
```

**Key Features:**
- ✅ Firebase App Hosting (NOT Firebase Hosting)
- ✅ Google Secret Manager for all API keys
- ✅ Automatic builds on push to GitHub
- ✅ Easy secret rotation without code changes

---

## 🔑 Step 1: Set Up Google Secret Manager

### 1.1 Enable Secret Manager API

```bash
gcloud services enable secretmanager.googleapis.com --project=betgenie-ai
```

### 1.2 Create Secrets

Create secrets for all API keys:

```bash
# Firebase Web API Key
echo -n "your-firebase-web-api-key" | gcloud secrets create firebase-web-api-key \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-

# The Odds API Key
echo -n "your-odds-api-key" | gcloud secrets create odds-api-key \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-

# News API Key
echo -n "your-news-api-key" | gcloud secrets create news-api-key \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-

# OpenAI API Key (for NLP)
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-

# Twitter/X API Bearer Token
echo -n "your-twitter-bearer-token" | gcloud secrets create twitter-bearer-token \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-

# BoltOdds API Key (if needed)
echo -n "9ed66088-9cce-4529-a0c2-f4452aac05cb" | gcloud secrets create boltonds-api-key \
  --project=betgenie-ai \
  --replication-policy="automatic" \
  --data-file=-
```

### 1.3 List All Secrets

```bash
gcloud secrets list --project=betgenie-ai
```

### 1.4 Grant Access to Cloud Run Service Account

```bash
# Get the Cloud Run service account
gcloud iam service-accounts list --project=betgenie-ai

# Grant Secret Manager accessor role
gcloud secrets add-iam-policy-binding firebase-web-api-key \
  --project=betgenie-ai \
  --member="serviceAccount:betgenie-ai@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Repeat for all secrets
```

---

## 🔥 Step 2: Set Up Firebase App Hosting

### 2.1 Enable Firebase App Hosting

```bash
# Login to Firebase
firebase login

# Enable App Hosting experiment
firebase experiments:enable apphosting

# Initialize App Hosting (creates backend)
firebase apphosting:backends:create \
  --project=betgenie-ai \
  --region=us-central1 \
  --root-directory=apps/web
```

### 2.2 Connect GitHub Repository

```bash
# Link GitHub repo to Firebase App Hosting
firebase apphosting:backends:repo:create \
  --project=betgenie-ai \
  --github-repo=richardmohn/BetGenie
```

Or manually in Firebase Console:
1. Go to https://console.firebase.google.com/project/betgenie-ai/apphosting
2. Click "Get Started"
3. Connect GitHub repository
4. Select repository: `richardmohn/BetGenie`

### 2.3 Configure Build Settings

The `apphosting.yaml` file is already configured:

```yaml
runConfig:
  cpu: 1
  memoryMiB: 512
  concurrency: 80
  minInstances: 0
  maxInstances: 10

rootDir: apps/web
runCommand: npm run start

env:
  - variable: NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
    value: betgenie-ai.firebaseapp.com
  - variable: NEXT_PUBLIC_FIREBASE_PROJECT_ID
    value: betgenie-ai
```

### 2.4 Grant Secret Access to App Hosting

```bash
# Grant the App Hosting service account access to secrets
SERVICE_ACCOUNT="betgenie-ai@appspot.gserviceaccount.com"

for SECRET in firebase-web-api-key odds-api-key news-api-key openai-api-key; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --project=betgenie-ai \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
done
```

---

## 🔐 Step 3: Configure GitHub Actions

### 3.1 Add Required GitHub Secrets

Go to GitHub → Settings → Secrets and variables → Actions

**Required Secrets:**

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `GCP_SA_KEY` | Service account JSON | Firebase Console → Project Settings → Service Accounts → Generate new private key |

### 3.2 Service Account Permissions

The service account needs these roles:

```bash
# Grant roles to the service account
gcloud projects add-iam-policy-binding betgenie-ai \
  --member="serviceAccount:your-service-account@betgenie-ai.iam.gserviceaccount.com" \
  --role="roles/firebase.admin"

gcloud projects add-iam-policy-binding betgenie-ai \
  --member="serviceAccount:your-service-account@betgenie-ai.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.admin"

gcloud projects add-iam-policy-binding betgenie-ai \
  --member="serviceAccount:your-service-account@betgenie-ai.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding betgenie-ai \
  --member="serviceAccount:your-service-account@betgenie-ai.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## 🚀 Step 4: Deploy

### 4.1 Push to GitHub

```bash
git add .
git commit -m "Setup Firebase App Hosting with Google Secret Manager"
git push origin main
```

### 4.2 Monitor Deployment

1. Go to GitHub → Actions tab
2. Watch the workflow run
3. Deployment takes 5-10 minutes

### 4.3 Verify Deployment

```bash
# Check App Hosting status
firebase apphosting:backends:list --project=betgenie-ai

# Get live URL
firebase apphosting:backends:get --project=betgenie-ai
```

**Your site will be live at:** `https://betgenie-ai.web.app`

---

## 🔄 Managing Secrets

### Update a Secret

```bash
# Create new version of a secret
echo -n "new-api-key-value" | gcloud secrets versions add odds-api-key \
  --project=betgenie-ai \
  --data-file=-

# Redeploy to use new secret
firebase apphosting:backends:rollout:create \
  --project=betgenie-ai
```

### View Secret Versions

```bash
gcloud secrets versions list odds-api-key --project=betgenie-ai
```

### Access Secrets in Code

**Node.js (Next.js):**
```javascript
// Secrets are automatically injected as env vars
const apiKey = process.env.ODDS_API_KEY;
```

**Python (Cloud Run):**
```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/betgenie-ai/secrets/odds-api-key/versions/latest"
response = client.access_secret_version(request={"name": name})
api_key = response.payload.data.decode("UTF-8")
```

---

## 📁 File Structure

```
BetGenie/
├── apphosting.yaml          # Firebase App Hosting config
├── firebase.json            # Firebase services (NO hosting section)
├── .firebaserc              # Project aliases
├── .github/
│   └── workflows/
│       └── firebase-apphosting-deploy.yml  # GitHub Actions
├── apps/
│   └── web/                 # Next.js app
│       ├── apphosting.yaml  # (optional override)
│       └── package.json
└── cloud-services/          # Python AI services
    └── [service]/
        └── Dockerfile
```

---

## 🛠️ Troubleshooting

### "Backend not found"

```bash
# List backends
firebase apphosting:backends:list --project=betgenie-ai

# Create if missing
firebase apphosting:backends:create --project=betgenie-ai
```

### "Permission denied on secret"

```bash
# Check IAM policy
gcloud secrets get-iam-policy odds-api-key --project=betgenie-ai

# Grant access
SERVICE_ACCOUNT="betgenie-ai@appspot.gserviceaccount.com"
gcloud secrets add-iam-policy-binding odds-api-key \
  --project=betgenie-ai \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"
```

### "Build failed"

```bash
# Test build locally
cd apps/web
npm ci
npm run build

# Check apphosting.yaml syntax
firebase apphosting:backends:validate --project=betgenie-ai
```

### "Secret not accessible"

Make sure the Cloud Run service account has `secretmanager.secretAccessor` role on each secret.

---

## 💰 Cost Optimization

| Service | Config | Monthly Cost |
|---------|--------|--------------|
| Firebase App Hosting | 512Mi, 0-10 instances | $10-50 |
| Secret Manager | 6 secrets | $0.06/secret = $0.36 |
| Cloud Functions | As configured | $5-20 |
| Cloud Run | 4 services, 0-10 instances | $20-80 |
| **Total** | | **$35-150** |

---

## 🎯 Quick Commands Reference

```bash
# Deploy everything manually
firebase deploy --only firestore,functions,storage

# Deploy specific service
firebase deploy --only functions

# View App Hosting logs
firebase apphosting:logs:tail --project=betgenie-ai

# List rollouts
firebase apphosting:backends:rollouts:list --project=betgenie-ai

# Rollback to previous version
firebase apphosting:backends:rollback --project=betgenie-ai

# Open console
firebase open apphosting
```

---

## ✅ Deployment Checklist

Before pushing to GitHub:

- [ ] All secrets created in Google Secret Manager
- [ ] Cloud Run service account has secret access
- [ ] GitHub secret `GCP_SA_KEY` added
- [ ] Firebase App Hosting backend created
- [ ] GitHub repository connected to Firebase
- [ ] Local build passes (`npm run build`)

After deployment:

- [ ] Site loads at https://betgenie-ai.web.app
- [ ] Secrets accessible in Cloud Functions
- [ ] AI pipeline can read/write to Firestore
- [ ] No errors in Firebase Console logs

---

## 🎉 Success!

Your BetGenie app is now deployed with:
- ✅ Firebase App Hosting (modern, scalable)
- ✅ Google Secret Manager (secure, easy to rotate)
- ✅ Automatic GitHub deployments
- ✅ No Firebase Hosting (as requested)

**Live URL:** https://betgenie-ai.web.app

---

## 📞 Support

- Firebase App Hosting Docs: https://firebase.google.com/docs/app-hosting
- Secret Manager Docs: https://cloud.google.com/secret-manager/docs
- GitHub Actions: https://github.com/richardmohn/BetGenie/actions
