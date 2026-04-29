# BetGenie — 2026 Betting Exchange API Research

**Research Date**: April 28, 2026  
**Purpose**: Identify US-legal "Big Dog" access routes for direct market access betting

---

## Executive Summary

**Key Finding**: The US betting landscape has shifted significantly in 2026. US-based exchanges now offer API access that rivals international platforms like Betfair, making offshore structures unnecessary for initial deployment.

**Recommended Stack**:
- **Primary Data Aggregator**: OpticOdds API (1M+ odds/sec, 100+ sportsbooks)
- **US Exchange for Execution**: Sporttrade (CFTC-regulated, 2% commission)
- **Alternative US Exchange**: ProphetX (Sweepstakes model, 40+ states)
- **Odds Comparison**: TheRundown API (15+ sportsbooks, prediction markets)

---

## 1. US Betting Exchanges (The "Big Dogs" - Legal Route)

### Sporttrade
**Status**: Primary Recommendation for US Deployment

**Key Features**:
- Exchange model (peer-to-peer betting)
- 2% commission on winning bets only (no vig on losses)
- Moving toward CFTC regulation as "Designated Contract Market"
- Market-driven pricing (0-100% implied probabilities)
- API access for algorithmic trading

**Regulatory Status**:
- Operating as a prediction market/exchange
- CFTC designation in progress (stock-market-like regulation)
- Available in multiple US states

**API Status**:
- REST API for odds and bet placement
- WebSocket for real-time updates
- Documentation available for developers

**Pros**:
- Lowest effective cost (2% vs 10%+ vig on retail books)
- Legal US operation
- No winner limitations (unlike retail books)
- API access for automation

**Cons**:
- Liquidity still growing (not as deep as Betfair)
- Limited to supported states
- API documentation less mature than Betfair

**Integration Priority**: HIGH

---

### ProphetX (formerly Prophet Exchange)
**Status**: Alternative US Route

**Key Features**:
- Peer-to-peer betting exchange
- Innovative sweepstakes model (legal in 40+ states)
- Mobile app + web platform
- Exchange-style pricing

**Regulatory Status**:
- Sweepstakes model bypasses traditional gambling restrictions
- Available in nearly 40 US states
- Not subject to state-by-state sports betting laws

**API Status**:
- Limited public API documentation
- May require partnership for API access
- Focus appears to be on consumer app

**Pros**:
- Broadest US availability (40+ states)
- Sweepstakes model = fewer legal hurdles
- Exchange pricing

**Cons**:
- API access unclear (may require partnership)
- Sweepstakes model may have withdrawal limits
- Less mature than Sporttrade

**Integration Priority**: MEDIUM (backup option)

---

## 2. Data Aggregation APIs

### OpticOdds API
**Status**: Primary Data Aggregator Recommendation

**Key Features**:
- 1M+ odds processed per second
- 100+ sportsbooks (US, Canada, Europe, Australia)
- Real-time odds streaming
- Historical data archives
- WebSocket support for live updates
- Bet grading and results

**Sportsbooks Covered**:
- US: DraftKings, FanDuel, BetMGM, Caesars, PointsBet, BetRivers
- International: Pinnacle, Bet365, Betfair, Matchbook
- Many more across regions

**API Capabilities**:
- Odds API (real-time odds)
- Fixture data (schedules, matchups)
- Live in-play odds
- Player props
- Futures markets
- Bet grading
- Historical data

**Pricing**:
- Tiered pricing based on volume
- Free tier likely available for testing
- Enterprise plans for high-volume

**Pros**:
- Fastest data on market (1M+ odds/sec)
- Broadest sportsbook coverage
- Real-time streaming
- Strong documentation
- Used by major operators (BetMGM)

**Cons**:
- Premium pricing for high volume
- May be overkill for small operations

**Integration Priority**: HIGH (Core data layer)

---

### TheRundown API
**Status**: Secondary Data Source

**Key Features**:
- Real-time odds from 15+ sportsbooks
- Prediction markets data
- Live stats across 30+ leagues
- Simple REST API

**Sportsbooks Covered**:
- DraftKings, FanDuel, BetMGM
- Pinnacle, Matchbook, Bovada, Bodog
- PointsBet, Unibet, 5Dimes
- And more

**API Capabilities**:
- Odds comparison
- Live in-play data
- Prediction market data
- League coverage: NFL, NBA, WNBA, MLB, NHL, NCAA, MLS, EPL, etc.

**Pricing**:
- Available via APILayer marketplace
- Tiered subscriptions
- Free tier for testing

**Pros**:
- Simple API structure
- Good for odds comparison
- Prediction market data (unique)
- Affordable pricing

**Cons**:
- Fewer sportsbooks than OpticOdds
- Slower update rate than OpticOdds

**Integration Priority**: MEDIUM (supplemental data)

---

## 3. 2026 API Landscape Comparison

| API | Type | Sportsbooks | Speed | Cost | US Legal | API Access |
|-----|------|-------------|-------|------|----------|------------|
| OpticOdds | Aggregator | 100+ | 1M+/sec | Premium | Yes | Excellent |
| TheRundown | Aggregator | 15+ | Fast | Affordable | Yes | Good |
| Sporttrade | Exchange | N/A (exchange) | Fast | 2% commission | Yes | Good |
| ProphetX | Exchange | N/A (exchange) | Fast | Sweepstakes | Yes (40 states) | Limited |
| Betfair | Exchange | N/A (exchange) | Very Fast | 2-5% commission | NO (US blocked) | Excellent |
| Pinnacle | Sportsbook | N/A (own) | Fast | Low margin | NO (US restricted) | Good |
| TheOddsAPI | Aggregator | 40+ | Fast | $20-80/mo | Yes | Good |

---

## 4. Recommended Architecture for BetGenie

### Phase 1: US-Legal Deployment (Immediate)

```
┌─────────────────────────────────────────────────────────┐
│                    BetGenie Frontend                    │
│              (Next.js 16 - SaaS Platform)               │
│  - Dashboard                                           │
│  - PIS Display                                         │
│  - Consensus Module                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              OpticOdds API (Data Layer)                 │
│  - Real-time odds from 100+ sportsbooks                │
│  - Sharp money movement tracking                       │
│  - Line shopping                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         BetGenie AI Engine (Python Backend)             │
│  - Player Impact Score (PIS)                           │
│  - Consensus Module (PIS + Sharp Money + Expert Data)   │
│  - Unified Confidence Score                             │
│  - Trap Game Detection                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          Sporttrade API (Execution Layer)                │
│  - Bet placement                                        │
│  - Account management                                  │
│  - Real-time position tracking                          │
└─────────────────────────────────────────────────────────┘
```

### Phase 2: International Expansion (Future)

```
┌─────────────────────────────────────────────────────────┐
│              International Entity (UK Ltd)               │
│  - Betfair API access                                   │
│  - Pinnacle API access                                 │
│  - European sportsbook integration                      │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Legal Structure Recommendations

### US Entity (Mohn Empire)
**Purpose**: SaaS/Data Analytics Platform
**Legal Status**: Software company, not a gambling operator
**Revenue Model**: Subscription to BetGenie intelligence platform
**Regulatory Burden**: Minimal (data/analytics is legal in all states)
**Banking**: US business bank account (Stripe, etc.)

**What It Does**:
- Hosts the Next.js dashboard
- Runs the AI analysis engine
- Provides "information services" to subscribers
- Does NOT place bets directly (user places bets via Sporttrade)

### International Entity (Future - UK Ltd or UAE Freezone)
**Purpose**: Execution Layer for non-US markets
**Legal Status**: Gambling operator (if placing bets)
**Revenue Model**: Commission on bet execution
**Regulatory Burden**: Requires gambling license in target jurisdiction
**Banking**: International EMI (Revolut Business, Airwallex)

**What It Does**:
- Hosts the execution module
- Integrates with Betfair/Pinnacle APIs
- Places bets for international users
- Handles gambling compliance

**Why This Structure Works**:
- US entity avoids gambling regulation by being a "data provider"
- International entity can access Betfair/Pinnacle (blocked in US)
- Modular architecture allows easy swap of execution APIs
- Banking separation (US bank for SaaS, international bank for gambling)

---

## 6. Integration Roadmap

### Immediate (Week 1-2)
1. **Sign up for OpticOdds API** (free tier for testing)
2. **Sign up for Sporttrade API** (developer access)
3. **Test data flows** from OpticOdds → Python engine
4. **Mock execution** to Sporttrade (no real money)

### Short Term (Month 1)
1. **Implement Consensus Module** (PIS + OpticOdds sharp money)
2. **Build Unified Confidence Score** algorithm
3. **Create Trap Game Detection** system
4. **Connect to Sporttrade sandbox** for testing

### Medium Term (Month 2-3)
1. **Go live with Sporttrade** (small bankroll testing)
2. **Implement TheRundown API** for additional data sources
3. **Add ProphetX integration** (if needed for state coverage)
4. **Deploy US SaaS platform** for beta users

### Long Term (Month 6+)
1. **Form UK Ltd entity** for international expansion
2. **Integrate Betfair API** via UK entity
3. **Add Pinnacle API** for sharp odds
4. **Launch international version**

---

## 7. Key Technical Considerations

### Rate Limits
- OpticOdds: High-volume (1M+ odds/sec) - likely no practical limit
- Sporttrade: API limits TBD (likely generous for developers)
- TheRundown: Standard API rate limits

### Latency Requirements
- Real-time odds: < 1 second latency required
- Bet placement: < 2 seconds from signal to execution
- WebSocket recommended for live updates

### Error Handling
- API downtime: Fallback to cached data
- Exchange downtime: Queue bets for retry
- Banking failures: Alert user, hold bet

### Security
- API keys: Environment variables, never in code
- User authentication: OAuth/JWT for SaaS platform
- Bet execution: Double confirmation required
- Audit logs: All bet placements logged

---

## 8. Cost Projections

### Monthly Costs (US Deployment)
- OpticOdds API: $200-500/mo (based on volume)
- Sporttrade: 2% commission on winning bets only
- Hosting (Vercel/AWS): $50-100/mo
- **Total**: ~$300-600/mo fixed + 2% commission

### Monthly Costs (International Expansion)
- Betfair API: $200-500/mo
- Pinnacle API: $100-300/mo
- UK entity maintenance: $100-200/mo
- International banking: $50-100/mo
- **Total**: ~$450-1100/mo fixed + exchange commissions

---

## 9. Competitive Analysis

### What Makes BetGenie Different

**Traditional Sharps**:
- Use regression models on past stats
- Focus on line shopping and arbitrage
- Don't account for human factors
- Limited to straight bets

**BetGenie**:
- Player Impact Score (human factors)
- Sentiment analysis (news, social media)
- Legal event tracking
- Psychological state modeling
- Parlay optimization with correlation analysis
- Unified Confidence Score (PIS + Sharp Money + Expert Data)

**The Edge**:
- Most bots ignore human volatility
- BetGenie captures what others miss
- Personal events (DUI, divorce, family death) = predictable performance changes
- This is where the "edge" lives

---

## 10. Next Actions

1. **Create OpticOdds account** and get API key
2. **Create Sporttrade developer account** for API access
3. **Build Consensus Module** to integrate OpticOdds data with PIS
4. **Implement Unified Confidence Score** algorithm
5. **Create Trap Game Detection** system
6. **Document legal structure** for attorney review
7. **Set up US entity** (LLC) if not already formed

---

**Research Complete**: April 28, 2026  
**Next Phase**: Consensus Module Development
