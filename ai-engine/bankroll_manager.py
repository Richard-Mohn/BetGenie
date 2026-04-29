"""
BetGenie — Bankroll Management System

This module implements Kelly Criterion and conservative bankroll management
to recommend bet sizes based on confidence levels and edge size.

Key Principles:
- Never bet more than 2-3% of bankroll on a single bet
- Use Kelly Criterion for optimal bet sizing (with fractional Kelly for safety)
- Adjust bet size based on AI confidence and edge
- Provide clear risk management guidance
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum
import math


class RiskProfile(Enum):
    CONSERVATIVE = "conservative"  # 0.25 Kelly, max 1% per bet
    MODERATE = "moderate"          # 0.5 Kelly, max 2% per bet
    AGGRESSIVE = "aggressive"      # 0.75 Kelly, max 3% per bet
    PRO = "pro"                    # Full Kelly, max 5% per bet


@dataclass
class BetRecommendation:
    """A single bet recommendation with bankroll guidance."""
    bet_type: str  # "straight", "parlay"
    description: str
    confidence: float  # 0-100
    odds: int  # American odds
    implied_probability: float
    true_probability: float  # AI's estimated probability
    edge: float  # Percentage edge
    recommended_amount: float  # Dollar amount
    percentage_of_bankroll: float
    expected_value: float
    risk_level: str
    reasoning: List[str]


@dataclass
class BankrollSession:
    """A betting session with multiple recommendations."""
    total_bankroll: float
    risk_profile: RiskProfile
    recommendations: List[BetRecommendation]
    total_exposure: float
    total_expected_value: float
    session_start: datetime
    notes: str


class BankrollManager:
    """Manages bankroll and bet sizing using Kelly Criterion."""
    
    def __init__(self, bankroll: float, risk_profile: RiskProfile = RiskProfile.MODERATE):
        self.bankroll = bankroll
        self.risk_profile = risk_profile
        self.bet_history = []
    
    def calculate_kelly_fraction(
        self, 
        true_probability: float, 
        odds: int,
        kelly_multiplier: float = 0.5
    ) -> float:
        """
        Calculate optimal bet fraction using Kelly Criterion.
        
        Kelly Formula: f* = (bp - q) / b
        Where:
        - b = decimal odds - 1
        - p = probability of winning
        - q = probability of losing (1 - p)
        
        Returns fraction of bankroll to bet (0 to 1).
        """
        # Convert American odds to decimal
        if odds > 0:
            decimal_odds = (odds / 100) + 1
        else:
            decimal_odds = (100 / abs(odds)) + 1
        
        b = decimal_odds - 1
        p = true_probability
        q = 1 - p
        
        # Kelly formula
        kelly_fraction = (b * p - q) / b
        
        # Apply safety multiplier (fractional Kelly)
        kelly_fraction *= kelly_multiplier
        
        # Clamp to 0-1 range (never bet more than bankroll)
        return max(0, min(1, kelly_fraction))
    
    def get_max_bet_percentage(self) -> float:
        """Get maximum allowed bet percentage based on risk profile."""
        limits = {
            RiskProfile.CONSERVATIVE: 0.01,  # 1%
            RiskProfile.MODERATE: 0.02,      # 2%
            RiskProfile.AGGRESSIVE: 0.03,    # 3%
            RiskProfile.PRO: 0.05,           # 5%
        }
        return limits.get(self.risk_profile, 0.02)
    
    def get_kelly_multiplier(self) -> float:
        """Get Kelly multiplier based on risk profile."""
        multipliers = {
            RiskProfile.CONSERVATIVE: 0.25,
            RiskProfile.MODERATE: 0.5,
            RiskProfile.AGGRESSIVE: 0.75,
            RiskProfile.PRO: 1.0,
        }
        return multipliers.get(self.risk_profile, 0.5)
    
    def recommend_bet(
        self,
        description: str,
        confidence: float,
        odds: int,
        bet_type: str = "straight"
    ) -> BetRecommendation:
        """
        Generate a bet recommendation with optimal sizing.
        
        Args:
            description: Human-readable bet description
            confidence: AI confidence (0-100)
            odds: American odds (e.g., -110, +150)
            bet_type: "straight" or "parlay"
        """
        # Convert confidence to probability
        true_probability = confidence / 100
        
        # Calculate implied probability from odds
        if odds > 0:
            implied_prob = 100 / (odds + 100)
        else:
            implied_prob = abs(odds) / (abs(odds) + 100)
        
        # Calculate edge
        edge = (true_probability - implied_prob) * 100
        
        # Calculate Kelly fraction
        kelly_mult = self.get_kelly_multiplier()
        kelly_fraction = self.calculate_kelly_fraction(true_probability, odds, kelly_mult)
        
        # Apply max bet limit
        max_pct = self.get_max_bet_percentage()
        bet_percentage = min(kelly_fraction, max_pct)
        
        # Calculate dollar amount
        bet_amount = self.bankroll * bet_percentage
        
        # Calculate expected value
        if odds > 0:
            decimal_odds = (odds / 100) + 1
        else:
            decimal_odds = (100 / abs(odds)) + 1
        
        ev = (true_probability * decimal_odds) - ((1 - true_probability) * 1)
        
        # Determine risk level
        if confidence >= 75:
            risk_level = "LOW"
        elif confidence >= 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        # Generate reasoning
        reasoning = [
            f"AI Confidence: {confidence}%",
            f"Implied Probability: {implied_prob:.1%}",
            f"True Probability: {true_probability:.1%}",
            f"Edge: {edge:+.1f}%",
        ]
        
        if edge > 5:
            reasoning.append("Strong positive edge detected")
        elif edge > 0:
            reasoning.append("Moderate positive edge")
        else:
            reasoning.append("Negative or no edge - consider skipping")
        
        if bet_percentage < max_pct * 0.5:
            reasoning.append("Bet size limited by Kelly Criterion")
        else:
            reasoning.append("Bet size at maximum allowed for risk profile")
        
        return BetRecommendation(
            bet_type=bet_type,
            description=description,
            confidence=confidence,
            odds=odds,
            implied_probability=implied_prob,
            true_probability=true_probability,
            edge=edge,
            recommended_amount=round(bet_amount, 2),
            percentage_of_bankroll=round(bet_percentage * 100, 2),
            expected_value=round(ev, 3),
            risk_level=risk_level,
            reasoning=reasoning,
        )
    
    def create_session(
        self, 
        recommendations: List[BetRecommendation],
        notes: str = ""
    ) -> BankrollSession:
        """Create a betting session with multiple recommendations."""
        total_exposure = sum(r.recommended_amount for r in recommendations)
        total_ev = sum(r.expected_value * r.recommended_amount for r in recommendations)
        
        # Warn if total exposure exceeds 10% of bankroll
        if total_exposure > self.bankroll * 0.10:
            notes += f" WARNING: Total exposure ({total_exposure:.2f}) exceeds 10% of bankroll"
        
        return BankrollSession(
            total_bankroll=self.bankroll,
            risk_profile=self.risk_profile,
            recommendations=recommendations,
            total_exposure=total_exposure,
            total_expected_value=total_ev,
            session_start=datetime.now(),
            notes=notes,
        )
    
    def update_bankroll(self, result: str, amount: float):
        """Update bankroll after a bet result."""
        if result == "win":
            self.bankroll += amount
        elif result == "loss":
            self.bankroll -= amount
        elif result == "push":
            pass  # No change
        
        self.bet_history.append({
            "result": result,
            "amount": amount,
            "new_bankroll": self.bankroll,
            "timestamp": datetime.now(),
        })


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — BANKROLL MANAGEMENT SYSTEM")
    print("=" * 70)
    
    # Example: $500 bankroll with moderate risk
    manager = BankrollManager(bankroll=500.00, risk_profile=RiskProfile.MODERATE)
    
    print(f"\nBankroll: ${manager.bankroll:.2f}")
    print(f"Risk Profile: {manager.risk_profile.value}")
    print(f"Max Bet: {manager.get_max_bet_percentage() * 100}% of bankroll")
    print(f"Kelly Multiplier: {manager.get_kelly_multiplier()}")
    
    # Generate some bet recommendations
    print("\n" + "-" * 70)
    print("  BET RECOMMENDATIONS")
    print("-" * 70)
    
    recommendations = [
        manager.recommend_bet(
            description="LeBron James OVER 23.5 points",
            confidence=72,
            odds=-110,
            bet_type="straight"
        ),
        manager.recommend_bet(
            description="Luka Doncic OVER 28.5 points",
            confidence=68,
            odds=-110,
            bet_type="straight"
        ),
        manager.recommend_bet(
            description="SGA UNDER 31.5 points",
            confidence=65,
            odds=-105,
            bet_type="straight"
        ),
        manager.recommend_bet(
            description="3-Leg Parlay: LeBron O23.5 + Luka O28.5 + SGA U31.5",
            confidence=55,
            odds=+590,
            bet_type="parlay"
        ),
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n#{i} {rec.description}")
        print(f"    Type: {rec.bet_type.upper()}")
        print(f"    Odds: {'+' if rec.odds > 0 else ''}{rec.odds}")
        print(f"    Confidence: {rec.confidence}%")
        print(f"    Edge: {rec.edge:+.1f}%")
        print(f"    Risk Level: {rec.risk_level}")
        print(f"    Recommended Bet: ${rec.recommended_amount:.2f} ({rec.percentage_of_bankroll}% of bankroll)")
        print(f"    Expected Value: {rec.expected_value:+.3f}")
        print(f"    Reasoning:")
        for reason in rec.reasoning:
            print(f"      - {reason}")
    
    # Create session
    print("\n" + "-" * 70)
    print("  SESSION SUMMARY")
    print("-" * 70)
    
    session = manager.create_session(recommendations)
    
    print(f"\nTotal Bankroll: ${session.total_bankroll:.2f}")
    print(f"Total Exposure: ${session.total_exposure:.2f} ({session.total_exposure/session.total_bankroll*100:.1f}%)")
    print(f"Total Expected Value: ${session.total_expected_value:.2f}")
    print(f"Number of Bets: {len(session.recommendations)}")
    
    if session.notes:
        print(f"\nNotes: {session.notes}")
    
    print("\n" + "=" * 70)
