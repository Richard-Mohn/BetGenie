# BetGenie — Cloud Run Service Architecture

**Purpose**: Design real-time data ingestion services using Google Cloud Run for scalable, serverless processing.

**Why Cloud Run**:
- Serverless (no server management)
- Auto-scaling (scales to zero when not in use)
- Pay-per-use (only pay for actual compute time)
- Easy integration with Firebase/GCP ecosystem
- Supports Python for AI engine

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GCP Project                              │
│  betgenie-prod (or betgenie-dev for testing)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Cloud Run Services                              │
├─────────────────────────────────────────────────────────────┤
│  1. NBA Data Ingestion Service                              │
│     - Fetches NBA game data from official API               │
│     - Fetches player stats and injury reports               │
│     - Runs every 5 minutes during NBA season               │
│     - Stores to Firestore                                   │
├─────────────────────────────────────────────────────────────┤
│  2. Odds Aggregation Service                                │
│     - Fetches odds from OpticOdds API                       │
│     - Compares across sportsbooks                           │
│     - Detects line movements                                │
│     - Runs every 1 minute during games                      │
│     - Stores to Firestore                                   │
├─────────────────────────────────────────────────────────────┤
│  3. News Monitoring Service                                 │
│     - Fetches news from NewsAPI                             │
│     - Scans for player mentions                             │
│     - Classifies events (legal, family, health, etc.)       │
│     - Runs every 15 minutes                                │
│     - Stores to Firestore                                   │
├─────────────────────────────────────────────────────────────┤
│  4. Social Media Monitoring Service                          │
│     - Fetches tweets from Twitter/X API                     │
│     - Scans for player mentions                             │
│     - Analyzes sentiment                                    │
│     - Runs every 10 minutes                                 │
│     - Stores to Firestore                                   │
├─────────────────────────────────────────────────────────────┤
│  5. AI Analysis Service                                     │
│     - Runs PIS calculation on new data                     │
│     - Runs consensus aggregation                            │
│     - Generates picks and recommendations                   │
│     - Triggered by new data from other services             │
│     - Stores to Firestore                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Firebase Firestore                              │
│  - Real-time database                                       │
│  - Collections: games, players, odds, news, social, picks  │
│  - Triggers Cloud Functions on data changes                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Next.js Dashboard                               │
│  - Real-time updates via Firestore SDK                      │
│  - Displays picks, confidence scores, bet recommendations   │
└─────────────────────────────────────────────────────────────┘
```

---

## Service 1: NBA Data Ingestion Service

**File**: `cloud-services/nba_data_ingestion/main.py`

**Purpose**: Fetch NBA game data, player stats, and injury reports

**Schedule**: Every 5 minutes during NBA season (October - June)

**Python Dependencies**:
```python
requests
google-cloud-firestore
google-cloud-logging
```

**Key Functions**:
- `fetch_nba_games()` - Get today's games from NBA API
- `fetch_player_stats()` - Get player stats for active games
- `fetch_injury_reports()` - Get injury reports
- `store_to_firestore()` - Save data to Firestore

**Environment Variables**:
- `NBA_API_KEY` - Official NBA API key
- `FIRESTORE_PROJECT_ID` - GCP project ID
- `FIRESTORE_COLLECTION` - Firestore collection name

---

## Service 2: Odds Aggregation Service

**File**: `cloud-services/odds_aggregation/main.py`

**Purpose**: Fetch odds from OpticOdds API, compare across sportsbooks

**Schedule**: Every 1 minute during active games

**Python Dependencies**:
```python
requests
google-cloud-firestore
google-cloud-logging
```

**Key Functions**:
- `fetch_odds_from_opticodds()` - Get odds for active games
- `compare_odds_across_books()` - Find best lines
- `detect_line_movement()` - Track line changes
- `store_to_firestore()` - Save odds data

**Environment Variables**:
- `OPTICODDS_API_KEY` - OpticOdds API key
- `FIRESTORE_PROJECT_ID` - GCP project ID
- `FIRESTORE_COLLECTION` - Firestore collection name

---

## Service 3: News Monitoring Service

**File**: `cloud-services/news_monitoring/main.py`

**Purpose**: Fetch news from NewsAPI, scan for player mentions

**Schedule**: Every 15 minutes

**Python Dependencies**:
```python
requests
google-cloud-firestore
google-cloud-logging
newspaper3k  # For article text extraction
```

**Key Functions**:
- `fetch_sports_news()` - Get sports news from NewsAPI
- `extract_player_mentions()` - Find player names in articles
- `classify_event()` - Classify event type (legal, family, health, etc.)
- `calculate_severity()` - Score event severity (0-1)
- `store_to_firestore()` - Save news data

**Environment Variables**:
- `NEWS_API_KEY` - NewsAPI key
- `FIRESTORE_PROJECT_ID` - GCP project ID
- `FIRESTORE_COLLECTION` - Firestore collection name

---

## Service 4: Social Media Monitoring Service

**File**: `cloud-services/social_monitoring/main.py`

**Purpose**: Fetch tweets from Twitter/X API, analyze sentiment

**Schedule**: Every 10 minutes

**Python Dependencies**:
```python
tweepy  # Twitter API wrapper
google-cloud-firestore
google-cloud-logging
textblob  # For sentiment analysis
```

**Key Functions**:
- `fetch_player_tweets()` - Get tweets mentioning players
- `analyze_sentiment()` - Score sentiment (-1 to +1)
- `detect_events()` - Detect personal events from tweets
- `store_to_firestore()` - Save social data

**Environment Variables**:
- `TWITTER_BEARER_TOKEN` - Twitter/X API bearer token
- `TWITTER_API_KEY` - Twitter API key
- `TWITTER_API_SECRET` - Twitter API secret
- `FIRESTORE_PROJECT_ID` - GCP project ID
- `FIRESTORE_COLLECTION` - Firestore collection name

---

## Service 5: AI Analysis Service

**File**: `cloud-services/ai_analysis/main.py`

**Purpose**: Run PIS calculation and consensus aggregation

**Schedule**: Triggered by new data (Cloud Firestore trigger)

**Python Dependencies**:
```python
google-cloud-firestore
google-cloud-functions
google-cloud-logging
```

**Key Functions**:
- `calculate_pis()` - Run Player Impact Score calculation
- `run_consensus()` - Aggregate intelligence sources
- `generate_picks()` - Generate betting recommendations
- `store_to_firestore()` - Save picks and recommendations

**Environment Variables**:
- `FIRESTORE_PROJECT_ID` - GCP project ID
- `FIRESTORE_COLLECTION` - Firestore collection name

---

## Deployment Steps

### 1. Set Up GCP Project

```bash
# Create project (if not exists)
gcloud projects create betgenie-prod

# Set as default
gcloud config set project betgenie-prod

# Enable APIs
gcloud services enable \
  run.googleapis.com \
  firestore.googleapis.com \
  cloudbuild.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudscheduler.googleapis.com
```

### 2. Set Up Firestore

```bash
# Create Firestore database
gcloud firestore databases create \
  --region=us-central1 \
  --type=firestore-native

# Create collections (can be done via Firebase Console)
# - games
# - players
# - odds
# - news
# - social
# - picks
```

### 3. Build and Deploy Services

```bash
# NBA Data Ingestion Service
cd cloud-services/nba_data_ingestion
gcloud run deploy nba-data-ingestion \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=NBA_API_KEY=$NBA_API_KEY,FIRESTORE_PROJECT_ID=betgenie-prod

# Odds Aggregation Service
cd cloud-services/odds_aggregation
gcloud run deploy odds-aggregation \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=OPTICODDS_API_KEY=$OPTICODDS_API_KEY,FIRESTORE_PROJECT_ID=betgenie-prod

# News Monitoring Service
cd cloud-services/news_monitoring
gcloud run deploy news-monitoring \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=NEWS_API_KEY=$NEWS_API_KEY,FIRESTORE_PROJECT_ID=betgenie-prod

# Social Media Monitoring Service
cd cloud-services/social_monitoring
gcloud run deploy social-monitoring \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=TWITTER_BEARER_TOKEN=$TWITTER_BEARER_TOKEN,FIRESTORE_PROJECT_ID=betgenie-prod

# AI Analysis Service
cd cloud-services/ai_analysis
gcloud run deploy ai-analysis \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=FIRESTORE_PROJECT_ID=betgenie-prod
```

### 4. Set Up Cloud Scheduler

```bash
# NBA Data Ingestion - Every 5 minutes
gcloud scheduler jobs create http nba-data-ingestion-schedule \
  --schedule="*/5 * * * *" \
  --time-zone="America/New_York" \
  --uri=$(gcloud run services describe nba-data-ingestion --region=us-central1 --format='value(status.url)') \
  --http-method=POST

# Odds Aggregation - Every 1 minute during games
gcloud scheduler jobs create http odds-aggregation-schedule \
  --schedule="* * * * *" \
  --time-zone="America/New_York" \
  --uri=$(gcloud run services describe odds-aggregation --region=us-central1 --format='value(status.url)') \
  --http-method=POST

# News Monitoring - Every 15 minutes
gcloud scheduler jobs create http news-monitoring-schedule \
  --schedule="*/15 * * * *" \
  --time-zone="America/New_York" \
  --uri=$(gcloud run services describe news-monitoring --region=us-central1 --format='value(status.url)') \
  --http-method=POST

# Social Media Monitoring - Every 10 minutes
gcloud scheduler jobs create http social-monitoring-schedule \
  --schedule="*/10 * * * *" \
  --time-zone="America/New_York" \
  --uri=$(gcloud run services describe social-monitoring --region=us-central1 --format='value(status.url)') \
  --http-method=POST
```

---

## Cost Estimates

**Cloud Run Pricing**:
- $0.40 per million requests
- $0.000025 per GB-second (CPU, memory)
- Free tier: 2 million requests/month, 400,000 GB-seconds/month

**Estimated Monthly Costs**:
- NBA Data Ingestion (every 5 min): ~8,640 requests/month = $0.003
- Odds Aggregation (every 1 min): ~43,200 requests/month = $0.017
- News Monitoring (every 15 min): ~2,880 requests/month = $0.001
- Social Media (every 10 min): ~4,320 requests/month = $0.002
- AI Analysis (triggered): ~1,000 requests/month = $0.0004
- **Total**: ~$0.02/month (well within free tier)

**Firestore Pricing**:
- $0.18 per GB stored
- $0.06 per 100,000 reads
- $0.18 per 100,000 writes
- Free tier: 1 GB stored, 50,000 reads/day, 20,000 writes/day

**Estimated Monthly Costs**:
- Storage: ~1 GB = $0.18
- Reads: ~500,000 = $0.30
- Writes: ~200,000 = $0.36
- **Total**: ~$0.84/month

**Total Estimated Cost**: ~$1/month (within free tier limits)

---

## Security Considerations

1. **IAM Roles**: Use least-privilege IAM roles for each service
2. **Secret Manager**: Store API keys in Secret Manager, not environment variables
3. **VPC Connector**: Use VPC Connector for private service communication
4. **Authentication**: Require authentication for service-to-service calls
5. **Logging**: Enable Cloud Logging for audit trails

---

## Monitoring

**Cloud Logging**:
- All services log to Cloud Logging
- Set up log-based metrics for monitoring
- Create alerts for service failures

**Cloud Monitoring**:
- Monitor service latency
- Monitor error rates
- Monitor request counts
- Set up uptime checks

---

## Next Steps

1. Create GCP project if not exists
2. Enable required APIs
3. Set up Firestore database
4. Create service directories and code
5. Deploy services to Cloud Run
6. Set up Cloud Scheduler jobs
7. Test end-to-end data flow
8. Monitor and optimize

---

**Document Status**: Architecture Complete - Ready for Implementation  
**Last Updated**: April 28, 2026  
**Next**: Create service code and deploy
