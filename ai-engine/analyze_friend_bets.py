"""
Quick analysis of friend's spread/total bets using BetGenie's game simulator.
"""

from datetime import datetime, timezone
from game_simulator import GameMatchup, Sport, project_player_stats, analyze_game
from player_database import get_all_players, Sport as PD_Sport

def analyze_spread_bet(game: GameMatchup, pick_team: str, spread_line: float):
    """
    Analyze a spread bet using team composition and player impact scores.
    """
    print(f"\n{'='*70}")
    print(f"ANALYZING: {pick_team} {spread_line:+.1f} vs {game.away_team if pick_team == game.home_team else game.home_team}")
    print(f"{'='*70}")
    
    # Get all players for both teams
    all_players = get_all_players()
    home_players = [p for p in all_players if p.team == game.home_team and p.sport == PD_Sport.NBA]
    away_players = [p for p in all_players if p.team == game.away_team and p.sport == PD_Sport.NBA]
    
    # Project stats for all players
    home_projections = []
    away_projections = []
    
    for player in home_players:
        try:
            proj = project_player_stats(player, game)
            home_projections.append(proj)
        except:
            pass
    
    for player in away_players:
        try:
            proj = project_player_stats(player, game)
            away_projections.append(proj)
        except:
            pass
    
    # Calculate team strength based on player projections
    home_strength = sum(p.impact_score for p in home_projections) / len(home_projections) if home_projections else 50
    away_strength = sum(p.impact_score for p in away_projections) / len(away_projections) if away_projections else 50
    
    print(f"\nTeam Impact Scores:")
    print(f"  {game.home_team}: {home_strength:.1f}/100")
    print(f"  {game.away_team}: {away_strength:.1f}/100")
    
    # Determine which team is favored by our analysis
    strength_diff = home_strength - away_strength
    our_spread = strength_diff / 5  # Convert impact score diff to points
    
    print(f"\nOur Analysis Spread: {game.home_team} {our_spread:+.1f}")
    print(f"Market Spread: {game.home_team} {game.spread:+.1f}")
    
    # Analyze the pick
    if pick_team == game.home_team:
        pick_spread = spread_line
    else:
        pick_spread = -spread_line
    
    edge = our_spread - pick_spread
    
    print(f"\nPick Analysis:")
    print(f"  Your Pick: {pick_team} {spread_line:+.1f}")
    print(f"  Our Edge: {edge:+.1f} points")
    
    if edge > 3:
        recommendation = "STRONG BET - Good edge"
        confidence = 75
    elif edge > 1:
        recommendation = "MODERATE BET - Small edge"
        confidence = 60
    elif edge > -1:
        recommendation = "NEUTRAL - No clear edge"
        confidence = 50
    elif edge > -3:
        recommendation = "WEAK BET - Slight disadvantage"
        confidence = 40
    else:
        recommendation = "AVOID - Significant disadvantage"
        confidence = 25
    
    print(f"  Recommendation: {recommendation}")
    print(f"  Win Probability: {confidence}%")
    
    return confidence, recommendation

def analyze_total_bet(game: GameMatchup, total_line: float, direction: str):
    """
    Analyze an over/under total bet.
    """
    print(f"\n{'='*70}")
    print(f"ANALYZING: {direction.upper()} {total_line} - {game.home_team} vs {game.away_team}")
    print(f"{'='*70}")
    
    # Get all players for both teams
    all_players = get_all_players()
    home_players = [p for p in all_players if p.team == game.home_team and p.sport == PD_Sport.NBA]
    away_players = [p for p in all_players if p.team == game.away_team and p.sport == PD_Sport.NBA]
    
    # Project stats for all players
    home_projections = []
    away_projections = []
    
    for player in home_players:
        try:
            proj = project_player_stats(player, game)
            home_projections.append(proj)
        except:
            pass
    
    for player in away_players:
        try:
            proj = project_player_stats(player, game)
            away_projections.append(proj)
        except:
            pass
    
    # Calculate projected team points based on player projections
    home_projected = sum(p.projected_points for p in home_projections)
    away_projected = sum(p.projected_points for p in away_projections)
    total_projected = home_projected + away_projected
    
    print(f"\nProjected Points:")
    print(f"  {game.home_team}: {home_projected:.1f}")
    print(f"  {game.away_team}: {away_projected:.1f}")
    print(f"  Total: {total_projected:.1f}")
    
    print(f"\nMarket Total: {total_line}")
    
    # Analyze the pick
    if direction == "over":
        edge = total_projected - total_line
    else:
        edge = total_line - total_projected
    
    print(f"\nPick Analysis:")
    print(f"  Your Pick: {direction.upper()} {total_line}")
    print(f"  Our Edge: {edge:+.1f} points")
    
    if edge > 5:
        recommendation = "STRONG BET - Good edge"
        confidence = 75
    elif edge > 2:
        recommendation = "MODERATE BET - Small edge"
        confidence = 60
    elif edge > -2:
        recommendation = "NEUTRAL - No clear edge"
        confidence = 50
    elif edge > -5:
        recommendation = "WEAK BET - Slight disadvantage"
        confidence = 40
    else:
        recommendation = "AVOID - Significant disadvantage"
        confidence = 25
    
    print(f"  Recommendation: {recommendation}")
    print(f"  Win Probability: {confidence}%")
    
    return confidence, recommendation

def main():
    print("\n" + "="*70)
    print("  BETGENIE — FRIEND'S BETS ANALYSIS")
    print("="*70)
    print(f"\nAnalysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("⚠️  Games have already started - this is for informational purposes only")
    
    # Friend's bets from screenshot
    bets = [
        {
            "game": GameMatchup(
                game_id="nba-2025-04-28-dal-gsw",
                home_team="Golden State Warriors",
                away_team="Dallas Mavericks",
                game_time=datetime.now(timezone.utc),
                venue="Chase Center",
                sport=Sport.NBA,
                spread=-3.5,  # Warriors favored by 3.5
                over_under=229.5
            ),
            "bets": [
                {"type": "spread", "team": "Dallas Mavericks", "line": +3.5},
                {"type": "total", "direction": "over", "line": 229.5}
            ]
        },
        {
            "game": GameMatchup(
                game_id="nba-2025-04-28-lal-phx",
                home_team="Phoenix Suns",
                away_team="Los Angeles Lakers",
                game_time=datetime.now(timezone.utc),
                venue="Footprint Center",
                sport=Sport.NBA,
                spread=-6.5,  # Suns favored by 6.5
                over_under=234.5
            ),
            "bets": [
                {"type": "spread", "team": "Los Angeles Lakers", "line": +6.5},
                {"type": "total", "direction": "over", "line": 234.5}
            ]
        },
        {
            "game": GameMatchup(
                game_id="nba-2025-04-28-orl-nyk",
                home_team="New York Knicks",
                away_team="Orlando Magic",
                game_time=datetime.now(timezone.utc),
                venue="Madison Square Garden",
                sport=Sport.NBA,
                spread=-11.5,  # Knicks favored by 11.5
                over_under=220.0
            ),
            "bets": [
                {"type": "spread", "team": "Orlando Magic", "line": +11.5}
            ]
        }
    ]
    
    all_confidences = []
    
    for matchup in bets:
        game = matchup["game"]
        for bet in matchup["bets"]:
            if bet["type"] == "spread":
                conf, rec = analyze_spread_bet(game, bet["team"], bet["line"])
                all_confidences.append(conf)
            elif bet["type"] == "total":
                conf, rec = analyze_total_bet(game, bet["line"], bet["direction"])
                all_confidences.append(conf)
    
    # Summary
    print(f"\n{'='*70}")
    print("  SUMMARY")
    print(f"{'='*70}")
    avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0
    print(f"\nAverage Win Probability: {avg_confidence:.1f}%")
    
    if avg_confidence > 60:
        print("Overall Assessment: GOOD - Above average edge")
    elif avg_confidence > 50:
        print("Overall Assessment: NEUTRAL - Mixed bets")
    else:
        print("Overall Assessment: POOR - Below average edge")
    
    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
