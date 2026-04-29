"""
BetGenie — Exotic Bets Module

This module implements exotic and game line betting types including:
- First Basket Scorer
- Race to X Points (20, 30, 40, etc.)
- First Team to Score
- Winning Margin
- First Quarter/Half Results
- Overtime Props
- Tip-off Winner
- High Odds "Kicker" Bets
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
from datetime import datetime


class ExoticBetType(Enum):
    """Types of exotic NBA bets."""
    FIRST_BASKET_SCORER = "first_basket_scorer"  # Which player scores first
    FIRST_TEAM_TO_SCORE = "first_team_to_score"  # Which team scores first
    RACE_TO_20 = "race_to_20"  # First team to 20 points
    RACE_TO_30 = "race_to_30"  # First team to 30 points
    RACE_TO_40 = "race_to_40"  # First team to 40 points
    WINNING_MARGIN = "winning_margin"  # Exact winning margin range
    FIRST_QUARTER_WINNER = "first_quarter_winner"  # Who leads after Q1
    FIRST_HALF_WINNER = "first_half_winner"  # Who leads at halftime
    OVERTIME_YES_NO = "overtime_yes_no"  # Will game go to OT
    TIP_OFF_WINNER = "tip_off_winner"  # Who wins the opening tip
    FIRST_THREE_POINTER = "first_three_pointer"  # Who makes first 3PT
    FIRST_FREE_THROW = "first_free_throw"  # Who makes first FT
    DOUBLE_RESULT = "double_result"  # HT/FT result combo


@dataclass
class ExoticBet:
    """An exotic or game line bet."""
    bet_id: str
    game_id: str
    bet_type: ExoticBetType
    selection: str  # The specific pick (player name, team, yes/no, etc.)
    odds: int  # American odds
    ai_confidence: float  # 0-100
    reasoning: List[str]  # Why this pick has value
    factors: List[str]  # Key factors influencing the bet
    projected_probability: float  # AI's estimated true probability
    edge: float  # Edge over implied odds
    bet_category: str  # "kicker", "smart_money", "value_play", "long_shot"


@dataclass
class KickerBet:
    """
    High odds "kicker" bet that can pay out big.
    These are long shots with positive EV that add massive upside to parlays.
    """
    bet_id: str
    game_id: str
    description: str  # Human readable description
    odds: int  # High odds, e.g., +2000, +5000, +20000
    ai_confidence: float  # Lower confidence but positive EV
    potential_payout: float  # Dollar amount on $10 bet
    reasoning: List[str]
    risk_level: str  # "high", "extreme", "moonshot"
    correlation_with: List[str]  # Other bets this correlates with


@dataclass
class GameLineAnalysis:
    """Analysis of all game lines for a specific game."""
    game_id: str
    home_team: str
    away_team: str
    tip_off_winner: Optional[ExoticBet]  # Who wins opening tip
    first_basket_options: List[ExoticBet]  # All first basket odds
    race_to_20: List[ExoticBet]  # Race to 20 options
    race_to_30: List[ExoticBet]  # Race to 30 options
    first_quarter: List[ExoticBet]  # First quarter winner options
    winning_margins: List[ExoticBet]  # Winning margin ranges
    overtime_prop: Optional[ExoticBet]  # OT yes/no
    best_kicker: Optional[KickerBet]  # Best high-odds kicker for this game


class CorrelationMatrix:
    """
    Analyzes correlations between different bet types.
    Used to construct smarter parlays with realistic probability calculations.
    """
    
    # Correlation coefficients between different bet types
    # 1.0 = perfectly correlated (if A happens, B definitely happens)
    # -1.0 = perfectly negatively correlated
    # 0.0 = independent
    CORRELATION_MAP = {
        # First basket scorer correlates with first team to score
        (ExoticBetType.FIRST_BASKET_SCORER, ExoticBetType.FIRST_TEAM_TO_SCORE): 0.85,
        
        # Race to 20 correlates with first quarter winner
        (ExoticBetType.RACE_TO_20, ExoticBetType.FIRST_QUARTER_WINNER): 0.70,
        
        # Race to 30 correlates with first half winner
        (ExoticBetType.RACE_TO_30, ExoticBetType.FIRST_HALF_WINNER): 0.65,
        
        # Winning margin correlates with game winner (if we know team)
        (ExoticBetType.WINNING_MARGIN, ExoticBetType.DOUBLE_RESULT): 0.60,
        
        # Overtime negatively correlates with blowout margins
        (ExoticBetType.OVERTIME_YES_NO, ExoticBetType.WINNING_MARGIN): -0.40,
        
        # Tip-off winner slightly correlates with first basket
        (ExoticBetType.TIP_OFF_WINNER, ExoticBetType.FIRST_TEAM_TO_SCORE): 0.55,
        
        # First three pointer correlates with first team to score
        (ExoticBetType.FIRST_THREE_POINTER, ExoticBetType.FIRST_TEAM_TO_SCORE): 0.45,
    }
    
    @classmethod
    def get_correlation(cls, bet1: ExoticBetType, bet2: ExoticBetType) -> float:
        """Get correlation coefficient between two bet types."""
        # Check both directions
        if (bet1, bet2) in cls.CORRELATION_MAP:
            return cls.CORRELATION_MAP[(bet1, bet2)]
        if (bet2, bet1) in cls.CORRELATION_MAP:
            return cls.CORRELATION_MAP[(bet2, bet1)]
        return 0.0  # Default: independent
    
    @classmethod
    def calculate_parlay_probability(
        cls,
        bets: List[ExoticBet],
        individual_probabilities: List[float]
    ) -> float:
        """
        Calculate true parlay probability accounting for correlations.
        
        Uses a simplified correlation adjustment:
        - Start with product of individual probabilities (independence assumption)
        - Adjust up/down based on average correlation between legs
        """
        if len(bets) < 2:
            return individual_probabilities[0] if individual_probabilities else 0.0
        
        # Base probability (independence assumption)
        base_prob = 1.0
        for prob in individual_probabilities:
            base_prob *= prob
        
        # Calculate average correlation
        total_corr = 0.0
        count = 0
        for i in range(len(bets)):
            for j in range(i + 1, len(bets)):
                corr = cls.get_correlation(bets[i].bet_type, bets[j].bet_type)
                total_corr += corr
                count += 1
        
        avg_correlation = total_corr / count if count > 0 else 0.0
        
        # Adjust probability based on correlation
        # Positive correlation = higher probability than independence assumption
        # Negative correlation = lower probability
        adjustment = 1.0 + (avg_correlation * 0.3)  # 30% weight to correlation
        
        return min(0.99, base_prob * adjustment)


class ExoticBetAnalyzer:
    """
    Analyzes exotic bets and identifies value opportunities.
    """
    
    def __init__(self):
        self.correlation_matrix = CorrelationMatrix()
    
    def analyze_first_basket_scorer(
        self,
        game_id: str,
        home_team: str,
        away_team: str,
    ) -> List[ExoticBet]:
        """
        Analyze first basket scorer options.
        
        In production, this would fetch real odds from sportsbook API.
        For now, returns empty list as real odds integration is needed.
        """
        return []
    
    def find_kicker_bets(
        self,
        game_id: str,
        home_team: str,
        away_team: str,
        game_context: dict
    ) -> List[KickerBet]:
        """
        Find high-odds "kicker" bets with positive expected value.
        
        In production, this would fetch real odds from sportsbook API.
        For now, returns empty list as real odds integration is needed.
        """
        return []
    
    def analyze_race_to_points(
        self,
        game_id: str,
        home_team: str,
        away_team: str,
        target_points: int = 20
    ) -> List[ExoticBet]:
        """
        Analyze 'Race to X Points' markets.
        
        In production, this would fetch real odds from sportsbook API.
        For now, returns empty list as real odds integration is needed.
        """
        return []
    
    def build_exotic_parlay(
        self,
        bets: List[ExoticBet],
        stake: float = 10.0
    ) -> dict:
        """
        Build and analyze an exotic bets parlay.
        
        Returns detailed analysis including:
        - Combined odds
        - True probability (accounting for correlations)
        - Expected value
        - Risk assessment
        """
        # Calculate combined odds
        combined_decimal = 1.0
        for bet in bets:
            if bet.odds > 0:
                decimal = (bet.odds / 100) + 1
            else:
                decimal = (100 / abs(bet.odds)) + 1
            combined_decimal *= decimal
        
        # Convert to American odds
        if combined_decimal >= 2.0:
            combined_american = round((combined_decimal - 1) * 100)
        else:
            combined_american = round(-100 / (combined_decimal - 1))
        
        # Get individual probabilities
        individual_probs = [bet.projected_probability for bet in bets]
        
        # Calculate true probability using correlation matrix
        true_prob = self.correlation_matrix.calculate_parlay_probability(
            bets, individual_probs
        )
        
        # Calculate implied probability from odds
        implied_prob = 1 / combined_decimal
        
        # Calculate expected value
        ev = (true_prob * combined_decimal) - ((1 - true_prob) * 1)
        
        # Calculate potential payout
        potential_payout = stake * combined_decimal
        
        # Risk assessment
        if len(bets) >= 6 and combined_american > 2000:
            risk_level = "MOONSHOT"
        elif len(bets) >= 4 and combined_american > 1000:
            risk_level = "HIGH"
        elif ev > 0.2:
            risk_level = "POSITIVE_EV"
        else:
            risk_level = "MODERATE"
        
        return {
            "legs": bets,
            "num_legs": len(bets),
            "combined_odds": combined_american,
            "decimal_odds": combined_decimal,
            "true_probability": true_prob,
            "implied_probability": implied_prob,
            "expected_value": ev,
            "potential_payout": potential_payout,
            "stake": stake,
            "risk_level": risk_level,
            "correlation_adjusted": True,
        }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — EXOTIC BETS & KICKER ANALYZER")
    print("  High Odds Opportunities & Game Line Intelligence")
    print("=" * 70)
    
    analyzer = ExoticBetAnalyzer()
    
    # Analyze first basket scorers
    print("\n🏀 FIRST BASKET SCORER ANALYSIS")
    print("-" * 70)
    
    first_basket_bets = analyzer.analyze_first_basket_scorer(
        game_id="nba-test-001",
        home_team="76ers",
        away_team="Celtics",
        tip_off_winner="76ers",
        player_jump_ball_odds={}
    )
    
    for bet in first_basket_bets[:3]:
        print(f"\n  {bet.selection}")
        print(f"    Odds: {'+' if bet.odds > 0 else ''}{bet.odds}")
        print(f"    AI Confidence: {bet.ai_confidence:.1f}%")
        print(f"    Projected Probability: {bet.projected_probability:.1%}")
        print(f"    Edge: {bet.edge:+.1%}")
        print(f"    Category: {bet.bet_category}")
        print(f"    Reasoning:")
        for reason in bet.reasoning:
            print(f"      • {reason}")
    
    # Find kicker bets
    print("\n\n🚀 KICKER BETS (High Payout Opportunities)")
    print("-" * 70)
    
    kickers = analyzer.find_kicker_bets(
        game_id="nba-test-001",
        home_team="76ers",
        away_team="Celtics",
        game_context={}
    )
    
    for kicker in kickers:
        print(f"\n  💰 {kicker.description}")
        print(f"    Odds: {'+' if kicker.odds > 0 else ''}{kicker.odds}")
        print(f"    Potential Payout: ${kicker.potential_payout:.2f} on $10 bet")
        print(f"    Risk Level: {kicker.risk_level.upper()}")
        print(f"    AI Confidence: {kicker.ai_confidence:.1f}%")
        print(f"    Reasoning:")
        for reason in kicker.reasoning[:3]:
            print(f"      • {reason}")
    
    # Build a 6-leg exotic parlay
    print("\n\n🎲 6-LEG EXOTIC PARLAY (with Kicker)")
    print("-" * 70)
    
    # Create sample exotic bets for parlay
    exotic_legs = [
        ExoticBet(
            bet_id="ex-1", game_id="g1", bet_type=ExoticBetType.FIRST_BASKET_SCORER,
            selection="Joel Embiid", odds=+620, ai_confidence=75.0,
            reasoning=["Tip off winner"], factors=["tip_off"],
            projected_probability=0.14, edge=0.02, bet_category="value_play"
        ),
        ExoticBet(
            bet_id="ex-2", game_id="g2", bet_type=ExoticBetType.RACE_TO_20,
            selection="Lakers", odds=+155, ai_confidence=68.0,
            reasoning=["Fast starters"], factors=["pace"],
            projected_probability=0.42, edge=0.03, bet_category="smart_money"
        ),
        ExoticBet(
            bet_id="ex-3", game_id="g3", bet_type=ExoticBetType.FIRST_QUARTER_WINNER,
            selection="Celtics", odds=-110, ai_confidence=72.0,
            reasoning=["Strong starters"], factors=["momentum"],
            projected_probability=0.52, edge=0.01, bet_category="smart_money"
        ),
        ExoticBet(
            bet_id="ex-4", game_id="g4", bet_type=ExoticBetType.FIRST_TEAM_TO_SCORE,
            selection="Nuggets", odds=+145, ai_confidence=65.0,
            reasoning=["Jokic tip advantage"], factors=["center"],
            projected_probability=0.41, edge=0.02, bet_category="value_play"
        ),
        ExoticBet(
            bet_id="ex-5", game_id="g5", bet_type=ExoticBetType.OVERTIME_YES_NO,
            selection="No", odds=-450, ai_confidence=88.0,
            reasoning=["Low OT probability"], factors=["regulation"],
            projected_probability=0.82, edge=0.01, bet_category="lock"
        ),
        ExoticBet(
            bet_id="ex-6", game_id="g6", bet_type=ExoticBetType.FIRST_BASKET_SCORER,
            selection="Long Shot Player", odds=+2500, ai_confidence=25.0,
            reasoning=["Kicker leg"], factors=["long_shot"],
            projected_probability=0.045, edge=0.008, bet_category="kicker"
        ),
    ]
    
    parlay_analysis = analyzer.build_exotic_parlay(exotic_legs, stake=10.0)
    
    print(f"\n  Combined Odds: {'+' if parlay_analysis['combined_odds'] > 0 else ''}{parlay_analysis['combined_odds']}")
    print(f"  Decimal Odds: {parlay_analysis['decimal_odds']:.2f}x")
    print(f"  True Probability: {parlay_analysis['true_probability']:.1%}")
    print(f"  Implied Probability: {parlay_analysis['implied_probability']:.1%}")
    print(f"  Expected Value: {parlay_analysis['expected_value']:+.3f}")
    print(f"  Potential Payout: ${parlay_analysis['potential_payout']:.2f} on $10 bet")
    print(f"  Risk Level: {parlay_analysis['risk_level']}")
    
    print("\n" + "=" * 70)
