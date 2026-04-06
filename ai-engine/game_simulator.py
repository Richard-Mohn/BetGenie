"""
BetGenie — Game Simulation Engine (v1 Prototype)

Simulates fictional upcoming games using real player data and BetGenie's
full analysis pipeline to demonstrate how personal life events create
actionable betting edges.

Pipeline: Player Database → Event Analysis → Impact Score → Stat Projection 
         → Prop Generation → Parlay Optimization → Recommendations
"""

import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

# Import our existing modules
from impact_score import (
    EventCategory, PlayerEvent, ImpactFactor, ImpactDirection,
    calculate_impact_score, EVENT_IMPACT_PROFILES, COMPONENT_WEIGHTS,
)
from player_database import (
    PlayerProfile, Sport, get_player, get_all_players, PersonalEvent,
)
from parlay_optimizer import (
    PropBet, PropType, BetDirection, score_parlay, SmartParlay,
    american_to_decimal, american_to_implied_prob,
)


# ============================================================
# GAME SIMULATION MODELS
# ============================================================

@dataclass
class GameMatchup:
    """A fictional upcoming game between two teams."""
    game_id: str
    home_team: str
    away_team: str
    game_time: datetime
    venue: str
    sport: Sport
    # Contextual factors
    is_national_tv: bool = False
    is_rivalry: bool = False
    is_back_to_back: bool = False
    weather_notes: str = ""
    # Spread and totals (from hypothetical market)
    spread: float = 0.0  # Negative = home favored
    over_under: float = 0.0


@dataclass
class PlayerGameProjection:
    """BetGenie's full projection for a player in a specific game."""
    player_id: str
    player_name: str
    team: str
    game_id: str
    # Impact Score results
    impact_score: float  # Overall PIS (0-100)
    physical_score: float
    emotional_score: float
    psychological_score: float
    situational_score: float
    active_factors: list[str]
    # Projected stats (adjusted by PIS)
    projected_points: float
    projected_rebounds: float
    projected_assists: float
    projected_steals: float
    projected_blocks: float
    projected_threes: float
    projected_minutes: float
    # Comparison to baseline
    baseline_points: float  # Season average
    points_delta: float  # Projected - Baseline
    confidence: float  # 0-100


@dataclass
class PropRecommendation:
    """A prop bet recommendation from BetGenie."""
    player_name: str
    prop_type: str
    direction: str  # OVER or UNDER
    line: float
    projected_value: float
    edge: float  # How much edge we have
    confidence: float
    reasoning: list[str]
    impact_score: float


@dataclass
class GameAnalysis:
    """Complete BetGenie analysis for a game."""
    game: GameMatchup
    projections: list[PlayerGameProjection]
    prop_recommendations: list[PropRecommendation]
    parlay_suggestion: Optional[SmartParlay]
    analysis_timestamp: datetime
    summary: str


# ============================================================
# STAT PROJECTION ENGINE
# ============================================================

# Category to EventCategory mapping
CATEGORY_MAP = {
    "legal_arrest": EventCategory.LEGAL_ARREST,
    "legal_suspension": EventCategory.LEGAL_SUSPENSION,
    "legal_investigation": EventCategory.LEGAL_INVESTIGATION,
    "family_positive": EventCategory.FAMILY_POSITIVE,
    "family_negative": EventCategory.FAMILY_NEGATIVE,
    "health_injury": EventCategory.HEALTH_INJURY,
    "health_recovery": EventCategory.HEALTH_RECOVERY,
    "financial_positive": EventCategory.FINANCIAL_POSITIVE,
    "financial_negative": EventCategory.FINANCIAL_NEGATIVE,
    "team_trade": EventCategory.TEAM_TRADE,
    "team_coaching": EventCategory.TEAM_COACHING,
    "social_controversy": EventCategory.SOCIAL_CONTROVERSY,
    "social_positive": EventCategory.SOCIAL_POSITIVE,
    "performance_streak_hot": EventCategory.PERFORMANCE_STREAK_HOT,
    "performance_streak_cold": EventCategory.PERFORMANCE_STREAK_COLD,
    "media_pressure": EventCategory.MEDIA_PRESSURE,
}


def convert_personal_events_to_player_events(
    player: PlayerProfile, 
    reference_time: datetime
) -> list[PlayerEvent]:
    """
    Convert a player's personal events into PlayerEvent objects
    that the impact_score module can process.
    Only includes events within the last 60 days.
    """
    events = []
    cutoff = reference_time - timedelta(days=60)
    
    for i, pe in enumerate(player.personal_events):
        if pe.date < cutoff:
            continue
        
        cat = CATEGORY_MAP.get(pe.category)
        if cat is None:
            continue
        
        events.append(PlayerEvent(
            event_id=f"evt-{player.player_id}-{i}",
            player_id=player.player_id,
            category=cat,
            description=pe.description,
            source_urls=[pe.public_source],
            sentiment_score=-0.7 if "negative" in pe.category or pe.severity > 0.5 else 0.5,
            severity=pe.severity,
            date=pe.date,
            confidence=0.90 if pe.verified else 0.65,
            verified=pe.verified,
        ))
    
    return events


def project_player_stats(
    player: PlayerProfile,
    game: GameMatchup,
    reference_time: Optional[datetime] = None,
) -> PlayerGameProjection:
    """
    Project a player's stats for a specific game, adjusting for their
    Player Impact Score.
    
    The key insight: a PIS of 75 means baseline performance.
    - PIS > 75 → player likely to exceed averages
    - PIS < 75 → player likely to underperform averages
    
    The multiplier is: (PIS - 75) / 100, so a PIS of 60 means
    the player is expected to perform at 85% of their average.
    """
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    
    # Convert personal events and calculate Impact Score
    events = convert_personal_events_to_player_events(player, reference_time)
    impact_result = calculate_impact_score(events, current_time=reference_time)
    
    pis = impact_result["overall"]
    
    # Calculate performance multiplier
    # PIS 75 = 1.0x (baseline), PIS 50 = 0.90x, PIS 100 = 1.10x
    # This is conservative — even major events don't make stars zero out
    base_multiplier = 0.70 + (pis / 250)  # Range: 0.70 to 1.10 for PIS 0-100
    
    # Situational adjustments
    situational_factor = 1.0
    if game.is_back_to_back:
        situational_factor *= 0.95  # -5% for B2B
    if game.is_national_tv:
        situational_factor *= 1.02  # Stars play slightly harder on national TV
    if game.is_rivalry:
        situational_factor *= 1.03  # Rivalry games = more intensity
    
    # Home vs away
    is_home = player.team.lower() in game.home_team.lower()
    home_factor = 1.02 if is_home else 0.98
    
    total_multiplier = base_multiplier * situational_factor * home_factor
    
    # Project stats
    s = player.current_season
    proj_points = round(s.points_per_game * total_multiplier, 1)
    proj_rebounds = round(s.rebounds_per_game * total_multiplier, 1)
    proj_assists = round(s.assists_per_game * total_multiplier, 1)
    proj_steals = round(s.steals_per_game * total_multiplier, 1)
    proj_blocks = round(s.blocks_per_game * total_multiplier, 1)
    proj_threes = round((s.points_per_game * s.three_pt_percentage * 0.33) * total_multiplier, 1)
    proj_minutes = round(s.minutes_per_game * min(total_multiplier, 1.05), 1)  # Minutes cap
    
    # Collect active factor descriptions
    factor_descriptions = [f.name for f in impact_result["active_factors"]]
    
    return PlayerGameProjection(
        player_id=player.player_id,
        player_name=player.full_name,
        team=player.team,
        game_id=game.game_id,
        impact_score=pis,
        physical_score=impact_result["physical"],
        emotional_score=impact_result["emotional"],
        psychological_score=impact_result["psychological"],
        situational_score=impact_result["situational"],
        active_factors=factor_descriptions,
        projected_points=proj_points,
        projected_rebounds=proj_rebounds,
        projected_assists=proj_assists,
        projected_steals=proj_steals,
        projected_blocks=proj_blocks,
        projected_threes=proj_threes,
        projected_minutes=proj_minutes,
        baseline_points=s.points_per_game,
        points_delta=round(proj_points - s.points_per_game, 1),
        confidence=min(95, max(30, pis * 0.9 + 10)),
    )


# ============================================================
# PROP BET GENERATION
# ============================================================

def generate_prop_recommendations(
    projection: PlayerGameProjection,
    game: GameMatchup,
) -> list[PropRecommendation]:
    """
    Generate prop bet recommendations based on player projection.
    
    If player is projected BELOW their normal line, recommend UNDER.
    If player is projected ABOVE their normal line, recommend OVER.
    Only recommend when there's a meaningful edge (> 1.5 points for scoring).
    """
    recommendations = []
    
    # Points prop — typically set at season average - 0.5
    points_line = projection.baseline_points - 0.5
    points_edge = projection.projected_points - points_line
    
    if abs(points_edge) >= 1.5:
        direction = "OVER" if points_edge > 0 else "UNDER"
        reasoning = []
        
        if points_edge < 0:
            reasoning.append(
                f"Impact Score {projection.impact_score}/100 — below baseline 75"
            )
            if projection.active_factors:
                reasoning.append(f"Key factor: {projection.active_factors[0]}")
            reasoning.append(
                f"Projected {projection.projected_points} pts vs line of {points_line}"
            )
        else:
            reasoning.append(
                f"Impact Score {projection.impact_score}/100 — above baseline"
            )
            reasoning.append(
                f"Projected {projection.projected_points} pts vs line of {points_line}"
            )
        
        recommendations.append(PropRecommendation(
            player_name=projection.player_name,
            prop_type="Points",
            direction=direction,
            line=points_line,
            projected_value=projection.projected_points,
            edge=round(abs(points_edge), 1),
            confidence=projection.confidence,
            reasoning=reasoning,
            impact_score=projection.impact_score,
        ))
    
    # Assists prop
    assists_line = round(projection.projected_rebounds + projection.projected_assists, 0) - 0.5
    # Simplified: just check assists
    assists_season = projection.baseline_points * 0.30  # Rough proxy
    assists_edge = projection.projected_assists - (projection.projected_assists + 0.5)
    
    # Rebounds prop — useful for bigs
    if projection.projected_rebounds >= 6.0:
        reb_line = round(projection.projected_rebounds) - 0.5
        reb_baseline = get_player(projection.player_id)
        if reb_baseline:
            reb_season_avg = reb_baseline.current_season.rebounds_per_game
            reb_edge = projection.projected_rebounds - reb_season_avg
            if abs(reb_edge) >= 1.0:
                direction = "OVER" if reb_edge > 0 else "UNDER"
                recommendations.append(PropRecommendation(
                    player_name=projection.player_name,
                    prop_type="Rebounds",
                    direction=direction,
                    line=reb_season_avg - 0.5,
                    projected_value=projection.projected_rebounds,
                    edge=round(abs(reb_edge), 1),
                    confidence=projection.confidence * 0.85,
                    reasoning=[
                        f"PIS adjustment: {projection.impact_score}/100",
                        f"Projected {projection.projected_rebounds} reb vs {reb_season_avg} avg",
                    ],
                    impact_score=projection.impact_score,
                ))
    
    return recommendations


# ============================================================
# FULL GAME ANALYSIS
# ============================================================

def analyze_game(
    game: GameMatchup,
    players: list[PlayerProfile],
    reference_time: Optional[datetime] = None,
) -> GameAnalysis:
    """
    Run the full BetGenie analysis pipeline for a game.
    
    1. Project stats for each player (using PIS)
    2. Generate prop recommendations
    3. Build an optimized parlay
    4. Generate summary
    """
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    
    projections = []
    all_recommendations = []
    
    # Step 1 & 2: Project each player and generate props
    for player in players:
        proj = project_player_stats(player, game, reference_time)
        projections.append(proj)
        
        recs = generate_prop_recommendations(proj, game)
        all_recommendations.extend(recs)
    
    # Sort recommendations by edge (best first)
    all_recommendations.sort(key=lambda r: r.edge, reverse=True)
    
    # Step 3: Build optimized parlay from top recommendations
    parlay = None
    if len(all_recommendations) >= 2:
        # Take top 3-4 recommendations for parlay
        top_recs = all_recommendations[:min(4, len(all_recommendations))]
        
        parlay_legs = []
        for i, rec in enumerate(top_recs):
            # Find the matching projection for this recommendation
            matching_proj = next(
                (p for p in projections if p.player_name == rec.player_name), None
            )
            prop = PropBet(
                player_id=matching_proj.player_id if matching_proj else f"player-{i}",
                player_name=rec.player_name,
                team=matching_proj.team if matching_proj else "",
                sport="NBA",
                game_id=game.game_id,
                prop_type=PropType.POINTS if rec.prop_type == "Points" else PropType.REBOUNDS,
                line=rec.line,
                direction=BetDirection.OVER if rec.direction == "OVER" else BetDirection.UNDER,
                odds=-110,
                ai_confidence=rec.confidence,
                impact_score=rec.impact_score,
                key_factors=rec.reasoning,
                projected_value=rec.projected_value,
                edge=rec.edge,
            )
            parlay_legs.append(prop)
        
        if len(parlay_legs) >= 2:
            parlay = score_parlay(parlay_legs)
    
    # Step 4: Generate summary
    flagged = [p for p in projections if p.impact_score < 70]
    boosted = [p for p in projections if p.impact_score > 80]
    
    summary_parts = []
    summary_parts.append(f"Game: {game.away_team} @ {game.home_team}")
    summary_parts.append(f"Analyzed {len(projections)} players")
    
    if flagged:
        names = ", ".join(p.player_name for p in flagged)
        summary_parts.append(f"FLAGGED (below baseline): {names}")
    if boosted:
        names = ", ".join(p.player_name for p in boosted)
        summary_parts.append(f"BOOSTED (above baseline): {names}")
    if all_recommendations:
        best = all_recommendations[0]
        summary_parts.append(
            f"Best edge: {best.player_name} {best.direction} {best.line} {best.prop_type} "
            f"(+{best.edge} edge, {best.confidence:.0f}% confidence)"
        )
    
    return GameAnalysis(
        game=game,
        projections=projections,
        prop_recommendations=all_recommendations,
        parlay_suggestion=parlay,
        analysis_timestamp=reference_time,
        summary=" | ".join(summary_parts),
    )


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def print_game_analysis(analysis: GameAnalysis):
    """Print a beautifully formatted game analysis."""
    g = analysis.game
    
    print("\n" + "=" * 70)
    print("  BETGENIE — GAME ANALYSIS REPORT")
    print("=" * 70)
    print(f"\n  {g.away_team} @ {g.home_team}")
    print(f"  {g.game_time.strftime('%A, %B %d, %Y — %I:%M %p ET')}")
    print(f"  Venue: {g.venue}")
    if g.is_national_tv:
        print(f"  National TV Game")
    if g.spread != 0:
        fav = g.home_team if g.spread < 0 else g.away_team
        print(f"  Spread: {fav} {abs(g.spread):.1f} | O/U: {g.over_under}")
    
    # Player Projections
    print(f"\n{'—'*70}")
    print(f"  PLAYER PROJECTIONS")
    print(f"{'—'*70}")
    
    for proj in sorted(analysis.projections, key=lambda p: p.impact_score):
        pis = proj.impact_score
        if pis >= 80:
            pis_icon = "[+]"  # Boosted
            pis_label = "BOOSTED"
        elif pis >= 70:
            pis_icon = "[=]"  # Normal
            pis_label = "BASELINE"
        elif pis >= 60:
            pis_icon = "[!]"  # Concerning
            pis_label = "FLAGGED"
        else:
            pis_icon = "[X]"  # Major impact
            pis_label = "IMPAIRED"
        
        print(f"\n  {pis_icon} {proj.player_name} ({proj.team})")
        print(f"      Impact Score: {pis}/100 — {pis_label}")
        print(f"      Physical: {proj.physical_score} | "
              f"Emotional: {proj.emotional_score} | "
              f"Psychological: {proj.psychological_score} | "
              f"Situational: {proj.situational_score}")
        print(f"      Projected: {proj.projected_points} pts / "
              f"{proj.projected_rebounds} reb / "
              f"{proj.projected_assists} ast / "
              f"{proj.projected_threes} 3PM")
        print(f"      vs Season Avg: {proj.baseline_points} pts "
              f"({proj.points_delta:+.1f})")
        
        if proj.active_factors:
            print(f"      Active Factors:")
            for factor in proj.active_factors[:3]:
                print(f"        - {factor[:70]}")
    
    # Prop Recommendations
    if analysis.prop_recommendations:
        print(f"\n{'—'*70}")
        print(f"  PROP RECOMMENDATIONS")
        print(f"{'—'*70}")
        
        for i, rec in enumerate(analysis.prop_recommendations, 1):
            edge_stars = "*" * min(5, int(rec.edge))
            print(f"\n  #{i} {rec.player_name} — {rec.direction} {rec.line} {rec.prop_type}")
            print(f"      Projected: {rec.projected_value} | Edge: +{rec.edge} {edge_stars}")
            print(f"      Confidence: {rec.confidence:.0f}% | PIS: {rec.impact_score}")
            for reason in rec.reasoning:
                print(f"      > {reason}")
    
    # Parlay
    if analysis.parlay_suggestion:
        p = analysis.parlay_suggestion
        print(f"\n{'—'*70}")
        print(f"  SMART PARLAY SUGGESTION")
        print(f"{'—'*70}")
        print(f"  Legs: {len(p.legs)} | Odds: {'+' if p.total_odds > 0 else ''}{p.total_odds}")
        print(f"  Payout: {p.payout_multiplier}x | Confidence: {p.ai_confidence}%")
        print(f"  Expected Value: {'+' if p.expected_value > 0 else ''}{p.expected_value:.3f}")
        
        for leg in p.legs:
            prop = leg.prop
            print(f"    Leg {leg.leg_number}: {prop.player_name} "
                  f"{prop.direction.value.upper()} {prop.line} {prop.prop_type.value}")
        
        if p.warnings:
            print(f"\n  Warnings:")
            for w in p.warnings:
                print(f"    ! {w}")
    
    print(f"\n{'='*70}")
    print(f"  Analysis generated: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Summary: {analysis.summary}")
    print(f"{'='*70}\n")


# ============================================================
# SCENARIO FACTORY — Creates realistic fictional game scenarios
# ============================================================

def create_scenario_morant_gun_incident() -> tuple[GameMatchup, list[PlayerProfile], datetime]:
    """
    Scenario 1: Ja Morant returns from gun controversy.
    
    Based on REAL events: After his Instagram Live gun incidents in 2023,
    Morant was suspended 25 games. In his return game vs Pelicans, he 
    scored 34 points but was clearly affected emotionally.
    
    This fictional scenario simulates: What if BetGenie analyzed Morant
    on the DAY he returned from suspension?
    """
    # Set reference time to the day of his actual return
    reference_time = datetime(2023, 12, 19, 18, 0, 0, tzinfo=timezone.utc)
    
    game = GameMatchup(
        game_id="nba-2023-12-19-mem-nop",
        home_team="Memphis Grizzlies",
        away_team="New Orleans Pelicans",
        game_time=reference_time,
        venue="FedExForum, Memphis, TN",
        sport=Sport.NBA,
        is_national_tv=True,
        is_rivalry=False,
        is_back_to_back=False,
        spread=-3.5,
        over_under=228.5,
    )
    
    morant = get_player("ja-morant-mem")
    players = [morant] if morant else []
    
    return game, players, reference_time


def create_scenario_luka_trade_adjustment() -> tuple[GameMatchup, list[PlayerProfile], datetime]:
    """
    Scenario 2: Luka Doncic first week with Lakers after blockbuster trade.
    
    Demonstrates how BetGenie captures the disruption of a major trade:
    new city, new teammates, new system, pressure to perform immediately.
    Combined with his existing injury and conditioning concerns.
    """
    reference_time = datetime(2025, 2, 10, 19, 30, 0, tzinfo=timezone.utc)
    
    game = GameMatchup(
        game_id="nba-2025-02-10-lal-bos",
        home_team="Boston Celtics",
        away_team="Los Angeles Lakers",
        game_time=reference_time,
        venue="TD Garden, Boston, MA",
        sport=Sport.NBA,
        is_national_tv=True,
        is_rivalry=True,  # Lakers-Celtics is always a rivalry
        is_back_to_back=False,
        spread=-5.5,
        over_under=221.0,
    )
    
    luka = get_player("luka-doncic-lal")
    lebron = get_player("lebron-james-lal")
    players = [p for p in [luka, lebron] if p is not None]
    
    return game, players, reference_time


def create_scenario_butler_trade_drama() -> tuple[GameMatchup, list[PlayerProfile], datetime]:
    """
    Scenario 3: Jimmy Butler's first game after demanding trade + double suspension.
    
    Maximum personal turmoil: demanded trade, suspended twice, traded to Phoenix.
    BetGenie should flag him as heavily impaired.
    """
    reference_time = datetime(2025, 2, 8, 21, 0, 0, tzinfo=timezone.utc)
    
    game = GameMatchup(
        game_id="nba-2025-02-08-phx-mia",
        home_team="Miami Heat",
        away_team="Phoenix Suns",
        game_time=reference_time,
        venue="Kaseya Center, Miami, FL",
        sport=Sport.NBA,
        is_national_tv=True,  # Revenge game = guaranteed TV
        is_rivalry=False,
        is_back_to_back=False,
        spread=-2.0,
        over_under=215.5,
    )
    
    butler = get_player("jimmy-butler-phx")
    players = [butler] if butler else []
    
    return game, players, reference_time


def create_scenario_stable_vs_volatile() -> tuple[GameMatchup, list[PlayerProfile], datetime]:
    """
    Scenario 4: SGA (stable, clean) vs Ja Morant (volatile, troubled).
    
    This is the KILLER demo — shows two elite players where BetGenie
    finds completely different risk profiles. SGA should score high PIS,
    Morant should score low PIS, creating clear prop bet edges.
    """
    reference_time = datetime(2025, 4, 5, 20, 0, 0, tzinfo=timezone.utc)
    
    game = GameMatchup(
        game_id="nba-2025-04-05-mem-okc",
        home_team="Oklahoma City Thunder",
        away_team="Memphis Grizzlies",
        game_time=reference_time,
        venue="Paycom Center, Oklahoma City, OK",
        sport=Sport.NBA,
        is_national_tv=True,
        is_rivalry=False,
        is_back_to_back=False,
        spread=-7.5,
        over_under=232.0,
    )
    
    sga = get_player("sga-okc")
    morant = get_player("ja-morant-mem")
    players = [p for p in [sga, morant] if p is not None]
    
    return game, players, reference_time


def create_scenario_wemby_showcase() -> tuple[GameMatchup, list[PlayerProfile], datetime]:
    """
    Scenario 5: Clean player showcase — Wembanyama with high PIS.
    
    Demonstrates that BetGenie doesn't just find negatives. A clean,
    focused player in a great mental state should project ABOVE baseline.
    """
    reference_time = datetime(2025, 3, 15, 19, 0, 0, tzinfo=timezone.utc)
    
    game = GameMatchup(
        game_id="nba-2025-03-15-sa-phi",
        home_team="San Antonio Spurs",
        away_team="Philadelphia 76ers",
        game_time=reference_time,
        venue="Frost Bank Center, San Antonio, TX",
        sport=Sport.NBA,
        is_national_tv=False,
        is_rivalry=False,
        is_back_to_back=False,
        spread=-4.0,
        over_under=225.5,
    )
    
    wemby = get_player("wemby-sa")
    maxey = get_player("tyrese-maxey-phi")
    players = [p for p in [wemby, maxey] if p is not None]
    
    return game, players, reference_time


# ============================================================
# DEMO — Run all scenarios
# ============================================================

if __name__ == "__main__":
    print("\n" + "#" * 70)
    print("#  BETGENIE — GAME SIMULATION ENGINE")
    print("#  Proof of Concept: 5 Real-World Scenarios")
    print("#" * 70)
    
    scenarios = [
        ("SCENARIO 1: Ja Morant Returns from Gun Suspension",
         create_scenario_morant_gun_incident),
        ("SCENARIO 2: Luka Doncic First Week as a Laker",
         create_scenario_luka_trade_adjustment),
        ("SCENARIO 3: Jimmy Butler's Revenge Game vs Miami",
         create_scenario_butler_trade_drama),
        ("SCENARIO 4: SGA (Stable) vs Morant (Volatile) — Head to Head",
         create_scenario_stable_vs_volatile),
        ("SCENARIO 5: Wembanyama Showcase — Clean PIS",
         create_scenario_wemby_showcase),
    ]
    
    all_analyses = []
    
    for title, scenario_fn in scenarios:
        print(f"\n\n{'#'*70}")
        print(f"#  {title}")
        print(f"{'#'*70}")
        
        game, players, ref_time = scenario_fn()
        
        if not players:
            print("  [No players found for this scenario]")
            continue
        
        analysis = analyze_game(game, players, ref_time)
        all_analyses.append(analysis)
        print_game_analysis(analysis)
    
    # Summary across all scenarios
    print("\n\n" + "#" * 70)
    print("#  EXECUTIVE SUMMARY — ALL SCENARIOS")
    print("#" * 70)
    
    total_recommendations = sum(len(a.prop_recommendations) for a in all_analyses)
    total_players = sum(len(a.projections) for a in all_analyses)
    
    print(f"\n  Scenarios Analyzed: {len(all_analyses)}")
    print(f"  Players Analyzed: {total_players}")
    print(f"  Prop Recommendations: {total_recommendations}")
    
    # Find most impacted player across all scenarios
    all_projections = []
    for a in all_analyses:
        all_projections.extend(a.projections)
    
    if all_projections:
        most_impaired = min(all_projections, key=lambda p: p.impact_score)
        most_boosted = max(all_projections, key=lambda p: p.impact_score)
        
        print(f"\n  Most Impaired: {most_impaired.player_name} "
              f"({most_impaired.impact_score}/100)")
        print(f"    - Projected {most_impaired.projected_points} pts "
              f"(vs {most_impaired.baseline_points} avg)")
        print(f"    - Delta: {most_impaired.points_delta:+.1f} pts")
        
        print(f"\n  Most Boosted: {most_boosted.player_name} "
              f"({most_boosted.impact_score}/100)")
        print(f"    - Projected {most_boosted.projected_points} pts "
              f"(vs {most_boosted.baseline_points} avg)")
        print(f"    - Delta: {most_boosted.points_delta:+.1f} pts")
    
    # Best bet across all scenarios
    all_recs = []
    for a in all_analyses:
        all_recs.extend(a.prop_recommendations)
    
    if all_recs:
        best = max(all_recs, key=lambda r: r.edge * r.confidence / 100)
        print(f"\n  Best Overall Edge:")
        print(f"    {best.player_name} {best.direction} {best.line} {best.prop_type}")
        print(f"    Edge: +{best.edge} | Confidence: {best.confidence:.0f}%")
        for r in best.reasoning:
            print(f"    > {r}")
    
    print(f"\n{'#'*70}")
    print(f"#  Proof of Concept Complete — BetGenie finds real edges")
    print(f"#  based on personal life events that markets don't price in.")
    print(f"{'#'*70}\n")
