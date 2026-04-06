# BetGenie — Data Sources & API Strategy

*Last Updated: March 2, 2026*

---

## Data Source Catalog

### Tier 1: Sports Performance Data (Core Stats)

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **NBA API (stats.nba.com)** | Player stats, box scores, schedules, rosters | Free | Moderate (headers required) | P0 |
| **ESPN API (unofficial)** | Scores, schedules, standings, player info | Free | Moderate | P0 |
| **Sports Reference / Basketball Reference** | Historical stats, advanced metrics | Scraping (respect robots.txt) | Slow, respectful scraping | P1 |
| **nfl.com / NFL API** | NFL stats, schedules, depth charts | Free/Limited | Moderate | P0 (Phase 3) |
| **MLB Stats API** | Baseball stats, pitch data | Free | Generous | P1 (Phase 3) |
| **NHL API** | Hockey stats, goalie data | Free | Generous | P1 (Phase 3) |
| **Sportradar** | Official league data (premium) | $$$ ($1K-10K/mo) | High | P2 (Phase 4+) |
| **Stats Perform / Opta** | Advanced analytics | $$$ | High | P2 (Phase 5) |

### Tier 2: Odds & Lines Data

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **The Odds API** | Live odds from 40+ sportsbooks | Free tier: 500 req/mo; Paid: $20-80/mo | Per-plan | P0 |
| **DraftKings API (unofficial)** | DK-specific lines and props | Scraping | Careful rate limits | P1 |
| **FanDuel API (unofficial)** | FD-specific lines and props | Scraping | Careful rate limits | P1 |
| **Pinnacle API** | Sharp lines (gold standard) | Free for affiliates | Moderate | P0 |
| **BetOnline API** | Additional odds source | Affiliate | Moderate | P2 |

### Tier 3: News & Media (The BetGenie Differentiator)

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **NewsAPI.org** | Aggregated news from 150K+ sources | Free: 100 req/day; Paid: $449/mo | Per-plan | P0 |
| **Google News RSS** | Google-curated news feeds | Free | Respectful scraping | P0 |
| **Associated Press API** | Breaking news | $$$ | High | P2 |
| **Reuters API** | Breaking news | $$$ | High | P2 |
| **TMZ (scraping)** | Celebrity/athlete personal news | Scraping | Careful, respectful | P1 |
| **ESPN (scraping)** | Sports news, injury reports | Scraping | Moderate | P0 |
| **Bleacher Report (scraping)** | Sports analysis, rumors | Scraping | Moderate | P1 |
| **The Athletic (scraping)** | Deep-dive analysis | Scraping (paywall challenge) | Limited | P2 |
| **Local beat reporters (aggregated)** | Team-specific insider info | Twitter/X API | Per API limits | P1 |

### Tier 4: Social Media & Sentiment

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **Twitter/X API v2** | Player tweets, mentions, sentiment | Free: basic; $100/mo: Pro | 300-1500 req/15min | P0 |
| **Reddit API** | Team subreddit sentiment, breaking news | Free | 60 req/min | P1 |
| **Instagram Graph API** | Player post activity (public only) | Free | 200 calls/hour | P2 |
| **YouTube Data API** | Press conferences, interviews | Free (quota-based) | 10K units/day | P2 |
| **TikTok API** | Player content, fan reactions | Limited access | Varies | P3 |

### Tier 5: Personal & Legal Data

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **PACER (Federal Courts)** | Federal court records | $0.10/page | N/A | P2 |
| **State court records** | State-level legal records | Varies by state | N/A | P2 |
| **Police blotter scraping** | Local arrest records | Scraping | Respectful | P2 |
| **TMZ / Gossip sites** | Celebrity arrests, incidents | Scraping | Careful | P1 |
| **Transaction records (public)** | Contract info, fines | Via news + league sources | N/A | P1 |
| **Wikipedia / Wikidata** | Player bios, personal info | Free API | Generous | P1 |

### Tier 6: Contextual / Environmental

| Source | Data Type | Cost | Rate Limits | Priority |
|--------|-----------|------|-------------|----------|
| **OpenWeather API** | Game-day weather (outdoor sports) | Free: 1K/day; $40/mo | Per-plan | P1 |
| **Google Maps API** | Travel distance calculations | $200 credit/mo | Per-plan | P2 |
| **Team schedule data** | Back-to-back detection, rest days | From sports APIs | Included | P0 |
| **Venue data** | Arena/stadium info, altitude, etc. | Static database | N/A | P1 |

---

## API Integration Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION ORCHESTRATOR                    │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  │
│  │ Scheduled  │  │  Webhook   │  │  Streaming  │  │  Manual  │  │
│  │  Jobs      │  │  Listeners │  │  Consumers  │  │  Trigger │  │
│  │ (cron)     │  │            │  │  (Twitter)  │  │          │  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └────┬─────┘  │
│        │               │               │              │         │
│        └───────────────┬┴───────────────┘              │         │
│                        ▼                               │         │
│              ┌──────────────────┐                      │         │
│              │   Rate Limiter   │◄─────────────────────┘         │
│              │   & Scheduler    │                                │
│              └────────┬─────────┘                                │
│                       ▼                                          │
│              ┌──────────────────┐                                │
│              │  Source Adapter  │  (One per API/source)          │
│              │  Factory         │                                │
│              └────────┬─────────┘                                │
│                       ▼                                          │
│              ┌──────────────────┐                                │
│              │  Data Normalizer │  (Standardize to schema)      │
│              └────────┬─────────┘                                │
│                       ▼                                          │
│              ┌──────────────────┐                                │
│              │  Message Queue   │  (RabbitMQ / Kafka)           │
│              └────────┬─────────┘                                │
│                       ▼                                          │
│         ┌─────────────┼─────────────┐                           │
│         ▼             ▼             ▼                           │
│  ┌────────────┐ ┌──────────┐ ┌──────────┐                     │
│  │  NLP       │ │  Stats   │ │  Odds    │                     │
│  │  Worker    │ │  Worker  │ │  Worker  │                     │
│  └─────┬──────┘ └────┬─────┘ └────┬─────┘                     │
│        │             │            │                             │
│        └─────────────┼────────────┘                             │
│                      ▼                                          │
│             ┌──────────────────┐                                │
│             │   Data Storage   │                                │
│             └──────────────────┘                                │
└──────────────────────────────────────────────────────────────────┘
```

---

## NLP Pipeline Detail

### Stage 1: Entity Extraction
- Identify **player names** mentioned in text
- Link to player database (fuzzy matching for nicknames: "KD" → Kevin Durant)
- Identify **teams**, **events**, **locations**

### Stage 2: Event Classification
Classify extracted events into categories:

| Category | Examples | Typical Impact |
|----------|----------|----------------|
| `legal_arrest` | DUI, assault, domestic violence | High negative (-15 to -25%) |
| `legal_suspension` | League suspension, PED violation | Very high negative (-20 to -40%) |
| `legal_investigation` | Under investigation, lawsuit | Moderate negative (-5 to -15%) |
| `family_positive` | Child born, marriage, family achievement | Mild positive (+2 to +8%) |
| `family_negative` | Divorce, family death, family illness | High negative (-10 to -20%) |
| `health_injury` | Injury report, surgery, illness | Variable (-5 to -100%) |
| `health_recovery` | Return from injury, cleared to play | Moderate positive (+5 to +10%) |
| `financial_positive` | New contract, endorsement deal | Mild positive (+3 to +7%) |
| `financial_negative` | Contract dispute, fine, financial trouble | Moderate negative (-5 to -12%) |
| `team_trade` | Player traded, teammate traded | Variable (-10 to +10%) |
| `team_coaching` | Coach fired/hired, scheme change | Variable (-5 to +5%) |
| `social_controversy` | Social media beef, public criticism | Moderate negative (-5 to -15%) |
| `social_positive` | Community service, award, fan love | Mild positive (+1 to +5%) |
| `performance_streak` | Hot/cold streak analysis | Variable |
| `media_pressure` | Heavy media attention, criticism | Moderate negative (-3 to -8%) |

### Stage 3: Sentiment Scoring
- Score each article/post: -1.0 (very negative) to +1.0 (very positive)
- Aggregate across sources for overall sentiment
- Track sentiment trajectory (improving/declining)

### Stage 4: Impact Estimation
- Map event type + severity to historical performance data
- Calculate expected performance delta
- Assign confidence interval
- Calculate decay curve (how quickly impact fades)

---

## Data Quality & Validation

### Multi-Source Verification
- Require 2+ sources for HIGH impact events before scoring
- Single-source events flagged as "unverified" with reduced weight
- Human review queue for critical/high-impact events

### False Positive Prevention
- NLP disambiguation (Jamal Murray the player vs. Jamal Murray a random person)
- Satire/joke detection for social media
- Recency validation (don't resurface old events)
- Duplicate detection across sources

### Data Freshness
| Data Type | Max Staleness | Refresh Frequency |
|-----------|--------------|-------------------|
| Odds/Lines | 30 seconds | Real-time stream |
| Breaking news | 5 minutes | Every 5 min polling |
| Social media | 15 minutes | Every 5-15 min |
| Player stats | 1 hour | Post-game + daily |
| Impact Scores | 30 minutes | On-event + scheduled |
| Legal records | 24 hours | Daily scan |

---

## API Budget Estimate (Monthly)

### Phase 1-2 (MVP)

| API | Tier | Monthly Cost |
|-----|------|-------------|
| NewsAPI | Business | $449 |
| The Odds API | Starter | $20 |
| Twitter/X API | Basic | $100 |
| OpenWeather | Free | $0 |
| Reddit API | Free | $0 |
| NBA/ESPN APIs | Free | $0 |
| **Total** | | **~$570/mo** |

### Phase 3-4 (Scale)

| API | Tier | Monthly Cost |
|-----|------|-------------|
| NewsAPI | Business | $449 |
| The Odds API | Pro | $80 |
| Twitter/X API | Pro | $100 |
| OpenWeather | Standard | $40 |
| Sports data (premium) | Various | $500 |
| Additional news sources | Various | $200 |
| **Total** | | **~$1,370/mo** |

### Phase 5 (Enterprise)

| API | Tier | Monthly Cost |
|-----|------|-------------|
| Sportradar | Custom | $3,000+ |
| Full news stack | Enterprise | $1,500 |
| All social APIs | Pro/Enterprise | $500 |
| All odds sources | Premium | $300 |
| **Total** | | **~$5,300+/mo** |

---

## Legal & Compliance Notes

- **Web Scraping**: Respect robots.txt, rate limit, don't overload servers
- **Social Media**: Use official APIs, comply with ToS, respect privacy settings
- **Court Records**: Public records are fair game, but present responsibly
- **Player Privacy**: Only use publicly available information. No private data
- **GDPR/CCPA**: User data (subscribers) handled with full compliance
- **Gambling Disclaimers**: BetGenie is an information platform, not a sportsbook. All gambling disclaimers required.
