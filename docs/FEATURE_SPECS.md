# BetGenie — Feature Specifications

*Last Updated: March 2, 2026*

---

## Feature 1: Player Impact Score (PIS)

### Overview
The Player Impact Score is BetGenie's core innovation — a real-time composite score (0-100) that represents a player's expected performance capacity, factoring in personal, emotional, psychological, and situational variables beyond traditional statistics.

### Score Components

| Component | Weight | Description |
|-----------|--------|-------------|
| **Physical** (0-100) | 30% | Injury status, fatigue (back-to-back games), rest days, physical condition reports |
| **Emotional** (0-100) | 25% | Personal life events (family, relationships, legal), social media sentiment |
| **Psychological** (0-100) | 25% | Media pressure, contract situation, team chemistry, playoff pressure, rivalry games |
| **Situational** (0-100) | 20% | Home/away, opponent strength, weather (outdoor), time zone travel, schedule density |

### Score Interpretation

| Score Range | Label | Betting Signal |
|-------------|-------|----------------|
| 90-100 | **ELITE** | Player likely to exceed expectations. Look for OVER on props |
| 75-89 | **STRONG** | Normal to above-normal performance expected |
| 60-74 | **NEUTRAL** | No strong signal — defer to traditional analysis |
| 45-59 | **CAUTION** | Negative factors present. Consider UNDER on props |
| 0-44 | **ALERT** | Significant negative factors. Strong UNDER signal |

### Decay Model
Events don't affect players forever. Each event type has a **decay curve**:
- **Legal issues**: High initial impact, slow decay (2-4 weeks)
- **Family emergency**: High initial impact, moderate decay (1-2 weeks)
- **Contract dispute**: Moderate impact, very slow decay (ongoing)
- **Social media controversy**: Moderate impact, fast decay (3-5 days)
- **Teammate trade**: Low-moderate impact, slow buildup then decay (2-3 weeks)

### Display
```
┌──────────────────────────────────────────────────┐
│  JAMAL MURRAY  │  PG  │  Denver Nuggets          │
│                                                    │
│  Player Impact Score:  ██████░░░░  62 / 100       │
│                        ▼ CAUTION                   │
│                                                    │
│  Physical:     ████████░░  75  (rest: 3 days)     │
│  Emotional:    █████░░░░░  45  ⚠️ DUI arrest      │
│  Psychological:██████░░░░  55  ⚠️ media scrutiny  │
│  Situational:  ███████░░░  70  (home game)        │
│                                                    │
│  Active Factors:                                   │
│  🔴 Arrested for DUI (Feb 28) — HIGH impact       │
│  🔴 Heavy media scrutiny — MODERATE impact         │
│  🟡 Social media gone silent — MINOR impact        │
│  🟢 3 rest days — POSITIVE impact                  │
│  🟢 Home game — POSITIVE impact                    │
│                                                    │
│  Adjusted Projections:                             │
│  Points:  21.5 (baseline 26.3)  │ Line: 24.5 → UNDER 76% │
│  Rebounds: 3.8 (baseline 4.1)   │ Line: 4.5  → UNDER 62% │
│  Assists:  5.7 (baseline 6.8)   │ Line: 6.5  → UNDER 68% │
└──────────────────────────────────────────────────┘
```

---

## Feature 2: Smart Parlay Builder

### Overview
AI-powered parlay construction that uses Player Impact Scores along with correlation analysis to build optimized multi-leg bets.

### Modes

#### 1. Auto-Build Mode
- User selects: desired payout range, sports, risk tolerance
- AI generates top 3-5 optimized parlays
- Each leg shows: player, prop, recommendation, confidence, active factors

#### 2. Analyze Mode
- User builds their own parlay
- AI scores each leg and the overall parlay
- Highlights weak legs (low confidence)
- Suggests replacements for weak legs
- Shows correlation warnings (e.g., "Two players on same team — correlated outcomes")

#### 3. Explorer Mode
- Browse all today's props sorted by AI confidence
- Filter by sport, confidence level, impact factor type
- One-tap add to parlay

### Parlay Scoring
Each parlay gets a **Parlay Confidence Score** (0-100):
- Average confidence across all legs
- Penalty for correlated legs
- Bonus for diverse sports/games
- Penalty for too many legs (mathematically harder)

### Display
```
┌──────────────────────────────────────────────────────────────┐
│  🎯 SMART PARLAY — AI OPTIMIZED                              │
│  Confidence: 72/100  │  Legs: 4  │  Est. Payout: +850       │
│                                                               │
│  LEG 1: ✅ HIGH CONFIDENCE (81%)                              │
│  Jamal Murray UNDER 24.5 Points                              │
│  PIS: 62  │  Factor: DUI arrest, media scrutiny              │
│                                                               │
│  LEG 2: ✅ HIGH CONFIDENCE (77%)                              │
│  Bobby Portis OVER 18.5 Points                               │
│  PIS: 88  │  Factor: Daughter's promotion, confidence high   │
│                                                               │
│  LEG 3: ✅ MODERATE CONFIDENCE (68%)                          │
│  Luka Doncic OVER 9.5 Assists                                │
│  PIS: 79  │  Factor: Home game, revenge matchup              │
│                                                               │
│  LEG 4: ⚠️ MODERATE CONFIDENCE (61%)                         │
│  Patrick Mahomes UNDER 275.5 Pass Yards                      │
│  PIS: 65  │  Factor: Ankle concern, wind advisory            │
│                                                               │
│  ⚠️ No correlated legs detected                              │
│  💡 Suggestion: Replace Leg 4 with Tyreek Hill OVER 85.5     │
│     receiving yards (confidence: 74%) to improve parlay score │
└──────────────────────────────────────────────────────────────┘
```

---

## Feature 3: Game Analysis Dashboard

### Overview
For every game on today's slate, BetGenie provides a comprehensive AI-powered breakdown.

### Components Per Game

1. **Team Impact Summary**
   - Aggregate PIS for each team (average of all active players)
   - List of key players with notable factors

2. **Spread Analysis**
   - AI-adjusted spread based on Impact Scores
   - Compare to sportsbook spread → identify value

3. **Total (Over/Under) Analysis**
   - AI-projected total based on adjusted player projections
   - Compare to sportsbook total

4. **Key Player Matchups**
   - Head-to-head Impact Score comparison
   - Historical performance in this matchup + current factors

5. **Top Props**
   - 3-5 highest-confidence prop bets for this game
   - Each with full factor breakdown

6. **Breaking News Feed**
   - Real-time feed of any news affecting players in this game
   - AI-tagged with impact classification

---

## Feature 4: Real-Time Alerts

### Alert Types

| Alert Type | Trigger | Priority |
|------------|---------|----------|
| **Breaking News** | Major event detected for watched player | HIGH |
| **Score Change** | Player Impact Score changes by 10+ points | HIGH |
| **Line Move** | Sportsbook line moves 1+ points | MEDIUM |
| **Prop Value** | New high-confidence prop opportunity detected | MEDIUM |
| **Game Start** | Watched game starting in 30 minutes | LOW |
| **Result** | Tracked bet/prediction result available | LOW |

### Delivery Channels
- Push notification (mobile)
- Email digest (configurable frequency)
- In-app notification center
- SMS (Elite tier only)
- Webhook (API tier)

---

## Feature 5: Bet Tracker & Bankroll Management

### Bet Tracking
- Log bets manually or auto-import (future: BetSync integration)
- Track: sport, type (prop/spread/ML/parlay), amount, odds, result
- Auto-calculate: ROI, win rate, units won/lost
- Tag bets: "AI-recommended" vs "personal pick"
- Compare performance: AI-recommended bets vs personal picks

### Bankroll Management
- Set starting bankroll
- Set daily/weekly/monthly limits
- Get alerts when approaching limits
- Suggested bet sizing based on bankroll and confidence
- Streak detection (stop-loss alerts on losing streaks)

---

## Feature 6: Multi-Sport Coverage

### Supported Sports (by launch phase)

| Sport | Phase | Player Count | Key Factors |
|-------|-------|-------------|-------------|
| **NBA** | Phase 2 (MVP) | ~500 | Back-to-back, load management, trade deadline, All-Star |
| **NFL** | Phase 3 | ~1,700 | Short week, bye week, weather, travel, playoff implications |
| **MLB** | Phase 3 | ~1,200 | Pitching matchups, hot/cold streaks, day/night games |
| **NHL** | Phase 3 | ~800 | Back-to-back, goalie rotation, line combinations |
| **College Basketball** | Phase 3 | ~2,000 | Tournament pressure, academic eligibility, coaching |
| **College Football** | Phase 3 | ~3,000 | NIL deals, transfer portal, recruiting distractions |
| **Soccer (EPL, MLS, Liga MX)** | Phase 4 | ~2,000 | International duty, transfer windows, manager changes |
| **UFC/MMA** | Phase 4 | ~500 | Weight cuts, camp changes, social media beefs |
| **Tennis** | Phase 5 | ~200 | Surface preference, travel fatigue, ranking pressure |
| **Golf** | Phase 5 | ~200 | Course history, weather, equipment changes |

---

## Feature 7: Social & Community

### Features
- Share picks with friends (private groups)
- Public pick leaderboard
- Follow top-performing users
- Discussion threads per game
- AI-verified track records (no fake screenshots)
- Tipping / gifting (future)

---

## Feature 8: Content & Education

### Auto-Generated Content
- Daily "Morning Briefing" email with top AI picks
- Pre-game analysis articles (AI-drafted, human-reviewed)
- Weekly "Impact Report" highlighting biggest factor-driven outcomes
- Monthly performance report for subscribers

### Educational Content
- "How to Use Impact Scores" guide
- "Understanding Parlay Math" interactive tool
- "Bankroll Management 101" course
- Sport-specific betting guides
