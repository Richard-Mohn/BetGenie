"""
BetGenie — Basketball Data Ingestion Pipeline

This module handles:
1. Fetching real-time NBA game data from official NBA API
2. Pulling odds from The Odds API
3. Fetching player stats and injury reports
4. Normalizing data for the AI engine
"""

import os
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict
from enum import Enum
import json


class Sport(Enum):
    NBA = "basketball_nba"


@dataclass
class NBAGame:
    """NBA game data from official API."""
    game_id: str
    home_team: str
    away_team: str
    game_time: datetime
    venue: str
    status: str  # Scheduled, In Progress, Final
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    quarter: Optional[int] = None
    time_remaining: Optional[str] = None


@dataclass
class NBAPlayerStats:
    """Player stats from NBA API."""
    player_id: str
    player_name: str
    team: str
    season: str
    games_played: int
    minutes_per_game: float
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float
    field_goal_percentage: float
    three_point_percentage: float
    free_throw_percentage: float
    turnovers_per_game: float


@dataclass
class NBAInjury:
    """Injury report data."""
    player_id: str
    player_name: str
    team: str
    injury_type: str
    status: str  # Out, Questionable, Doubtful, Day-to-Day
    return_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class OddsLine:
    """Odds data from The Odds API."""
    sportsbook: str
    player_name: str
    team: str
    prop_type: str  # points, rebounds, assists, etc.
    line: float
    over_odds: int  # American odds
    under_odds: int
    last_updated: datetime


@dataclass
class BasketballDataBundle:
    """Complete data package for a game."""
    game: NBAGame
    player_stats: List[NBAPlayerStats]
    injuries: List[NBAInjury]
    odds: List[OddsLine]
    fetched_at: datetime


class NBAAPI:
    """Official NBA Stats API client."""
    
    BASE_URL = "https://stats.nba.com/stats"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nba.com/",
    }
    
    # Team ID to name mapping
    TEAM_NAMES = {
        1: "Atlanta Hawks",
        2: "Boston Celtics",
        3: "Brooklyn Nets",
        4: "Charlotte Hornets",
        5: "Chicago Bulls",
        6: "Cleveland Cavaliers",
        7: "Dallas Mavericks",
        8: "Denver Nuggets",
        9: "Detroit Pistons",
        10: "Golden State Warriors",
        11: "Houston Rockets",
        12: "Indiana Pacers",
        13: "Los Angeles Clippers",
        14: "Los Angeles Lakers",
        15: "Memphis Grizzlies",
        16: "Miami Heat",
        17: "Milwaukee Bucks",
        18: "Minnesota Timberwolves",
        19: "New Orleans Pelicans",
        20: "New York Knicks",
        21: "Oklahoma City Thunder",
        22: "Orlando Magic",
        23: "Philadelphia 76ers",
        24: "Phoenix Suns",
        25: "Portland Trail Blazers",
        26: "Sacramento Kings",
        27: "San Antonio Spurs",
        28: "Toronto Raptors",
        29: "Utah Jazz",
        30: "Washington Wizards",
    }
    
    @staticmethod
    def get_team_name(team_id: int) -> str:
        """Convert team ID to team name."""
        return NBAAPI.TEAM_NAMES.get(team_id, f"Team {team_id}")
    
    @staticmethod
    def get_todays_games() -> List[NBAGame]:
        """Fetch today's NBA games from official NBA API."""
        try:
            # Scoreboard endpoint
            url = f"{NBAAPI.BASE_URL}/scoreboardv2"
            params = {
                "GameDate": datetime.now().strftime("%m/%d/%Y"),
                "LeagueID": "00",
            }
            
            response = requests.get(url, headers=NBAAPI.HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            games = []
            game_header = data.get("resultSets", [{}])[0].get("rowSet", [])
            
            for game in game_header:
                # game[3] = away team ID, game[4] = home team ID
                away_team_id = game[3] if isinstance(game[3], int) else int(game[3]) if game[3] and str(game[3]).isdigit() else 0
                home_team_id = game[4] if isinstance(game[4], int) else int(game[4]) if game[4] and str(game[4]).isdigit() else 0
                
                games.append(NBAGame(
                    game_id=str(game[2]),
                    home_team=NBAAPI.get_team_name(home_team_id),
                    away_team=NBAAPI.get_team_name(away_team_id),
                    game_time=datetime.strptime(game[0].split("T")[0], "%Y-%m-%d").replace(tzinfo=timezone.utc),
                    venue=game[6] if isinstance(game[6], str) else "NBA Arena",
                    status=game[7] if isinstance(game[7], str) else "Scheduled",
                ))
            
            return games
            
        except Exception as e:
            print(f"Error fetching NBA games: {e}")
            raise Exception(f"Failed to fetch real NBA data: {e}")
    
    @staticmethod
    def get_player_stats(player_id: str, season: str = "2024-25") -> Optional[NBAPlayerStats]:
        """Fetch player season stats."""
        try:
            url = f"{NBAAPI.BASE_URL}/playerprofilev2"
            params = {
                "PlayerID": player_id,
                "LeagueID": "00",
                "Season": season,
            }
            
            response = requests.get(url, headers=NBAAPI.HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract season averages from resultSets
            season_stats = data.get("resultSets", [{}])[0].get("rowSet", [[]])
            if not season_stats:
                return None
            
            stats = season_stats[0]
            return NBAPlayerStats(
                player_id=player_id,
                player_name="",  # Would need separate call
                team="",
                season=season,
                games_played=stats[1] or 0,
                minutes_per_game=stats[6] or 0.0,
                points_per_game=stats[26] or 0.0,
                rebounds_per_game=stats[18] or 0.0,
                assists_per_game=stats[19] or 0.0,
                steals_per_game=stats[20] or 0.0,
                blocks_per_game=stats[21] or 0.0,
                field_goal_percentage=stats[9] or 0.0,
                three_point_percentage=stats[11] or 0.0,
                free_throw_percentage=stats[15] or 0.0,
                turnovers_per_game=stats[22] or 0.0,
            )
            
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return None
    
    @staticmethod
    def get_injury_report() -> List[NBAInjury]:
        """Fetch current NBA injury report."""
        try:
            # In production, this would scrape NBA.com/injuries or use a dedicated API
            # For now, return empty list - this is a placeholder
            return []
        except Exception as e:
            print(f"Error fetching injury report: {e}")
            return []


class TheOddsAPI:
    """The Odds API client for NBA odds."""
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        if not self.api_key:
            print("Warning: ODDS_API_KEY not set. Using mock data.")
    
    def get_nba_odds(self, regions: str = "us", markets: str = "player_points") -> List[OddsLine]:
        """Fetch NBA player prop odds."""
        if not self.api_key:
            return self._get_mock_odds()
        
        try:
            url = f"{TheOddsAPI.BASE_URL}/sports/basketball_nba/odds"
            params = {
                "api_key": self.api_key,
                "regions": regions,
                "markets": markets,
                "oddsFormat": "american",
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            odds = []
            for game in data:
                for bookmaker in game.get("bookmakers", []):
                    sportsbook = bookmaker.get("title", "Unknown")
                    for market in bookmaker.get("markets", []):
                        if market.get("key") == "player_points":
                            for outcome in market.get("outcomes", []):
                                odds.append(OddsLine(
                                    sportsbook=sportsbook,
                                    player_name=outcome.get("description", ""),
                                    team=outcome.get("name", ""),
                                    prop_type="points",
                                    line=outcome.get("point", 0.0),
                                    over_odds=outcome.get("price", -110),
                                    under_odds=-110,  # Would need separate outcome
                                    last_updated=datetime.now(timezone.utc),
                                ))
            
            return odds
            
        except Exception as e:
            print(f"Error fetching odds: {e}")
            return self._get_mock_odds()
    
    def _get_mock_odds(self) -> List[OddsLine]:
        """Generate mock odds for testing without API key."""
        return [
            OddsLine(
                sportsbook="DraftKings",
                player_name="LeBron James",
                team="Los Angeles Lakers",
                prop_type="points",
                line=23.5,
                over_odds=-110,
                under_odds=-110,
                last_updated=datetime.now(timezone.utc),
            ),
            OddsLine(
                sportsbook="FanDuel",
                player_name="LeBron James",
                team="Los Angeles Lakers",
                prop_type="points",
                line=24.5,
                over_odds=-115,
                under_odds=-105,
                last_updated=datetime.now(timezone.utc),
            ),
            OddsLine(
                sportsbook="DraftKings",
                player_name="Shai Gilgeous-Alexander",
                team="Oklahoma City Thunder",
                prop_type="points",
                line=31.5,
                over_odds=-110,
                under_odds=-110,
                last_updated=datetime.now(timezone.utc),
            ),
            OddsLine(
                sportsbook="FanDuel",
                player_name="Shai Gilgeous-Alexander",
                team="Oklahoma City Thunder",
                prop_type="points",
                line=32.0,
                over_odds=-105,
                under_odds=-115,
                last_updated=datetime.now(timezone.utc),
            ),
            OddsLine(
                sportsbook="DraftKings",
                player_name="Stephen Curry",
                team="Golden State Warriors",
                prop_type="points",
                line=26.5,
                over_odds=-110,
                under_odds=-110,
                last_updated=datetime.now(timezone.utc),
            ),
            OddsLine(
                sportsbook="FanDuel",
                player_name="Stephen Curry",
                team="Golden State Warriors",
                prop_type="points",
                line=27.0,
                over_odds=-115,
                under_odds=-105,
                last_updated=datetime.now(timezone.utc),
            ),
        ]


class BasketballDataPipeline:
    """Main pipeline coordinator for basketball data."""
    
    def __init__(self, odds_api_key: Optional[str] = None):
        self.nba_api = NBAAPI()
        self.odds_api = TheOddsAPI(odds_api_key)
    
    def fetch_game_data(self, game_date: Optional[datetime] = None) -> List[BasketballDataBundle]:
        """Fetch complete data for all games on a given date."""
        if game_date is None:
            game_date = datetime.now(timezone.utc)
        
        bundles = []
        
        # Get games
        games = self.nba_api.get_todays_games()
        
        for game in games:
            # Get injuries
            injuries = self.nba_api.get_injury_report()
            
            # Get odds
            odds = self.odds_api.get_nba_odds()
            
            # Filter odds for this game
            game_odds = [
                o for o in odds 
                if o.team in [game.home_team, game.away_team]
            ]
            
            bundles.append(BasketballDataBundle(
                game=game,
                player_stats=[],  # Would fetch for each player
                injuries=injuries,
                odds=game_odds,
                fetched_at=datetime.now(timezone.utc),
            ))
        
        return bundles
    
    def get_best_odds(self, player_name: str, prop_type: str, line: float) -> Optional[OddsLine]:
        """Find the best odds across all sportsbooks for a specific bet."""
        odds = self.odds_api.get_nba_odds()
        
        matching = [
            o for o in odds 
            if o.player_name == player_name 
            and o.prop_type == prop_type
            and abs(o.line - line) < 0.5
        ]
        
        if not matching:
            return None
        
        # Return the one with best over odds (most positive)
        return max(matching, key=lambda o: o.over_odds)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — BASKETBALL DATA PIPELINE")
    print("=" * 70)
    
    pipeline = BasketballDataPipeline()
    
    print("\nFetching today's NBA games...")
    bundles = pipeline.fetch_game_data()
    
    print(f"\nFound {len(bundles)} games today:")
    for bundle in bundles:
        g = bundle.game
        print(f"  - {g.away_team} @ {g.home_team} ({g.game_time.strftime('%Y-%m-%d %H:%M')})")
        print(f"    Venue: {g.venue}")
        print(f"    Status: {g.status}")
        
        if bundle.odds:
            print(f"    Available odds: {len(bundle.odds)} lines")
            for odd in bundle.odds[:3]:  # Show first 3
                print(f"      {odd.sportsbook}: {odd.player_name} {odd.prop_type} {odd.line} ({odd.over_odds})")
    
    print("\n" + "=" * 70)
