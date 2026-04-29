# Advanced Betting Strategies

This document outlines advanced betting strategies beyond recreational approaches, focusing on arbitrage, matched betting, and line shopping for the BetGenie system.

## Table of Contents
- [Arbitrage Betting](#arbitrage-betting)
- [Matched Betting](#matched-betting)
- [Line Shopping](#line-shopping)
- [Integration with BetGenie](#integration-with-betgenie)

---

## Arbitrage Betting

### Overview
Arbitrage betting (also known as "arbing") involves placing bets on all possible outcomes of an event across different bookmakers to guarantee a profit regardless of the result. This is possible when bookmakers have different odds for the same event.

### How It Works
1. **Identify Arbitrage Opportunities**: Find discrepancies in odds between different sportsbooks
2. **Calculate Stakes**: Determine the exact amount to bet on each outcome to ensure profit
3. **Place Simultaneous Bets**: Execute all bets quickly before odds change
4. **Guaranteed Profit**: Lock in a small but guaranteed return

### Arbitrage Formula
For a two-outcome event:
```
Profit Margin = (1 / Odds_A) + (1 / Odds_B)
```

If Profit Margin < 1, arbitrage opportunity exists.

### Example
- Bookmaker A: Team A @ 2.10 (1/2.10 = 0.476)
- Bookmaker B: Team B @ 2.10 (1/2.10 = 0.476)
- Total: 0.476 + 0.476 = 0.952 < 1 (4.8% guaranteed profit)

### Arbitrage Calculator
```python
def calculate_arbitrage(odds_list):
    """
    Calculate arbitrage opportunity given odds from multiple bookmakers.
    Returns True if arbitrage exists, along with optimal stakes.
    """
    total_implied_probability = sum(1/odds for odds in odds_list)
    
    if total_implied_probability < 1:
        profit_margin = (1 - total_implied_probability) * 100
        stakes = [(1/odds) / total_implied_probability for odds in odds_list]
        return True, profit_margin, stakes
    return False, 0, []
```

### Key Considerations
- **Speed**: Odds change quickly; must act fast
- **Stake Limits**: Bookmakers may limit winning accounts
- **Bankroll Requirements**: Need significant capital for meaningful profits
- **Bet Placement**: Must place all bets simultaneously
- **Bookmaker Rules**: Different rules on voided bets can break arbitrage

### BetGenie Implementation
- Monitor multiple odds sources (OpticOdds, Sportradar, The Odds API)
- Real-time arbitrage detection algorithms
- Automated stake calculation
- Alert system for arbitrage opportunities
- Integration with bankroll management for position sizing

---

## Matched Betting

### Overview
Matched betting (also known as "bonus arbitrage") uses free bets, bonuses, and promotions offered by bookmakers to guarantee profit. It's risk-free when done correctly.

### How It Works
1. **Qualifying Bet**: Place a bet to qualify for a free bet promotion
2. **Lay Bet**: Place a counter-bet on a betting exchange to cover all outcomes
3. **Free Bet**: Use the free bet (usually with stake not returned)
4. **Lay Free Bet**: Cover the free bet on an exchange to lock in profit

### Key Concepts
- **Back Bet**: Betting for an outcome to happen (traditional sportsbook)
- **Lay Bet**: Betting against an outcome (betting exchange)
- **Stake Not Returned (SNR)**: Free bet where only winnings are paid
- **Stake Returned (SR)**: Free bet where stake is also returned

### Matched Betting Calculator
```python
def calculate_matched_bet(back_odds, lay_odds, stake, is_free_bet=False):
    """
    Calculate optimal lay stake for matched betting.
    """
    commission = 0.05  # Exchange commission (typically 5%)
    
    if is_free_bet:
        # Free bet (stake not returned)
        lay_stake = (stake * (back_odds - 1)) / (lay_odds - commission)
        profit = (stake * (back_odds - 1)) - (lay_stake * (lay_odds - 1)) - (lay_stake * commission)
    else:
        # Qualifying bet
        lay_stake = (stake * back_odds) / (lay_odds - commission)
        profit = (stake * (back_odds - 1)) - (lay_stake * (lay_odds - 1)) - (lay_stake * commission)
    
    return lay_stake, profit
```

### Example
- Qualifying bet: $50 on Team A @ 2.00
- Lay bet: $49.50 on Team A @ 2.02 (with 5% commission)
- Free bet: $50 free bet on Team B @ 3.00
- Lay free bet: $33.33 on Team B @ 3.10
- Guaranteed profit: ~$15-20

### Key Considerations
- **Promotion Terms**: Read terms carefully (wagering requirements, minimum odds)
- **Exchange Liquidity**: Need enough liquidity on betting exchanges
- **Account Restrictions**: Bookmakers may limit or close accounts
- **Time Investment**: Requires ongoing monitoring of promotions
- **Geographic Restrictions**: Not available in all jurisdictions

### BetGenie Implementation
- Monitor bookmaker promotions and bonuses
- Automated matched bet calculations
- Integration with betting exchanges
- Promotion tracking and optimization
- Risk-free profit opportunities alerts

---

## Line Shopping

### Overview
Line shopping involves comparing odds across multiple sportsbooks to find the best available line for a particular bet. This is the most accessible and sustainable way to gain an edge in sports betting.

### How It Works
1. **Compare Odds**: Check multiple sportsbooks for the same event
2. **Identify Best Lines**: Find the most favorable odds for your desired outcome
3. **Place Bet**: Wager with the sportsbook offering the best line
4. **Maximize Value**: Consistently betting better lines increases long-term profitability

### Line Shopping Benefits
- **Increased ROI**: Better odds = higher returns on winning bets
- **Reduced Vig**: Lower bookmaker margin
- **Long-term Edge**: Consistent value accumulation
- **No Additional Risk**: Same bet, better price

### Line Shopping Calculator
```python
def calculate_line_value(baseline_odds, available_odds, stake):
    """
    Calculate the value gained by line shopping.
    """
    baseline_payout = stake * baseline_odds
    available_payout = stake * available_odds
    value_gained = available_payout - baseline_payout
    percentage_gain = (value_gained / baseline_payout) * 100
    
    return value_gained, percentage_gain
```

### Example
- Baseline odds: Team A -3.5 @ -110
- Best available odds: Team A -3 @ -105
- On a $100 bet, this saves $5 in vig and increases potential payout

### Key Considerations
- **Number of Accounts**: Need accounts at multiple sportsbooks
- **Odds Movement**: Lines change frequently; must act quickly
- **Bet Limits**: Some books have lower limits on sharp lines
- **Bankroll Distribution**: Spread bankroll across multiple books
- **Withdrawal Speeds**: Consider payout times when choosing books

### Line Shopping Strategies
1. **Opening Lines**: Bet early when books are still setting lines
2. **Steam Chasing**: Follow sharp money movement
3. **Reverse Line Movement**: Bet against public sentiment
4. **Prop Bet Shopping**: Props often have wider variance
5. **Live Betting**: In-game lines offer additional opportunities

### BetGenie Implementation
- Aggregate odds from multiple sources (OpticOdds, Sportradar, The Odds API)
- Real-time odds comparison and alerts
- Best line recommendation engine
- Historical odds tracking
- Line movement analysis
- Automated line shopping suggestions

---

## Integration with BetGenie

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    BetGenie AI Engine                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Odds Aggregator  │  │  Strategy Engine  │                │
│  │  - OpticOdds      │  │  - Arbitrage     │                │
│  │  - Sportradar     │  │  - Matched Bet   │                │
│  │  - The Odds API   │  │  - Line Shopping │                │
│  └──────────────────┘  └──────────────────┘                │
│           │                      │                            │
│           └──────────┬───────────┘                            │
│                      ▼                                        │
│         ┌─────────────────────┐                               │
│         │  Decision Engine    │                               │
│         │  - Risk Assessment  │                               │
│         │  - Bankroll Mgmt    │                               │
│         │  - Bet Sizing       │                               │
│         └─────────────────────┘                               │
│                      │                                        │
│                      ▼                                        │
│         ┌─────────────────────┐                               │
│         │  Execution Layer    │                               │
│         │  - Order Placement   │                               │
│         │  - Bet Tracking     │                               │
│         │  - P&L Monitoring   │                               │
│         └─────────────────────┘                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow
1. **Odds Collection**: Real-time odds from multiple sources
2. **Strategy Analysis**: Apply arbitrage, matched betting, and line shopping algorithms
3. **Risk Assessment**: Evaluate opportunity against bankroll and risk parameters
4. **Decision Making**: Determine optimal bet sizing and execution
5. **Bet Execution**: Place bets with recommended sportsbooks
6. **Monitoring**: Track results and adjust strategies

### Implementation Priorities
1. **Phase 1**: Odds aggregation from multiple sources
2. **Phase 2**: Line shopping implementation (highest ROI, lowest risk)
3. **Phase 3**: Arbitrage detection and alerts
4. **Phase 4**: Matched betting integration (where legally permissible)
5. **Phase 5**: Automated execution with risk management

### Risk Management
- **Bankroll Allocation**: Separate pools for different strategies
- **Position Sizing**: Kelly Criterion for optimal bet sizing
- **Stop Losses**: Pre-defined loss limits
- **Account Protection**: Strategies to avoid account restrictions
- **Diversification**: Spread risk across multiple strategies and sports

### Performance Metrics
- **ROI by Strategy**: Track performance of each betting approach
- **Arbitrage Success Rate**: Percentage of successful arb opportunities
- **Line Shopping Savings**: Total value gained from better odds
- **Matched Betting Profit**: Risk-free profit from promotions
- **Overall Bankroll Growth**: Combined performance across all strategies

---

## Conclusion

These advanced betting strategies provide BetGenie with multiple pathways to profitability:

1. **Arbitrage**: Guaranteed but rare opportunities
2. **Matched Betting**: Risk-free but promotion-dependent
3. **Line Shopping**: Consistent edge through better odds

The system will implement these strategies in phases, starting with line shopping (most accessible) and gradually adding arbitrage and matched betting capabilities as the platform matures.

All strategies will be integrated with BetGenie's existing AI engine, player impact scoring, and bankroll management systems to create a comprehensive betting intelligence platform.
