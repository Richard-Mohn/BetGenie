# BetGenie — Technical Architecture

*Last Updated: March 2, 2026*

---

## System Overview

BetGenie is composed of 6 major subsystems that work together to deliver AI-powered betting intelligence:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              BETGENIE PLATFORM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐            │
│  │   WEB APP         │     │   MOBILE APP      │     │   API CLIENTS    │            │
│  │   (Next.js)       │     │   (React Native)  │     │   (3rd Party)    │            │
│  └────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘            │
│           │                        │                         │                      │
│           └────────────────────────┼─────────────────────────┘                      │
│                                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                        API GATEWAY (Express/FastAPI)                     │        │
│  │                  Authentication · Rate Limiting · Routing               │        │
│  └──────────┬──────────────┬──────────────┬──────────────┬────────────────┘        │
│             │              │              │              │                          │
│             ▼              ▼              ▼              ▼                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐              │
│  │  PLAYER       │ │  PREDICTION   │ │  BETTING      │ │  USER         │              │
│  │  INTELLIGENCE │ │  ENGINE       │ │  OPTIMIZER    │ │  SERVICE      │              │
│  │  SERVICE      │ │               │ │               │ │               │              │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘              │
│         │                │                │                │                        │
│         ▼                ▼                ▼                ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                        DATA LAYER                                       │        │
│  │  PostgreSQL · MongoDB · Redis · Elasticsearch                           │        │
│  └──────────────────────────────┬──────────────────────────────────────────┘        │
│                                 │                                                    │
│                                 ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                    AI / ML ENGINE (Python)                               │        │
│  │  Sentiment Analysis · NLP · Performance Prediction · Impact Scoring     │        │
│  └──────────────────────────────┬──────────────────────────────────────────┘        │
│                                 │                                                    │
│                                 ▼                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐        │
│  │                  DATA INGESTION PIPELINE                                 │        │
│  │  News APIs · Social Media · Injury Reports · Court Records              │        │
│  │  Box Scores · Odds Feeds · Team News · Police Blotters                  │        │
│  └─────────────────────────────────────────────────────────────────────────┘        │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Subsystem 1: Data Ingestion Pipeline

The backbone of BetGenie. Continuously collects data from diverse sources.

### Data Categories

| Category | Sources | Frequency | Storage |
|----------|---------|-----------|---------|
| **Player Stats** | NBA API, NFL API, ESPN, Sports Reference | Real-time during games, daily otherwise | PostgreSQL |
| **News & Media** | NewsAPI, Google News, AP, Reuters, TMZ, ESPN, Bleacher Report | Every 15 minutes | MongoDB + Elasticsearch |
| **Social Media** | Twitter/X API, Instagram (public), Reddit | Every 5 minutes for active players | MongoDB |
| **Injury Reports** | Official league injury reports, beat reporter tweets | Real-time | PostgreSQL |
| **Legal/Police** | Court records (public), news scraping for arrests/charges | Hourly | MongoDB |
| **Odds & Lines** | The Odds API, sportsbook feeds | Real-time | Redis + PostgreSQL |
| **Team News** | Trades, coaching changes, roster moves | As available | PostgreSQL |
| **Weather** | OpenWeather API (for outdoor sports) | Pre-game | Redis |
| **Personal Events** | AI-extracted from news, social media, public records | Continuous | MongoDB |

### Ingestion Architecture

```
[News APIs] ──────┐
[Social APIs] ────┤
[Sports APIs] ────┤──► [Message Queue (RabbitMQ/Kafka)] ──► [Processing Workers]
[Web Scrapers] ───┤                                              │
[Odds Feeds] ─────┘                                              ▼
                                                          [NLP Pipeline]
                                                              │
                                                              ▼
                                                    [Entity Extraction]
                                                    [Sentiment Scoring]
                                                    [Event Classification]
                                                              │
                                                              ▼
                                                      [Data Storage]
                                                    [Player Profiles Updated]
```

---

## Subsystem 2: Player Intelligence Service

Maintains a comprehensive, real-time profile for every tracked athlete.

### Player Profile Schema (Simplified)

```json
{
  "player_id": "jamal-murray-den",
  "name": "Jamal Murray",
  "sport": "NBA",
  "team": "Denver Nuggets",
  "position": "PG",
  "impact_score": {
    "overall": 62,
    "physical": 75,
    "emotional": 45,
    "psychological": 55,
    "situational": 70,
    "last_updated": "2026-03-02T14:30:00Z"
  },
  "recent_events": [
    {
      "event_type": "legal_issue",
      "severity": "high",
      "description": "Arrested for DUI on Feb 28, 2026",
      "sources": ["espn.com/article/...", "tmz.com/article/..."],
      "sentiment_score": -0.85,
      "estimated_performance_impact": -0.18,
      "decay_rate": 0.03,
      "date": "2026-02-28",
      "confidence": 0.92
    }
  ],
  "baseline_stats": {
    "ppg": 26.3,
    "rpg": 4.1,
    "apg": 6.8,
    "fg_pct": 0.462,
    "games_played": 55
  },
  "adjusted_projections": {
    "points": { "over_under": 24.5, "recommendation": "UNDER", "confidence": 0.76 },
    "rebounds": { "over_under": 4.5, "recommendation": "HOLD", "confidence": 0.52 },
    "assists": { "over_under": 6.5, "recommendation": "UNDER", "confidence": 0.68 }
  },
  "social_sentiment": {
    "player_activity": "silent",
    "public_sentiment": -0.65,
    "media_tone": -0.78,
    "trending": true
  },
  "factors_active": [
    { "factor": "legal_trouble", "weight": 0.35, "direction": "negative" },
    { "factor": "media_scrutiny", "weight": 0.15, "direction": "negative" },
    { "factor": "home_game", "weight": 0.05, "direction": "positive" },
    { "factor": "rest_days_3", "weight": 0.08, "direction": "positive" }
  ]
}
```

---

## Subsystem 3: AI/ML Prediction Engine

The brain of BetGenie. Multiple models work together.

### Model Architecture

| Model | Purpose | Input | Output |
|-------|---------|-------|--------|
| **Event Classifier** | Categorizes news/events by type and severity | Raw text from news/social | Event type, severity score, player linkage |
| **Sentiment Analyzer** | Scores emotional tone of content about a player | Processed text | Sentiment score (-1 to +1), confidence |
| **Impact Predictor** | Predicts how an event will affect performance | Event type + severity + player history + historical correlations | Performance delta (%), decay curve, duration |
| **Performance Projector** | Generates adjusted stat projections | Baseline stats + all active impact factors | Adjusted projections with confidence intervals |
| **Parlay Optimizer** | Finds optimal parlay combinations | Multiple player projections + correlation analysis | Ranked parlay suggestions with expected value |
| **Confidence Scorer** | Meta-model that scores prediction reliability | All model outputs + data quality signals | Overall confidence rating (0-100) |

### Training Data Strategy

1. **Historical Correlation Dataset**: Backtest 10+ years of personal events against performance data
   - Scrape historical news archives for player events
   - Align with box score data to measure performance deltas
   - Build event-type-to-impact lookup tables

2. **Continuous Learning**: Every game outcome feeds back into models
   - Compare predictions to actual results
   - Adjust weights and parameters
   - Identify new factor patterns

3. **Sport-Specific Models**: Each sport has unique dynamics
   - NBA: Back-to-back fatigue, playoff pressure, All-Star distractions
   - NFL: Short week, bye week effects, playoff implications
   - MLB: Pitching matchups, batting order changes, platoon splits
   - NHL: Line combinations, goalie rotations, travel fatigue
   - Soccer: International duty, transfer windows, manager changes

---

## Subsystem 4: Betting Optimizer

Translates AI predictions into actionable betting intelligence.

### Features

1. **Player Props Analysis**
   - Compare AI projections to sportsbook lines
   - Identify value bets where Impact Score creates edge
   - Show confidence-weighted recommendations

2. **Parlay Builder**
   - Input desired payout → get optimized leg combinations
   - Each leg scored by confidence and impact factor analysis
   - Correlation detection (don't parlay teammates in same game blindly)
   - "Smart Parlay" mode: AI selects highest-value multi-leg combos

3. **Game Predictions**
   - Spread, moneyline, and totals analysis
   - Team-level aggregation of all player Impact Scores
   - Matchup-specific factors (playoff revenge game, rivalry, etc.)

4. **Live Updates**
   - Pre-game alerts when new information surfaces
   - In-game adjustment signals
   - Post-game model accuracy tracking

---

## Subsystem 5: User Service

Handles authentication, subscriptions, preferences, and user experience.

### User Features

- **Dashboard**: Personalized view of today's games with AI insights
- **Watchlist**: Track specific players and get alerts
- **Bet Tracker**: Log and track betting performance
- **Bankroll Manager**: Set limits, track ROI, get discipline alerts
- **Notification Engine**: Push alerts for breaking player news, line moves, and AI signals
- **Subscription Tiers**: Free, Pro, Elite (see Business Model)

---

## Subsystem 6: API Layer

RESTful + WebSocket API for all client applications.

### Key Endpoints (Planned)

```
GET    /api/v1/games/today                    # Today's games with AI analysis
GET    /api/v1/games/:id                      # Detailed game analysis
GET    /api/v1/players/:id                    # Full player profile + Impact Score
GET    /api/v1/players/:id/events             # Recent events affecting player
GET    /api/v1/players/:id/projections        # Stat projections (adjusted)
GET    /api/v1/props/today                    # Today's player props with analysis
GET    /api/v1/props/:id/recommendation       # Specific prop recommendation
POST   /api/v1/parlays/optimize               # Generate optimized parlay
POST   /api/v1/parlays/analyze                # Analyze user-built parlay
GET    /api/v1/sports/:sport/games            # Games by sport
GET    /api/v1/alerts                         # User's active alerts
WS     /api/v1/live                           # Real-time updates stream

# Search
GET    /api/v1/search/players?q=              # Search players
GET    /api/v1/search/events?q=               # Search events

# User
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/user/profile
PUT    /api/v1/user/watchlist
POST   /api/v1/user/bets                      # Log a bet
GET    /api/v1/user/bets/history               # Bet history
GET    /api/v1/user/bankroll                   # Bankroll stats
```

---

## Infrastructure

### Cloud Architecture (AWS)

```
                    ┌─────────────┐
                    │ CloudFront  │ (CDN)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    ALB      │ (Load Balancer)
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  ECS     │ │  ECS     │ │  ECS     │
        │  API     │ │  API     │ │  API     │
        │  Cluster │ │  Cluster │ │  Workers │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
              └────────────┼────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │  RDS     │     │ MongoDB  │     │ ElastiC  │
   │ (Postgres)│    │  Atlas   │     │  ache    │
   └──────────┘     └──────────┘     │ (Redis)  │
                                     └──────────┘
```

### Estimated Monthly Infrastructure Costs (at Scale)

| Service | Cost |
|---------|------|
| ECS (API + Workers) | $800 - $2,000 |
| RDS PostgreSQL | $200 - $500 |
| MongoDB Atlas | $200 - $500 |
| ElastiCache (Redis) | $100 - $300 |
| Elasticsearch | $300 - $600 |
| Data Transfer | $100 - $300 |
| External APIs | $500 - $2,000 |
| ML/GPU (SageMaker) | $500 - $1,500 |
| **Total** | **$2,700 - $7,700/mo** |

---

## Security Considerations

- JWT-based authentication with refresh tokens
- Rate limiting per tier
- Data encryption at rest and in transit
- GDPR/CCPA compliance for user data
- No storage of betting account credentials
- Regular security audits
- SOC 2 compliance roadmap
