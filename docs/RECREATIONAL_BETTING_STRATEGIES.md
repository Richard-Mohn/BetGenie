# BetGenie — Recreational Betting Strategies Research

**Purpose**: Document "little guy" betting strategies that recreational bettors use for steady income with small bankrolls.

**Key Insight**: Professional bettors focus on value and edge, but recreational bettors can still profit with disciplined, low-risk strategies that prioritize consistency over big wins.

---

## Core Principles for Small Bankroll Betting

### 1. Unit Betting Strategy
**Concept**: Bet the same amount on every wager (1-3% of bankroll)

**How It Works**:
- If bankroll is $40/week, bet $1-2 per wager
- If bankroll is $500, bet $5-15 per wager
- Never vary bet size based on emotions or "hot streaks"

**Why It Works**:
- Removes emotional decision-making
- Prevents chasing losses
- Makes performance tracking easier
- Protects bankroll during losing streaks

**BetGenie Implementation**: Already built into `adaptive_betting_system.py` - starts at $1, scales up only after proven win rate.

---

### 2. Low Odds Betting Strategy
**Concept**: Focus on high-probability outcomes (1.20-2.00 odds) for steady, repeatable wins

**How It Works**:
- Target odds between 1.20 and 2.00
- Look for value where true probability > implied probability
- Example: Team at 1.35 (74% implied) but real probability is 85% = value bet

**Top 3 Low Odds Strategies**:

#### A. Best 2 Odds Strategy (Safe and Steady)
- Pick two solid outcomes at 1.30-1.45 odds
- Combine into a slip at ~2.00 total odds
- Example: Team A win @ 1.35 + Team B Over 1.5 goals @ 1.45 = ~2.00
- Best for: Measured progress, low volatility

#### B. 3 Odds Strategy (Balanced)
- Select three matches at ~1.30 odds each
- Combined total: 2.20-2.60
- Higher ceiling than 2-odds, more risk
- Best for: Strong weekly win rate, controlled growth

#### C. High Strike Rate Combos
- Combine 3-4 selections at 1.20-1.30 odds
- Total odds: 2.10-2.40
- Markets: Over 1.5 goals, Both Teams to Score, Double Chance
- Golden Rule: Never stack more than 4-5 games

**Why It Works**:
- Higher win rate compensates for lower payouts
- Reduced volatility vs. long-shot parlays
- Easier to build consistent bankroll growth

**BetGenie Application**: Use consensus module to identify high-confidence props (70%+), combine 2-3 correlated legs for 2.00-2.40 odds.

---

### 3. Percentage Staking (1-5% Rule)
**Concept**: Bet a fixed percentage of current bankroll, not fixed dollar amount

**How It Works**:
- Bet 1-5% of current bankroll per wager
- If bankroll is $200 at 2% = $4 per bet
- If bankroll grows to $260 at 2% = $5.20 per bet
- Automatically scales up with wins, down with losses

**Why It Works**:
- Protects during losing periods
- Scales profits during winning streaks
- Keeps risk consistent over time
- Prevents over-betting on "hot" picks

**BetGenie Implementation**: Built into `adaptive_betting_system.py` - uses percentage-based scaling based on phase.

---

### 4. Fixed Stake Strategy
**Concept**: Wager the same amount on every bet regardless of previous results

**How It Works**:
- Decide on a fixed stake (e.g., $5 per bet)
- Never change stake size
- Remove emotional decision-making

**Why It Works**:
- Simplicity and discipline
- Easy to track performance
- Prevents "doubling down" after losses
- Eliminates "betting big" after wins

**BetGenie Application**: Use during TESTING phase ($1-2 fixed stakes) before scaling up.

---

## Popular Betting Options for Beginners

### Moneylines
- Bet on straight-up winner
- Odds close to even for favorites
- Better payouts for underdogs
- **Best for**: New bettors, simple wins

### Point Spreads
- Bet on margin of victory
- Favorite must win by more than spread
- Underdog can lose by less than spread
- **Best for**: Making lopsided games interesting

### Totals (Over/Under)
- Bet on combined score over/under set number
- Consider offensive/defensive matchups
- **Best for**: Statistical analysis, prop betting

**BetGenie Focus**: Player props (points, rebounds, assists) - this is our sweet spot with PIS analysis.

---

## Live Betting Opportunities

**When Games Are Active**:
- Oddsmakers set lines quickly, may overreact
- Look for overreactions to big plays
- Watch for star player foul trouble
- Consider team psychology (slow starters, strong finishers)

**BetGenie Application**: Real-time PIS updates during games (future feature).

---

## Common Mistakes to Avoid

### 1. Emotional Betting
- Don't bet on favorite teams
- Don't follow "gut feelings"
- Stick to stats and facts
- Remove personal biases

### 2. Chasing Losses
- Never increase stakes after losses
- Accept losing days as part of variance
- Stick to predetermined budget
- Don't deposit more money after losing

### 3. Overloading Accumulators
- Don't stack more than 4-5 legs
- Each additional leg reduces probability
- Keep parlays focused and correlated
- Avoid "lottery ticket" mentality

### 4. Ignoring Bankroll Management
- Never bet more than 5% of bankroll
- Set weekly budget and stick to it
- Track every bet and result
- Review performance regularly

---

## BetGenie Strategy Integration

### Phase 1: Testing (First 20 bets)
- **Bet Size**: $1-2 fixed
- **Strategy**: Single props on role players with soft lines
- **Target**: 55%+ win rate to advance
- **Focus**: Validate PIS + Consensus system

### Phase 2: Growth (Proven winner)
- **Bet Size**: $5-10 (1-2% of bankroll)
- **Strategy**: 2-leg correlated parlays at ~2.00 odds
- **Target**: 60%+ win rate to advance
- **Focus**: Role players + soft lines for value

### Phase 3: Expansion (Consistent profits)
- **Bet Size**: $20-50 (2-3% of bankroll)
- **Strategy**: 3-leg parlays at 2.20-2.60 odds
- **Target**: 65%+ win rate to advance
- **Focus**: Mix of stars (fade) and role players (value)

### Phase 4: Maximum (Elite performance)
- **Bet Size**: $50-100 (up to 2% of bankroll)
- **Strategy**: High-confidence picks across all tiers
- **Target**: Maintain 65%+ win rate
- **Focus**: Maximum volume with proven system

---

## Recommended Free APIs to Sign Up For

### Data Sources
1. **The Odds API** (Free tier: 500 requests/month)
   - Real-time odds from 40+ sportsbooks
   - Player props included
   - Sign up: https://the-odds-api.com/

2. **OpticOdds** (Free tier available)
   - 100+ sportsbooks, 1M+ odds/sec
   - Sharp money movement data
   - Sign up: https://developer.opticodds.com/

3. **NewsAPI** (Free tier: 100 requests/day)
   - Real-time news for personal events
   - Player mentions tracking
   - Sign up: https://newsapi.org/

4. **Twitter/X API** (Free tier limited)
   - Social media monitoring
   - Player sentiment analysis
   - Sign up: https://developer.twitter.com/

### For Demo Picks (DraftKings/FanDuel)
- No API needed for demo
- Manual bet placement for testing
- Use odds from The Odds API to find best lines

---

## Summary: The "Little Guy" Advantage

**What Recreational Bettors Can Do That Pros Can't**:
1. **Fly under the radar**: Small bets don't move lines
2. **Exploit soft lines**: Bookmakers focus on sharp action, not small bets
3. **Take advantage of promos**: Sign-up bonuses, risk-free bets
4. **Specialize in niche markets**: Role player props are less efficient

**BetGenie Edge**:
- AI analysis of personal events (PIS) - no one else does this
- Consensus aggregation - combines multiple intelligence sources
- Adaptive betting - starts small, scales up only when proven
- Focus on role players - lines are softer, less sharp action

**The Path to Steady Income**:
1. Start with $1-2 bets to prove the system
2. Focus on role players with soft lines
3. Use 2-leg correlated parlays for 2.00 odds
4. Scale up only after 55%+ win rate over 50 bets
5. Maintain discipline, never chase losses
6. Track everything, review performance weekly

---

**Document Status**: Complete  
**Last Updated**: April 28, 2026  
**Next**: Integrate APIs and begin testing
