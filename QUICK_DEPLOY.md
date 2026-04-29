# BetGenie — Quick Deployment Guide

Get BetGenie live in 5 minutes.

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Firebase project created (`betgenie-ai`)
- [ ] Firebase CLI installed (`npm install -g firebase-tools`)
- [ ] Logged in to Firebase (`firebase login`)
- [ ] Node.js 18+ installed
- [ ] Git repository cloned

---

## 🚀 Step 1: Build the Web App

```bash
cd apps/web
npm install
npm run build
```

**Expected output:**
```
✓ Compiled successfully
✓ Generating static pages (5/5)
✓ Finalizing page optimization
```

---

## 🚀 Step 2: Deploy to Firebase

### Option A: Quick Deploy (Current Directory)

```bash
# From project root
firebase deploy --only hosting --project betgenie-ai
```

### Option B: Using Deploy Script

**Windows PowerShell:**
```powershell
.\deploy.ps1
```

**Mac/Linux:**
```bash
./deploy.sh
```

---

## 🔑 Service Account Setup (For Python AI Engine)

To enable the Python AI engine to sync with Firebase:

1. **Download Service Account Key:**
   - Go to: https://console.firebase.google.com/project/betgenie-ai/settings/serviceaccounts/adminsdk
   - Click "Generate new private key"
   - Save as `firebase-service-account.json` in project root

2. **Set Environment Variable:**
   
   **Windows PowerShell:**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="./firebase-service-account.json"
   ```
   
   **Mac/Linux:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="./firebase-service-account.json"
   ```

3. **Run AI Pipeline with Firebase Sync:**
   ```bash
   cd ai-engine
   python nba_betting_pipeline_firebase.py
   ```

---

## 🌐 Post-Deployment URLs

After deployment, your app will be live at:

| Service | URL |
|---------|-----|
| **Website** | https://betgenie-ai.web.app |
| **Firebase Console** | https://console.firebase.google.com/project/betgenie-ai |
| **Firestore Database** | https://console.firebase.google.com/project/betgenie-ai/firestore |
| **Realtime Database** | https://console.firebase.google.com/project/betgenie-ai/database |

---

## 🔧 Firebase Configuration Files

### firebase.json
Already configured with:
- Hosting: `apps/web/dist`
- Firestore rules: `firebase/firestore.rules`
- Storage rules: `firebase/storage.rules`
- Functions: `services/functions`

### .firebaserc
```json
{
  "projects": {
    "default": "betgenie-ai",
    "production": "betgenie-ai",
    "staging": "betgenie-ai-staging"
  }
}
```

---

## 🐛 Troubleshooting

### "Firebase CLI not found"
```bash
npm install -g firebase-tools
```

### "Not authenticated"
```bash
firebase login
```

### "Project not found"
```bash
firebase use betgenie-ai
```

### "Build errors"
```bash
cd apps/web
rm -rf .next dist
npm install
npm run build
```

---

## 📊 Verify Deployment

1. **Check website:**
   ```bash
   curl https://betgenie-ai.web.app
   ```

2. **Check Firebase Console:**
   - Go to https://console.firebase.google.com/project/betgenie-ai/hosting
   - See deployment history

3. **Check Realtime Database:**
   - Go to https://console.firebase.google.com/project/betgenie-ai/database
   - Should see data when AI pipeline runs

---

## 🔄 Continuous Deployment (GitHub Actions)

The repository includes `.github/workflows/firebase-deploy.yml` for automatic deployment.

**Setup:**
1. Go to GitHub → Settings → Secrets and variables → Actions
2. Add secret: `GCP_SA_KEY` (service account JSON)
3. Push to `main` branch triggers deployment

---

## 🎯 What Gets Deployed

### Web App (apps/web)
- Landing page with live demo
- Dashboard (shows real picks from Firebase)
- Player profiles
- Betting analysis

### Cloud Services (cloud-services/)
- NBA Data Ingestion (scheduled: hourly)
- Odds Aggregation (scheduled: every 30 min)
- News Monitoring (scheduled: every 15 min)
- AI Analysis (scheduled: daily 6 AM)

### Cloud Functions (services/functions)
- API endpoints: `/api/picks`, `/api/players`, `/api/games`
- Firestore triggers
- Scheduled functions

---

## 💰 Expected Costs

| Service | Free Tier | Est. Monthly Cost |
|---------|-----------|-------------------|
| Firebase Hosting | 10GB/month | $0 |
| Firestore | 50K reads/day | $0-10 |
| Cloud Functions | 2M invocations | $0-20 |
| Cloud Run | 2M requests | $0-50 |
| **Total** | | **$0-80/month** |

---

## ✅ Deployment Complete!

Your BetGenie app is now live at:
**https://betgenie-ai.web.app**

Next steps:
1. Run AI pipeline to populate Firebase with picks
2. Test the dashboard
3. Share the URL!

---

## 📞 Support

If deployment fails:
1. Check Firebase console for errors
2. Run `firebase deploy --debug` for verbose output
3. Check GitHub Issues
