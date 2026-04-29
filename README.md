# BetGenie 🎯

## AI-Powered Sports Betting Intelligence Platform

**By Mohn Empire**

BetGenie is a next-generation sports analytics platform that goes beyond traditional statistics. Using AI-driven sentiment analysis, real-time news aggregation, and psychological profiling, BetGenie analyzes the **whole player** — not just their box scores — to deliver smarter, more accurate predictions for player props, parlays, and game outcomes.

### What Makes BetGenie Different?

Every existing platform (Action Network, PrizePicks, Unabated, etc.) focuses on **numbers**: historical stats, line movements, odds comparisons.

**BetGenie analyzes the human behind the numbers.**

- Did a player just get arrested? Their performance WILL be affected.
- Is a player's child sick? That weighs on anyone.
- Did they just sign a massive endorsement deal? Confidence is sky-high.
- Are they going through a divorce? Focus is compromised.
- Did their teammate just get traded? Chemistry changes everything.

BetGenie's AI scans thousands of sources in real-time to build a **Player Impact Score** that accounts for physical, emotional, psychological, and situational factors — then translates that into actionable betting intelligence.

---

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Firebase CLI (`npm install -g firebase-tools`)
- Google Cloud SDK (`gcloud` CLI)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/betgenie.git
cd betgenie

# Install frontend dependencies
cd website
npm install

# Install Cloud Functions dependencies
cd ../services/functions
npm install

# (Optional) Install AI engine dependencies
cd ../../ai-engine
pip install -r requirements.txt
```

### Local Development

```bash
# Start the Next.js frontend
cd website
npm run dev

# Start Firebase emulators (Firestore, Functions, Hosting)
firebase emulators:start

# Run AI engine to generate picks
cd ai-engine
python nba_betting_pipeline.py
```

---

## 📦 Deployment — Firebase App Hosting

### Quick Deploy (One Command)

```bash
# Run the setup script
./setup-and-deploy.sh        # Mac/Linux
.\setup-and-deploy.ps1      # Windows PowerShell
```

This script will:
1. ✅ Check prerequisites (gcloud, firebase, git)
2. ✅ Enable required Google Cloud APIs
3. ✅ Set up Google Secret Manager for API keys
4. ✅ Configure IAM permissions
5. ✅ Initialize Firebase App Hosting
6. ✅ Build and deploy the Next.js app
7. ✅ Commit and push to GitHub

### Manual Deployment

**Prerequisites:**
- Google Cloud SDK (`gcloud`)
- Firebase CLI (`firebase-tools`)
- Node.js 20+
- Git

**Step 1: Enable APIs**
```bash
gcloud services enable secretmanager.googleapis.com --project=betgenie-ai
gcloud services enable firebaseapphosting.googleapis.com --project=betgenie-ai
```

**Step 2: Configure Secrets**
```bash
# Create secrets in Google Secret Manager
gcloud secrets create odds-api-key --project=betgenie-ai --data-file=<(echo -n "your-key")
gcloud secrets create news-api-key --project=betgenie-ai --data-file=<(echo -n "your-key")
```

**Step 3: Deploy**
```bash
# Firebase App Hosting (automatic from apphosting.yaml)
firebase apphosting:backends:create --project=betgenie-ai

# Firebase Services
firebase deploy --only functions,firestore,storage --project=betgenie-ai
```

### GitHub Actions (Automatic)

Push to `main` branch triggers automatic deployment:

1. Go to GitHub → Settings → Secrets
2. Add `GCP_SA_KEY` (service account JSON)
3. Push code: `git push origin main`
4. Monitor at: https://github.com/richardmohn/BetGenie/actions

**Live URL:** https://betgenie-ai.web.app

### Cloud Run Services

Four microservices run on Google Cloud Run:

1. **NBA Data Ingestion** - Fetches games, players, stats
2. **Odds Aggregation** - Aggregates odds from sportsbooks
3. **News Monitoring** - Monitors RSS feeds for player news
4. **AI Analysis** - Runs AI analysis on data

**Deploy Cloud Run Services:**
```bash
# Build and deploy each service
cd cloud-services/nba_data_ingestion
gcloud builds submit --tag gcr.io/betgenie-ai/nba_data_ingestion
gcloud run deploy nba_data_ingestion \
  --image gcr.io/betgenie-ai/nba_data_ingestion \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🏗️ Project Structure

```
betgenie/
├── apps/                    # Application workspaces
│   ├── web/                # Next.js web application
│   │   ├── src/
│   │   │   ├── app/        # Next.js app router pages
│   │   │   ├── components/ # React components
│   │   │   └── lib/        # Firebase client SDK
│   │   ├── public/         # Static assets
│   │   └── package.json
│   └── flutter/            # Flutter mobile app (Android/iOS)
│       └── lib/
├── packages/               # Shared packages
│   └── shared/             # Shared types, utilities, constants
│       ├── src/
│       └── package.json
├── services/               # Backend services
│   └── functions/          # Firebase Cloud Functions
│       ├── src/
│       │   └── index.ts    # Express API endpoints
│       └── package.json
├── cloud-services/         # Cloud Run microservices
│   ├── nba_data_ingestion/
│   ├── odds_aggregation/
│   ├── news_monitoring/
│   └── ai_analysis/
├── ai-engine/              # Python AI/ML engine
│   ├── nba_betting_pipeline.py
│   ├── guaranteed_picks_engine.py
│   ├── jarvis_intelligence.py
│   └── ...
├── firebase/               # Firebase configuration
│   ├── firestore.rules
│   ├── firestore.indexes.json
│   └── storage.rules
├── .firebaserc             # Firebase project aliases
├── firebase.json           # Firebase config
├── .github/
│   └── workflows/
│       └── firebase-deploy.yml
├── docs/                   # Documentation
├── DEPLOYMENT.md           # Deployment guide
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the `website` directory:

```env
# Firebase
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=betgenie-ai
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# APIs
ODDS_API_KEY=your_odds_api_key
BALLDONTLIE_API_KEY=your_balldontlie_key
NEWS_API_KEY=your_news_api_key
```

See `.env.example` for all available variables.

---

## 📊 API Endpoints

### Cloud Functions API

- `GET /api/health` - Health check
- `GET /api/picks/today` - Today's guaranteed picks
- `GET /api/parlays/today` - Today's parlay recommendations
- `GET /api/kickers/today` - Today's kicker bets
- `GET /api/games/today` - Today's NBA games
- `GET /api/players/:playerId` - Player details
- `GET /api/news/recent` - Recent news events
- `GET /api/report/today` - Full daily betting report
- `POST /api/jarvis/query` - Jarvis AI query
- `GET /api/dual-strategy/today` - Dual bet strategy

---

## 🤖 AI Engine Features

### Player Impact Score (PIS)
- **Physical Factors**: Injuries, fatigue, travel
- **Emotional Factors**: Personal events, family issues
- **Psychological Factors**: Confidence, motivation, stress
- **Situational Factors**: Contract status, trade rumors

### Betting Intelligence
- **Guaranteed Picks**: 70%+ confidence player props
- **Optimized Parlays**: Monte Carlo simulation for win rates
- **Kicker Bets**: High-payout long shots with +EV
- **Dual Strategy**: Guaranteed + kicker combo bets
- **Jarvis Intelligence**: AI-powered betting insights

---

## 📈 Performance

### AI Engine Results (Latest Run)
- **Games Analyzed**: 10 NBA games
- **Guaranteed Picks**: 4 (93%, 88%, 81%, 80% confidence)
- **Top Parlay**: 4-leg, +1228 odds, 64.5% win rate
- **Dual Strategy**: +$149.26 expected value on $27.50 stake

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is proprietary software. All rights reserved by Mohn Empire.

---

## 📞 Contact

**Mohn Empire**
- Website: [mohnempire.com](https://mohnempire.com)
- Email: contact@mohnempire.com

---

## 🙏 Acknowledgments

- NBA data provided by [BoltOdds API](https://boltdodds.com)
- News aggregation via [NewsAPI](https://newsapi.org)
- Built with [Firebase](https://firebase.google.com)
- AI powered by [OpenAI](https://openai.com) and custom models

- [Competitive Analysis](docs/COMPETITIVE_ANALYSIS.md)
- [Mission & Vision](docs/MISSION_VISION.md)
- [Product Roadmap](docs/ROADMAP.md)
- [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Feature Specifications](docs/FEATURE_SPECS.md)
- [Business Model](docs/BUSINESS_MODEL.md)
- [Data Sources & API Strategy](docs/DATA_SOURCES.md)

---

### Tech Stack (Planned)

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14+ / React / Tailwind CSS |
| Mobile | React Native / Expo |
| Backend API | Node.js (Express) / Python (FastAPI) |
| AI/ML Engine | Python / TensorFlow / OpenAI API / LangChain |
| NLP & Sentiment | spaCy / BERT / Custom fine-tuned models |
| Database | PostgreSQL (structured) / MongoDB (unstructured) / Redis (cache) |
| Search | Elasticsearch (news/articles indexing) |
| Real-time | WebSockets / Server-Sent Events |
| Scraping/Data | Scrapy / BeautifulSoup / News APIs |
| Infrastructure | AWS / Docker / Kubernetes |
| CI/CD | GitHub Actions |
| Monitoring | Datadog / Sentry |

---

### Project Status: **Phase 1 — Development & Deployment**

*Last Updated: April 28, 2026*

**Current Progress:**
- ✅ AI Engine fully functional (NBA betting pipeline, guaranteed picks, parlays, kickers)
- ✅ Next.js frontend built and ready for deployment
- ✅ Firebase Cloud Functions API implemented
- ✅ Cloud Run microservices scaffolded (4 services)
- ✅ GitHub Actions CI/CD workflow configured
- ⏳ Firebase project setup (requires manual creation)
- ⏳ Production deployment pending Firebase project
