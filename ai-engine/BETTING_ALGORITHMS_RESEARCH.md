# BetGenie — Proven Betting Algorithms Research

## Overview
This document summarizes the proven betting algorithms and strategies researched for the BetGenie NBA betting system. These algorithms form the mathematical foundation of our prediction pipeline.

---

## 1. Kelly Criterion

### What is it?
The Kelly Criterion is a mathematical formula developed by John L. Kelly in 1956 for optimal bet sizing. It determines the optimal fraction of your bankroll to wager on a bet to maximize long-term growth.

### The Formula
```
f* = (bp - q) / b
```

Where:
- **f*** = Fraction of current bankroll to wager
- **b** = Odds received on the bet (decimal odds - 1)
- **p** = Probability of winning (your estimated true probability)
- **q** = Probability of losing (1 - p)

### Example
If a bet has:
- 60% chance of winning (p = 0.6)
- 40% chance of losing (q = 0.4)
- +100 odds (b = 1.0)

Kelly recommends: f* = (1.0 × 0.6 - 0.4) / 1.0 = 0.20 = **20% of bankroll**

### Implementation in BetGenie
The `bankroll_manager.py` module implements Kelly Criterion for bet sizing:
- Calculates optimal stake based on AI confidence and edge
- Uses fractional Kelly (half-Kelly) for conservative risk management
- Adjusts for bankroll size and risk profile

### Key Insights
- **Only bet when f* > 0** (positive edge)
- **Fractional Kelly** (half-Kelly, third-Kelly) reduces volatility while maintaining growth
- **Legendary advocate**: Warren Buffett uses Kelly Criterion for investments
- **Maximizes long-term capital growth** when applied correctly

---

## 2. Poisson Distribution

### What is it?
Developed by 19th-century French mathematician Siméon Denis Poisson, this probability theory determines the likelihood of unrelated events occurring within a specific time period.

### How it Works in Sports Betting
Poisson distribution uses historical averages to calculate:
1. **Attack Strength** - Team's scoring ability relative to league average
2. **Defense Strength** - Team's defensive ability relative to league average
3. **Expected Goals/Points** - Combines attack/defense to predict score

### Application to Basketball
- Useful for predicting player prop over/under bets
- Can model points, rebounds, assists as Poisson events
- Best for stats that occur in small increments (1 point at a time)

### Limitations
- **Does not account for human factors**: injuries, locker room issues, personal events
- **Assumes independence**: Events are treated as unrelated
- **Historical bias**: May not reflect current form or context

### Implementation in BetGenie
While not directly implemented, BetGenie's **Player Impact Score (PIS)** addresses the key limitation of Poisson distribution by incorporating:
- Personal life events (family, legal, health)
- Psychological factors (sentiment, confidence)
- Time decay for event relevance
- This human context is what differentiates BetGenie from pure statistical models

---

## 3. Expected Value (EV)

### What is it?
Expected Value is the average profit or loss you can expect from a bet over time. It's the foundation of profitable sports betting.

### The Formula
```
EV = (probability of win × payout) - (probability of loss × stake)
```

### Example
Bet $100 at +110 odds with 55% win probability:
- Win: 0.55 × $110 = $60.50
- Loss: 0.45 × $100 = $45.00
- EV = $60.50 - $45.00 = **+$15.50 per $100 bet**

### Key Concept: +EV vs -EV
- **+EV (Positive Expected Value)**: Odds are better than true probability → Profitable long-term
- **-EV (Negative Expected Value)**: Odds are worse than true probability → Unprofitable long-term
- **Critical insight**: A bet can be "likely to win" but still be -EV (bad bet)

### Implementation in BetGenie
- **Single bets**: EV calculated for each prop recommendation
- **Parlays**: EV calculated using Monte Carlo simulation (10,000 iterations)
- **Guaranteed picks**: Only 70%+ confidence bets with positive EV are recommended
- **Bankroll management**: Bet sizes adjusted based on EV magnitude

---

## 4. Monte Carlo Simulation

### What is it?
A computational technique that uses repeated random sampling to estimate the probability of different outcomes.

### Application in BetGenie
Used in `guaranteed_picks_engine.py` for parlay probability estimation:
- **10,000 simulations** per parlay
- Accounts for correlation between legs
- Provides **conservative win rate** estimate
- More accurate than simple probability multiplication

### Why it Matters
- **Correlation awareness**: Same-game bets are correlated (not independent)
- **Risk assessment**: Provides realistic probability estimates
- **Parlay optimization**: Helps build parlays with balanced risk/reward

---

## 5. Time Decay Functions

### What is it?
Mathematical functions that reduce the impact of events over time. Recent events have more influence than old events.

### Implementation in BetGenie
The `impact_score.py` module uses exponential decay:
```
impact = base_impact × e^(-λ × days_since_event)
```

Where:
- **λ (lambda)** = Decay rate (different for each event category)
- **Half-life** = Time for impact to reduce by 50%

### Event Half-Lives
- **Legal events**: 30-90 days (long-lasting impact)
- **Family events**: 14-30 days (medium impact)
- **Health events**: 7-21 days (shorter recovery)
- **Performance streaks**: 3-7 days (very short-term)

---

## 6. Composite Scoring (Player Impact Score)

### What is it?
BetGenie's proprietary algorithm that combines multiple factors into a single 0-100 score representing a player's expected performance capacity.

### Components
1. **Physical Factor** (weight: 25%)
   - Health status, injury recovery, fatigue
2. **Emotional Factor** (weight: 25%)
   - Family events, personal milestones, stress
3. **Psychological Factor** (weight: 25%)
   - Confidence, motivation, mental state
4. **Situational Factor** (weight: 25%)
   - Team context, game importance, schedule

### Calculation
```
PIS = Σ (component_weight × component_score)
```

### Edge Over Traditional Models
- **Human context**: Incorporates personal life events
- **Time-aware**: Recent events weighted more heavily
- **Verified sources**: Higher confidence for verified events
- **Sentiment analysis**: Uses NLP to gauge emotional impact

---

## Algorithm Comparison

| Algorithm | Primary Use | BetGenie Implementation | Advantage |
|-----------|-------------|------------------------|-----------|
| Kelly Criterion | Bet sizing | `bankroll_manager.py` | Optimal bankroll growth |
| Poisson Distribution | Score prediction | Not used (addressed by PIS) | Pure statistical approach |
| Expected Value | Profitability | All modules | Foundation of +EV betting |
| Monte Carlo | Parlay probability | `guaranteed_picks_engine.py` | Correlation-aware simulation |
| Time Decay | Event relevance | `impact_score.py` | Dynamic impact weighting |
| PIS | Performance prediction | `impact_score.py` | Human context integration |

---

## Scientific Validation

### Kelly Criterion
- **Proven mathematically**: Maximizes geometric growth rate
- **Academic research**: Widely studied in finance and gambling theory
- **Real-world success**: Used by Warren Buffett, professional bettors

### Expected Value
- **Fundamental to probability theory**: Law of Large Numbers
- **Casino edge**: How casinos guarantee profits
- **Sports betting**: Only +EV bets are profitable long-term

### Monte Carlo Simulation
- **Standard in finance**: Risk assessment, option pricing
- **Scientific validity**: Law of Large Numbers ensures accuracy
- **BetGenie advantage**: 10,000 simulations provide robust estimates

### Player Impact Score
- **Novel approach**: Combines human factors with statistical analysis
- **Based on research**: Sports psychology, behavioral economics
- **Differentiation**: Addresses key limitation of pure statistical models

---

## Conclusion

BetGenie's algorithm foundation combines:
1. **Proven mathematical frameworks** (Kelly, EV, Monte Carlo)
2. **Novel human context integration** (PIS, time decay)
3. **Conservative risk management** (fractional Kelly, 70%+ confidence threshold)

This hybrid approach leverages the strengths of both:
- **Traditional statistical models** (objective, data-driven)
- **Human factor analysis** (subjective, context-aware)

The result is a betting system that is both mathematically sound and uniquely positioned to identify edges that pure statistical models miss.

---

## References

1. Kelly, J. L. (1956). "A New Interpretation of Information Rate". Bell System Technical Journal.
2. Wikipedia: Kelly Criterion - https://en.wikipedia.org/wiki/Kelly_criterion
3. OddsJam: Kelly Criterion in Sports Betting - https://oddsjam.com/betting-education/what-is-the-kelly-criterion-in-sports-betting
4. SportsBettingDime: Poisson Distribution - https://www.sportsbettingdime.com/guides/strategy/poisson-distribution/
5. Poisson, S. D. (1837). "Recherches sur la probabilité des jugements en matière criminelle et en matière civile".

---

**Document Version**: 1.0  
**Last Updated**: April 28, 2026  
**Author**: BetGenie AI Team
