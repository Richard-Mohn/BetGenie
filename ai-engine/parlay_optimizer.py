"""
BetGenie — Parlay Optimizer (v1 Prototype)

This module implements the Smart Parlay Builder that uses Player Impact Scores
and correlation analysis to construct optimized multi-leg parlays.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import math


class PropType(Enum):
    POINTS = "points"
    REBOUNDS = "rebounds"
    ASSISTS = "assists"
    THREES = "threes"
    STEALS = "steals"
    BLOCKS = "blocks"
    PASS_YARDS = "pass_yards"
    RUSH_YARDS = "rush_yards"
    RECEIVING_YARDS = "receiving_yards"
    TOUCHDOWNS = "touchdowns"
    STRIKEOUTS = "strikeouts"
    HITS = "hits"
    GOALS = "goals"
    SHOTS_ON_GOAL = "shots_on_goal"


class BetDirection(Enum):
    OVER = "over"
    UNDER = "under"


@dataclass
class PropBet:
    """A single player prop bet."""
    player_id: str
    player_name: str
    team: str
    sport: str
    game_id: str
    prop_type: PropType
    line: float
    direction: BetDirection
    odds: int  # American odds (e.g., -110, +150)
    ai_confidence: float  # 0-100
    impact_score: float  # Player's current Impact Score
    key_factors: list[str]  # Human-readable factor descriptions
    projected_value: float  # AI's projected stat
    edge: float  # Projected value vs line (positive = edge exists)


@dataclass
class ParlayLeg:
    """A single leg of a parlay."""
    prop: PropBet
    leg_number: int
    correlation_warnings: list[str]


@dataclass
class SmartParlay:
    """An AI-optimized parlay."""
    legs: list[ParlayLeg]
    total_odds: int  # Combined American odds
    implied_probability: float  # Combined probability
    ai_confidence: float  # Overall confidence (0-100)
    expected_value: float  # Expected value per dollar
    payout_multiplier: float  # e.g., +850 means 9.5x
    warnings: list[str]
    suggestions: list[str]


def american_to_decimal(american_odds: int) -> float:
    """Convert American odds to decimal odds."""
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1


def american_to_implied_prob(american_odds: int) -> float:
    """Convert American odds to implied probability."""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)


def decimal_to_american(decimal_odds: float) -> int:
    """Convert decimal odds to American odds."""
    if decimal_odds >= 2.0:
        return round((decimal_odds - 1) * 100)
    else:
        return round(-100 / (decimal_odds - 1))


def check_correlation(leg1: PropBet, leg2: PropBet) -> list[str]:
    """
    Check if two parlay legs are correlated (which affects true probability).
    Correlated legs reduce the independence assumption that parlays rely on.
    """
    warnings = []
    
    # Same game correlation
    if leg1.game_id == leg2.game_id:
        warnings.append(
            f"Same game: {leg1.player_name} and {leg2.player_name} "
            f"are in the same game — outcomes may be correlated"
        )
    
    # Same team correlation
    if leg1.team == leg2.team:
        warnings.append(
            f"Same team: {leg1.player_name} and {leg2.player_name} "
            f"are teammates — their stats are correlated"
        )
    
    # Opposing players in same game
    if leg1.game_id == leg2.game_id and leg1.team != leg2.team:
        if leg1.prop_type == leg2.prop_type:
            warnings.append(
                f"Head-to-head: Both props are {leg1.prop_type.value} "
                f"in the same game — game pace affects both"
            )
    
    return warnings


def score_parlay(legs: list[PropBet]) -> SmartParlay:
    """
    Score and analyze a parlay built from prop bets.
    
    Returns a SmartParlay with confidence scoring, correlation analysis,
    and optimization suggestions.
    """
    parlay_legs = []
    all_warnings = []
    all_suggestions = []
    
    # Build legs and check correlations
    for i, prop in enumerate(legs):
        leg_warnings = []
        
        # Check correlation with every other leg
        for j, other_prop in enumerate(legs):
            if i != j:
                correlations = check_correlation(prop, other_prop)
                leg_warnings.extend(correlations)
        
        # Deduplicate warnings
        leg_warnings = list(set(leg_warnings))
        all_warnings.extend(leg_warnings)
        
        parlay_legs.append(ParlayLeg(
            prop=prop,
            leg_number=i + 1,
            correlation_warnings=leg_warnings,
        ))
    
    # Calculate combined odds
    combined_decimal = 1.0
    combined_ai_prob = 1.0
    
    for leg in parlay_legs:
        decimal_odds = american_to_decimal(leg.prop.odds)
        combined_decimal *= decimal_odds
        
        # AI's estimated actual probability
        ai_prob = leg.prop.ai_confidence / 100
        combined_ai_prob *= ai_prob
    
    total_american = decimal_to_american(combined_decimal)
    implied_prob = 1 / combined_decimal
    
    # Calculate AI confidence for the parlay
    base_confidence = combined_ai_prob * 100
    
    # Apply penalties
    correlation_penalty = len(set(all_warnings)) * 3  # -3 per unique correlation
    leg_penalty = max(0, (len(legs) - 3) * 5)  # -5 per leg beyond 3
    
    # Apply bonuses
    diversity_bonus = len(set(l.prop.sport for l in parlay_legs)) * 2  # +2 per unique sport
    high_confidence_bonus = sum(2 for l in parlay_legs if l.prop.ai_confidence > 75)
    
    adjusted_confidence = (
        base_confidence 
        - correlation_penalty 
        - leg_penalty 
        + diversity_bonus 
        + high_confidence_bonus
    )
    adjusted_confidence = max(5, min(95, adjusted_confidence))
    
    # Expected value calculation
    # EV = (probability of winning * payout) - (probability of losing * stake)
    payout_multiplier = combined_decimal
    ev = (combined_ai_prob * payout_multiplier) - ((1 - combined_ai_prob) * 1)
    
    # Generate suggestions
    if len(legs) > 4:
        all_suggestions.append(
            "Consider reducing to 3-4 legs for better hit rate. "
            "More legs exponentially reduces probability."
        )
    
    # Find weakest leg
    weakest = min(parlay_legs, key=lambda l: l.prop.ai_confidence)
    if weakest.prop.ai_confidence < 55:
        all_suggestions.append(
            f"Leg {weakest.leg_number} ({weakest.prop.player_name} "
            f"{weakest.prop.direction.value} {weakest.prop.line} "
            f"{weakest.prop.prop_type.value}) has low confidence "
            f"({weakest.prop.ai_confidence}%). Consider replacing."
        )
    
    all_warnings = list(set(all_warnings))
    
    return SmartParlay(
        legs=parlay_legs,
        total_odds=total_american,
        implied_probability=implied_prob,
        ai_confidence=round(adjusted_confidence, 1),
        expected_value=round(ev, 3),
        payout_multiplier=round(payout_multiplier, 2),
        warnings=all_warnings,
        suggestions=all_suggestions,
    )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Demo: Build and analyze a 4-leg parlay
    
    legs = [
        PropBet(
            player_id="jamal-murray-den",
            player_name="Jamal Murray",
            team="Denver Nuggets",
            sport="NBA",
            game_id="nba-2026-03-02-den-uta",
            prop_type=PropType.POINTS,
            line=24.5,
            direction=BetDirection.UNDER,
            odds=-110,
            ai_confidence=76,
            impact_score=62,
            key_factors=["DUI arrest (Feb 28)", "Media scrutiny", "Social media silent"],
            projected_value=21.5,
            edge=3.0,
        ),
        PropBet(
            player_id="bobby-portis-mil",
            player_name="Bobby Portis",
            team="Milwaukee Bucks",
            sport="NBA",
            game_id="nba-2026-03-02-bos-mil",
            prop_type=PropType.POINTS,
            line=18.5,
            direction=BetDirection.OVER,
            odds=-115,
            ai_confidence=77,
            impact_score=88,
            key_factors=["Daughter promoted at work", "Confidence high", "Home game"],
            projected_value=22.0,
            edge=3.5,
        ),
        PropBet(
            player_id="luka-doncic-dal",
            player_name="Luka Doncic",
            team="Dallas Mavericks",
            sport="NBA",
            game_id="nba-2026-03-02-dal-gsw",
            prop_type=PropType.ASSISTS,
            line=9.5,
            direction=BetDirection.OVER,
            odds=+100,
            ai_confidence=68,
            impact_score=79,
            key_factors=["Revenge game", "Home crowd", "Well rested"],
            projected_value=10.8,
            edge=1.3,
        ),
        PropBet(
            player_id="patrick-mahomes-kc",
            player_name="Patrick Mahomes",
            team="Kansas City Chiefs",
            sport="NFL",
            game_id="nfl-2026-03-02-kc-buf",
            prop_type=PropType.PASS_YARDS,
            line=275.5,
            direction=BetDirection.UNDER,
            odds=-105,
            ai_confidence=61,
            impact_score=65,
            key_factors=["Ankle concern", "Wind advisory", "Short week"],
            projected_value=258.0,
            edge=17.5,
        ),
    ]
    
    parlay = score_parlay(legs)
    
    print("=" * 65)
    print("  BETGENIE — SMART PARLAY ANALYSIS")
    print("=" * 65)
    print(f"\n  Total Odds: {'+' if parlay.total_odds > 0 else ''}{parlay.total_odds}")
    print(f"  Payout Multiplier: {parlay.payout_multiplier}x")
    print(f"  AI Confidence: {parlay.ai_confidence}%")
    print(f"  Expected Value: {'+' if parlay.expected_value > 0 else ''}{parlay.expected_value}")
    print(f"  Implied Probability: {parlay.implied_probability:.1%}")
    
    print(f"\n  LEGS ({len(parlay.legs)}):")
    for leg in parlay.legs:
        p = leg.prop
        print(f"\n  Leg {leg.leg_number}: {p.player_name}")
        print(f"    {p.direction.value.upper()} {p.line} {p.prop_type.value}")
        print(f"    Odds: {'+' if p.odds > 0 else ''}{p.odds} | "
              f"Confidence: {p.ai_confidence}% | "
              f"PIS: {p.impact_score}")
        print(f"    Projected: {p.projected_value} | Edge: {p.edge:+.1f}")
        print(f"    Factors: {', '.join(p.key_factors)}")
    
    if parlay.warnings:
        print(f"\n  WARNINGS:")
        for w in parlay.warnings:
            print(f"    ⚠️  {w}")
    
    if parlay.suggestions:
        print(f"\n  SUGGESTIONS:")
        for s in parlay.suggestions:
            print(f"    💡 {s}")
    
    print("\n" + "=" * 65)
