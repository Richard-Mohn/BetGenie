# BetGenie Deployment Status

## ✅ Completed

### Project Setup
- ✅ Firebase project `betgenie-ai` created
- ✅ Firebase App Hosting experiment enabled
- ✅ GitHub repository created: https://github.com/Richard-Mohn/BetGenie
- ✅ All code pushed to GitHub
- ✅ `apphosting.yaml` configured (MohnShop pattern)
- ✅ `firebase.json` configured (no hosting section)
- ✅ Next.js app builds successfully
- ✅ GitHub Actions workflows removed (using Firebase native integration)

### Configuration Files
- ✅ `apphosting.yaml` — Firebase App Hosting config
- ✅ `firebase.json` — Firestore, Functions, Storage (no hosting)
- ✅ `.firebaserc` — Project aliases configured
- ✅ `DEPLOYMENT.md` — Updated with Firebase App Hosting instructions

---

## ⚠️ Blocking Issues

### 1. Firebase Blaze Plan Required

**Error:** Firebase project must be on Blaze (pay-as-you-go) plan for App Hosting

**Action Required:**
1. Go to: https://console.firebase.google.com/project/betgenie-ai/usage/details
2. Click "Upgrade" to Blaze plan
3. Add payment method (Google Cloud billing)
4. Blaze plan is pay-as-you-go, no monthly commitment

**Why:** App Hosting requires Cloud Run, which is only available on Blaze plan

---

## 📋 Next Steps (After Blaze Upgrade)

### Step 1: Deploy Firebase Services
```bash
# Deploy Firestore rules and indexes
firebase deploy --only firestore:rules,firestore:indexes --project betgenie-ai

# Deploy Storage rules
firebase deploy --only storage:rules --project betgenie-ai

# Deploy Cloud Functions
cd services/functions
npm ci
npm run build
cd ../..
firebase deploy --only functions --project betgenie-ai
```

### Step 2: Set Up Firebase App Hosting Backend
```bash
# Create App Hosting backend
firebase apphosting:backends:create \
  --backend betgenie \
  --primary-region us-central1 \
  --root-dir apps/web \
  --project betgenie-ai
```

### Step 3: Connect GitHub Repository (Native Integration)
1. Go to Firebase Console: https://console.firebase.google.com/project/betgenie-ai/apphosting
2. Click "Get Started"
3. Click "Connect GitHub"
4. Authorize Firebase to access your GitHub
5. Select repository: `Richard-Mohn/BetGenie`
6. Select branch: `master`

### Step 4: Automatic Deployment
- Firebase App Hosting will watch your GitHub repository
- Every push to `master` triggers automatic build and deploy
- Uses `apphosting.yaml` for configuration
- No GitHub Actions needed

---

## 🔐 API Keys & Secrets (After Deployment)

### Google Secret Manager
```bash
# Create secrets for API keys
gcloud secrets create odds-api-key --project=betgenie-ai --data-file=<(echo -n "your-key")
gcloud secrets create news-api-key --project=betgenie-ai --data-file=<(echo -n "your-key")
gcloud secrets create openai-api-key --project=betgenie-ai --data-file=<(echo -n "your-key")
```

### Grant IAM Permissions
```bash
SERVICE_ACCOUNT="betgenie-ai@appspot.gserviceaccount.com"

for SECRET in odds-api-key news-api-key openai-api-key; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --project=betgenie-ai \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
done
```

---

## 🌐 Final URLs

After deployment:
- **Web App:** https://betgenie-ai.web.app
- **Firebase Console:** https://console.firebase.google.com/project/betgenie-ai
- **GitHub Repository:** https://github.com/Richard-Mohn/BetGenie

---

## 📊 Architecture

```
GitHub Push → Firebase App Hosting (Native Integration) → Cloud Run → Live Site
     ↓                    ↓                                      ↓
   Source           apphosting.yaml                     Google Secret Manager
```

**No GitHub Actions needed** — Firebase handles everything natively.

---

## 💰 Cost Estimates (Blaze Plan)

| Service | Estimated Cost |
|---------|---------------|
| Firebase App Hosting | $10-50/month |
| Cloud Functions | $5-20/month |
| Firestore | $5-15/month |
| Storage | $0-5/month |
| **Total** | **$20-90/month** |

---

## ✅ Summary

**What's Done:**
- Project created and configured
- Code pushed to GitHub
- Configuration files ready
- Documentation complete

**What You Need to Do:**
1. Upgrade Firebase to Blaze plan: https://console.firebase.google.com/project/betgenie-ai/usage/details
2. Run deployment commands (see above)
3. Connect GitHub in Firebase Console
4. Add API keys to Google Secret Manager

**After That:**
- Every push to GitHub automatically deploys
- No GitHub Actions needed
- Everything managed by Firebase
