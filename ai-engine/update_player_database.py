"""
Player Database Update Script

This script fetches real-time player data from ESPN API and updates the player database.
It replaces the manual entry approach with automated data ingestion.

Usage:
    python update_player_database.py

Author: BetGenie AI Team
"""

from sports_data_ingestion import SportsDataAggregator, Sport, DataSource, Player
from star_player_database import NBAPlayer, Position, SeasonStats, NBA_PLAYERS
from typing import Dict, List
import sys


def convert_espn_to_nba_player(espn_player: Player) -> NBAPlayer:
    """
    Convert ESPN Player format to NBAPlayer format for the database.
    
    Args:
        espn_player: Player object from ESPN API
    
    Returns:
        NBAPlayer object compatible with star_player_database
    """
    # Map ESPN position to Position enum
    position_map = {
        "Point Guard": Position.PG,
        "Shooting Guard": Position.SG,
        "Small Forward": Position.SF,
        "Power Forward": Position.PF,
        "Center": Position.C,
        "Guard": Position.PG,  # Default to PG for generic Guard
        "Forward": Position.SF,  # Default to SF for generic Forward
    }
    
    # Normalize position string
    position_str = espn_player.position.lower() if espn_player.position else ""
    if "guard" in position_str:
        position = Position.PG
    elif "forward" in position_str:
        position = Position.SF
    elif "center" in position_str:
        position = Position.C
    else:
        position = Position.SF  # Default
    
    # Create player ID from full name (lowercase, underscores)
    player_id = espn_player.full_name.lower().replace(" ", "_").replace("-", "_")
    
    # Create season stats (ESPN doesn't provide current season stats in roster API)
    # We'll use placeholder data that can be updated later
    current_season = SeasonStats(
        season="2024-25",
        games_played=0,
        minutes_per_game=0.0,
        points_per_game=0.0,
        rebounds_per_game=0.0,
        assists_per_game=0.0,
        field_goal_percentage=0.0,
        three_point_percentage=0.0,
        free_throw_percentage=0.0
    )
    
    # Create career averages
    career_averages = SeasonStats(
        season="Career",
        games_played=0,
        minutes_per_game=0.0,
        points_per_game=0.0,
        rebounds_per_game=0.0,
        assists_per_game=0.0,
        field_goal_percentage=0.0,
        three_point_percentage=0.0,
        free_throw_percentage=0.0
    )
    
    # Determine player tier based on team and position (simplified logic)
    # In production, this could be based on actual performance metrics
    player_tier = "bench"  # Default
    is_all_star = False
    is_mvp = False
    
    # Detect star players by name (simplified approach)
    star_players = [
        "lebron james", "stephen curry", "kevin durant", "giannis antetokounmpo",
        "luka doncic", "joel embiid", "nikola jokic", "jayson tatum",
        "anthony davis", "kawhi leonard", "jimmy butler", "damian lillard",
        "trae young", "devin booker", "jaylen brown", "ja morant"
    ]
    
    if espn_player.full_name.lower() in star_players:
        player_tier = "star"
        is_all_star = True
    
    return NBAPlayer(
        player_id=player_id,
        full_name=espn_player.full_name,
        team=espn_player.team,
        position=position,
        age=espn_player.age,
        height=espn_player.height,
        salary=espn_player.salary or "Unknown",
        player_tier=player_tier,
        is_all_star=is_all_star,
        is_mvp=is_mvp,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=current_season,
        career_averages=career_averages,
        social_media_followers=espn_player.social_media_followers,
        endorsement_deals=espn_player.endorsement_deals,
        personal_events=[]
    )


def update_player_database():
    """Fetch players from ESPN and update the database"""
    print("=== Updating Player Database from ESPN API ===\n")
    
    # Initialize aggregator
    aggregator = SportsDataAggregator()
    
    # Fetch all NBA players from ESPN
    print("Fetching NBA players from ESPN...")
    espn_players = aggregator.fetch_all_players(Sport.NBA, DataSource.ESPN)
    print(f"Fetched {len(espn_players)} players from ESPN\n")
    
    # Convert to NBAPlayer format
    print("Converting to database format...")
    nba_players = {}
    converted_count = 0
    skipped_count = 0
    
    for espn_player in espn_players:
        try:
            nba_player = convert_espn_to_nba_player(espn_player)
            nba_players[nba_player.player_id] = nba_player
            converted_count += 1
            
            if converted_count % 50 == 0:
                print(f"  Converted {converted_count}/{len(espn_players)} players...")
        except Exception as e:
            print(f"  Error converting {espn_player.full_name}: {e}")
            skipped_count += 1
    
    print(f"\nConverted {converted_count} players, skipped {skipped_count}")
    
    # Update the NBA_PLAYERS dictionary
    print(f"\nUpdating database...")
    NBA_PLAYERS.update(nba_players)
    
    print(f"Database now contains {len(NBA_PLAYERS)} players")
    
    # Save to file (this would require modifying star_player_database.py to support saving)
    # For now, we'll just print the update
    print("\n=== Database Update Complete ===")
    print(f"Total players in database: {len(NBA_PLAYERS)}")
    print("\nTo persist these changes, the star_player_database.py file needs to be updated")
    print("with the new player entries.")
    
    # Export to JSON for manual review
    import json
    export_data = []
    for player_id, player in nba_players.items():
        player_dict = {
            "player_id": player.player_id,
            "full_name": player.full_name,
            "team": player.team,
            "position": player.position.value,
            "age": player.age,
            "height": player.height,
            "salary": player.salary
        }
        export_data.append(player_dict)
    
    with open("espn_players_export.json", "w") as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\nExported {len(export_data)} players to espn_players_export.json for review")


if __name__ == "__main__":
    update_player_database()
