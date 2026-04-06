"""
BetGenie — Player Impact Score Calculator (v1 Prototype)

This module implements the core Player Impact Score (PIS) algorithm.
The PIS is a composite score (0-100) representing a player's expected 
performance capacity, factoring in physical, emotional, psychological, 
and situational variables.

This is the PROTOTYPE. Production version will use trained ML models.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
import math


class EventCategory(Enum):
    """Categories of life events that can affect player performance."""
    LEGAL_ARREST = "legal_arrest"
    LEGAL_SUSPENSION = "legal_suspension"
    LEGAL_INVESTIGATION = "legal_investigation"
    FAMILY_POSITIVE = "family_positive"
    FAMILY_NEGATIVE = "family_negative"
    HEALTH_INJURY = "health_injury"
    HEALTH_RECOVERY = "health_recovery"
    FINANCIAL_POSITIVE = "financial_positive"
    FINANCIAL_NEGATIVE = "financial_negative"
    TEAM_TRADE = "team_trade"
    TEAM_COACHING = "team_coaching"
    SOCIAL_CONTROVERSY = "social_controversy"
    SOCIAL_POSITIVE = "social_positive"
    PERFORMANCE_STREAK_HOT = "performance_streak_hot"
    PERFORMANCE_STREAK_COLD = "performance_streak_cold"
    MEDIA_PRESSURE = "media_pressure"


class ImpactDirection(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class PlayerEvent:
    """Represents a life event affecting a player."""
    event_id: str
    player_id: str
    category: EventCategory
    description: str
    source_urls: list[str]
    sentiment_score: float  # -1.0 to 1.0
    severity: float  # 0.0 to 1.0
    date: datetime
    confidence: float  # 0.0 to 1.0 (how sure are we this is real)
    verified: bool = False  # True if confirmed by 2+ sources


@dataclass
class ImpactFactor:
    """A scored factor affecting a player's performance."""
    name: str
    category: EventCategory
    direction: ImpactDirection
    weight: float  # 0.0 to 1.0
    raw_impact: float  # percentage impact on performance (-1.0 to 1.0)
    decayed_impact: float  # impact after time decay
    source_event: Optional[PlayerEvent] = None


# Default impact profiles for each event category
# These will be replaced by ML model outputs in production
EVENT_IMPACT_PROFILES = {
    EventCategory.LEGAL_ARREST: {
        "base_impact": -0.20,  # -20% performance
        "decay_half_life_days": 14,  # Takes 2 weeks to halve
        "component": "emotional",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.LEGAL_SUSPENSION: {
        "base_impact": -0.30,
        "decay_half_life_days": 21,
        "component": "emotional",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.LEGAL_INVESTIGATION: {
        "base_impact": -0.10,
        "decay_half_life_days": 30,
        "component": "psychological",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.FAMILY_POSITIVE: {
        "base_impact": 0.05,
        "decay_half_life_days": 7,
        "component": "emotional",
        "direction": ImpactDirection.POSITIVE,
    },
    EventCategory.FAMILY_NEGATIVE: {
        "base_impact": -0.15,
        "decay_half_life_days": 14,
        "component": "emotional",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.HEALTH_INJURY: {
        "base_impact": -0.25,
        "decay_half_life_days": 7,
        "component": "physical",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.HEALTH_RECOVERY: {
        "base_impact": 0.08,
        "decay_half_life_days": 10,
        "component": "physical",
        "direction": ImpactDirection.POSITIVE,
    },
    EventCategory.FINANCIAL_POSITIVE: {
        "base_impact": 0.05,
        "decay_half_life_days": 7,
        "component": "psychological",
        "direction": ImpactDirection.POSITIVE,
    },
    EventCategory.FINANCIAL_NEGATIVE: {
        "base_impact": -0.10,
        "decay_half_life_days": 21,
        "component": "psychological",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.TEAM_TRADE: {
        "base_impact": -0.08,
        "decay_half_life_days": 14,
        "component": "situational",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.TEAM_COACHING: {
        "base_impact": -0.05,
        "decay_half_life_days": 21,
        "component": "situational",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.SOCIAL_CONTROVERSY: {
        "base_impact": -0.10,
        "decay_half_life_days": 5,
        "component": "psychological",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.SOCIAL_POSITIVE: {
        "base_impact": 0.03,
        "decay_half_life_days": 3,
        "component": "emotional",
        "direction": ImpactDirection.POSITIVE,
    },
    EventCategory.PERFORMANCE_STREAK_HOT: {
        "base_impact": 0.07,
        "decay_half_life_days": 5,
        "component": "psychological",
        "direction": ImpactDirection.POSITIVE,
    },
    EventCategory.PERFORMANCE_STREAK_COLD: {
        "base_impact": -0.07,
        "decay_half_life_days": 5,
        "component": "psychological",
        "direction": ImpactDirection.NEGATIVE,
    },
    EventCategory.MEDIA_PRESSURE: {
        "base_impact": -0.05,
        "decay_half_life_days": 7,
        "component": "psychological",
        "direction": ImpactDirection.NEGATIVE,
    },
}

# Component weights for overall Impact Score
COMPONENT_WEIGHTS = {
    "physical": 0.30,
    "emotional": 0.25,
    "psychological": 0.25,
    "situational": 0.20,
}


def calculate_time_decay(base_impact: float, half_life_days: float, 
                          days_elapsed: float) -> float:
    """
    Calculate the decayed impact of an event over time.
    Uses exponential decay: impact * (0.5 ^ (days / half_life))
    """
    if days_elapsed < 0:
        return 0.0
    decay_factor = math.pow(0.5, days_elapsed / half_life_days)
    return base_impact * decay_factor


def calculate_impact_score(
    events: list[PlayerEvent],
    current_time: Optional[datetime] = None,
    base_score: float = 75.0,
) -> dict:
    """
    Calculate the Player Impact Score from a list of events.
    
    Args:
        events: List of PlayerEvent objects affecting this player
        current_time: Reference time (defaults to now)
        base_score: Default score when no events are present (0-100)
    
    Returns:
        Dictionary with overall score, component scores, and active factors
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # Initialize component scores at baseline
    component_scores = {
        "physical": base_score,
        "emotional": base_score,
        "psychological": base_score,
        "situational": base_score,
    }
    
    active_factors = []
    
    for event in events:
        profile = EVENT_IMPACT_PROFILES.get(event.category)
        if profile is None:
            continue
        
        # Calculate time since event
        days_elapsed = (current_time - event.date).total_seconds() / 86400
        
        # Skip events older than 60 days (negligible impact)
        if days_elapsed > 60:
            continue
        
        # Calculate decayed impact
        decayed_impact = calculate_time_decay(
            base_impact=profile["base_impact"] * event.severity,
            half_life_days=profile["decay_half_life_days"],
            days_elapsed=days_elapsed,
        )
        
        # Apply confidence weighting
        weighted_impact = decayed_impact * event.confidence
        
        # Boost verified events
        if event.verified:
            weighted_impact *= 1.2
        
        # Apply to the relevant component (convert to 0-100 scale)
        component = profile["component"]
        impact_on_score = weighted_impact * 100  # e.g., -0.15 -> -15 points
        component_scores[component] += impact_on_score
        
        # Clamp to 0-100
        component_scores[component] = max(0, min(100, component_scores[component]))
        
        # Record active factor
        if abs(weighted_impact) > 0.01:  # Only track meaningful impacts
            active_factors.append(ImpactFactor(
                name=event.description[:80],
                category=event.category,
                direction=profile["direction"],
                weight=abs(weighted_impact),
                raw_impact=profile["base_impact"] * event.severity,
                decayed_impact=weighted_impact,
                source_event=event,
            ))
    
    # Calculate overall score as weighted average of components
    overall_score = sum(
        component_scores[comp] * weight
        for comp, weight in COMPONENT_WEIGHTS.items()
    )
    overall_score = max(0, min(100, overall_score))
    
    # Sort factors by absolute impact (most impactful first)
    active_factors.sort(key=lambda f: abs(f.decayed_impact), reverse=True)
    
    return {
        "overall": round(overall_score, 1),
        "physical": round(component_scores["physical"], 1),
        "emotional": round(component_scores["emotional"], 1),
        "psychological": round(component_scores["psychological"], 1),
        "situational": round(component_scores["situational"], 1),
        "active_factors": active_factors,
        "calculated_at": current_time.isoformat(),
    }


# ============================================================
# EXAMPLE USAGE / DEMO
# ============================================================

if __name__ == "__main__":
    # Demo: Jamal Murray with a DUI arrest
    now = datetime.now(timezone.utc)
    
    events = [
        PlayerEvent(
            event_id="evt-001",
            player_id="jamal-murray-den",
            category=EventCategory.LEGAL_ARREST,
            description="Arrested for DUI on Feb 28, 2026",
            source_urls=["https://espn.com/example", "https://tmz.com/example"],
            sentiment_score=-0.85,
            severity=0.80,
            date=now - timedelta(days=2),  # 2 days ago
            confidence=0.92,
            verified=True,
        ),
        PlayerEvent(
            event_id="evt-002",
            player_id="jamal-murray-den",
            category=EventCategory.MEDIA_PRESSURE,
            description="Heavy media scrutiny following DUI arrest",
            source_urls=["https://espn.com/example2"],
            sentiment_score=-0.70,
            severity=0.65,
            date=now - timedelta(days=1),  # 1 day ago
            confidence=0.88,
            verified=True,
        ),
        PlayerEvent(
            event_id="evt-003",
            player_id="jamal-murray-den",
            category=EventCategory.SOCIAL_CONTROVERSY,
            description="Social media accounts have gone silent",
            source_urls=["https://twitter.com/example"],
            sentiment_score=-0.40,
            severity=0.30,
            date=now - timedelta(hours=18),
            confidence=0.70,
            verified=False,
        ),
    ]
    
    result = calculate_impact_score(events, current_time=now)
    
    print("=" * 60)
    print("  BETGENIE — PLAYER IMPACT SCORE")
    print("  Player: Jamal Murray (DEN)")
    print("=" * 60)
    print(f"\n  Overall Score:   {result['overall']} / 100")
    print(f"  Physical:        {result['physical']}")
    print(f"  Emotional:       {result['emotional']}")
    print(f"  Psychological:   {result['psychological']}")
    print(f"  Situational:     {result['situational']}")
    print(f"\n  Active Factors ({len(result['active_factors'])}):")
    for factor in result['active_factors']:
        icon = "🔴" if factor.direction == ImpactDirection.NEGATIVE else "🟢"
        print(f"    {icon} {factor.name}")
        print(f"       Impact: {factor.decayed_impact:+.3f} | Weight: {factor.weight:.3f}")
    print(f"\n  Calculated at: {result['calculated_at']}")
    print("=" * 60)
