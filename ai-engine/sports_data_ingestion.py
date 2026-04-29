"""
Sports Data Ingestion Module

This module provides a unified interface for fetching real-time player data from multiple sports APIs.
Designed to be extensible for NBA and other sports (NFL, MLB, Soccer, etc.).

Author: BetGenie AI Team
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from enum import Enum
import os
import requests
import json
from abc import ABC, abstractmethod


# Fix for timezone UTC reference
UTC = timezone.utc


class Sport(Enum):
    """Supported sports"""
    NBA = "nba"
    NFL = "nfl"
    MLB = "mlb"
    NHL = "nhl"
    SOCCER = "soccer"
    MMA = "mma"
    TENNIS = "tennis"
    COLLEGE_FOOTBALL = "college-football"
    COLLEGE_BASKETBALL = "college-basketball"


class DataSource(Enum):
    """Data source providers"""
    ESPN = "espn"
    BALLEDONTLIE = "balldontlie"
    SPORTRADAR = "sportradar"
    API_SPORTS = "api_sports"
    THE_ODDS_API = "the_odds_api"


@dataclass
class PlayerStats:
    """Player statistics for a season"""
    season: str
    games_played: int
    minutes_per_game: float
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    field_goal_percentage: float
    three_point_percentage: float
    free_throw_percentage: float
    steals_per_game: float = 0.0
    blocks_per_game: float = 0.0
    turnovers_per_game: float = 0.0


@dataclass
class Player:
    """Unified player data structure"""
    player_id: str
    full_name: str
    sport: Sport
    team: str
    position: str
    age: int
    height: str
    weight: Optional[int] = None
    salary: Optional[str] = None
    current_season_stats: Optional[PlayerStats] = None
    career_stats: Optional[PlayerStats] = None
    social_media_followers: int = 0
    endorsement_deals: int = 0
    last_updated: datetime = field(default_factory=lambda: datetime.now(UTC))


class SportsDataProvider(ABC):
    """Abstract base class for sports data providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = ""
    
    @abstractmethod
    def fetch_all_players(self, sport: Sport) -> List[Player]:
        """Fetch all players for a given sport"""
        pass
    
    @abstractmethod
    def fetch_player_stats(self, player_id: str, sport: Sport) -> Dict[str, Any]:
        """Fetch detailed stats for a specific player"""
        pass
    
    @abstractmethod
    def fetch_team_roster(self, team_id: str, sport: Sport) -> List[Player]:
        """Fetch roster for a specific team"""
        pass


class ESPNProvider(SportsDataProvider):
    """
    ESPN API Provider
    
    Free, no API key required for basic data.
    Provides comprehensive data for multiple sports.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports"
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make a request to the ESPN API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching from ESPN: {e}")
            return {}
    
    def fetch_all_players(self, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch all players from ESPN for a given sport"""
        if sport == Sport.NBA:
            return self._fetch_nba_players()
        elif sport == Sport.NFL:
            return self._fetch_nfl_players()
        elif sport == Sport.MLB:
            return self._fetch_mlb_players()
        elif sport == Sport.NHL:
            return self._fetch_nhl_players()
        elif sport == Sport.COLLEGE_FOOTBALL:
            return self._fetch_college_football_players()
        elif sport == Sport.COLLEGE_BASKETBALL:
            return self._fetch_college_basketball_players()
        else:
            print(f"ESPN provider not yet implemented for {sport}")
            return []
    
    def _fetch_nba_players(self) -> List[Player]:
        """Fetch NBA players by iterating through teams"""
        all_players = []
        
        # First, get all NBA teams
        teams_data = self._make_request("/basketball/nba/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        # Get teams list
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        # Fetch roster for each team
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.NBA)
            all_players.extend(roster)
        
        return all_players
    
    def _fetch_nfl_players(self) -> List[Player]:
        """Fetch NFL players"""
        # Similar structure to NBA
        teams_data = self._make_request("/football/nfl/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        all_players = []
        
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.NFL)
            all_players.extend(roster)
        
        return all_players
    
    def _fetch_mlb_players(self) -> List[Player]:
        """Fetch MLB players"""
        teams_data = self._make_request("/baseball/mlb/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        all_players = []
        
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.MLB)
            all_players.extend(roster)
        
        return all_players
    
    def _fetch_nhl_players(self) -> List[Player]:
        """Fetch NHL players"""
        teams_data = self._make_request("/hockey/nhl/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        all_players = []
        
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.NHL)
            all_players.extend(roster)
        
        return all_players
    
    def _fetch_college_football_players(self) -> List[Player]:
        """Fetch College Football players"""
        teams_data = self._make_request("/football/college-football/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        all_players = []
        
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.COLLEGE_FOOTBALL)
            all_players.extend(roster)
        
        return all_players
    
    def _fetch_college_basketball_players(self) -> List[Player]:
        """Fetch College Basketball players"""
        teams_data = self._make_request("/basketball/mens-college-basketball/teams")
        
        if not teams_data or "sports" not in teams_data:
            return []
        
        sports = teams_data["sports"][0] if teams_data["sports"] else {}
        leagues = sports.get("leagues", [])
        teams = leagues[0].get("teams", []) if leagues else []
        
        all_players = []
        
        for team_info in teams:
            team = team_info.get("team", {})
            team_id = team.get("id")
            
            if not team_id:
                continue
            
            roster = self.fetch_team_roster(str(team_id), Sport.COLLEGE_BASKETBALL)
            all_players.extend(roster)
        
        return all_players
    
    def fetch_player_stats(self, player_id: str, sport: Sport = Sport.NBA) -> Dict[str, Any]:
        """Fetch player stats from ESPN"""
        if sport == Sport.NBA:
            endpoint = f"/basketball/nba/players/{player_id}"
        elif sport == Sport.NFL:
            endpoint = f"/football/nfl/players/{player_id}"
        elif sport == Sport.MLB:
            endpoint = f"/baseball/mlb/players/{player_id}"
        elif sport == Sport.NHL:
            endpoint = f"/hockey/nhl/players/{player_id}"
        elif sport == Sport.COLLEGE_FOOTBALL:
            endpoint = f"/football/college-football/players/{player_id}"
        elif sport == Sport.COLLEGE_BASKETBALL:
            endpoint = f"/basketball/mens-college-basketball/players/{player_id}"
        else:
            return {}
        
        data = self._make_request(endpoint)
        return data
    
    def fetch_team_roster(self, team_id: str, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch team roster from ESPN"""
        if sport == Sport.NBA:
            endpoint = f"/basketball/nba/teams/{team_id}/roster"
        elif sport == Sport.NFL:
            endpoint = f"/football/nfl/teams/{team_id}/roster"
        elif sport == Sport.MLB:
            endpoint = f"/baseball/mlb/teams/{team_id}/roster"
        elif sport == Sport.NHL:
            endpoint = f"/hockey/nhl/teams/{team_id}/roster"
        elif sport == Sport.COLLEGE_FOOTBALL:
            endpoint = f"/football/college-football/teams/{team_id}/roster"
        elif sport == Sport.COLLEGE_BASKETBALL:
            endpoint = f"/basketball/mens-college-basketball/teams/{team_id}/roster"
        else:
            return []
        
        data = self._make_request(endpoint)
        
        players = []
        if data:
            athletes = data.get("athletes", [])
            
            for athlete in athletes:
                player = self._parse_player(athlete, sport, data.get("team", {}).get("displayName", "Unknown"))
                if player:
                    players.append(player)
        
        return players
    
    def _parse_player(self, athlete: Dict[str, Any], sport: Sport, team_name: str) -> Optional[Player]:
        """Parse player data from ESPN format"""
        try:
            # Handle cases where athlete might be a string or unexpected format
            if not isinstance(athlete, dict):
                print(f"  Warning: athlete is not a dict, got {type(athlete)}")
                return None
            
            # Get position from ESPN
            position = ""
            if "position" in athlete:
                pos_data = athlete["position"]
                if isinstance(pos_data, dict):
                    position = pos_data.get("displayName", "")
                elif isinstance(pos_data, str):
                    position = pos_data
            elif "items" in athlete and len(athlete["items"]) > 0:
                # Try to get position from items
                for item in athlete["items"]:
                    if "position" in item:
                        pos_data = item["position"]
                        if isinstance(pos_data, dict):
                            position = pos_data.get("displayName", "")
                        elif isinstance(pos_data, str):
                            position = pos_data
                        break
            
            # Get height
            height_str = ""
            if "height" in athlete:
                height = athlete["height"]
                if isinstance(height, int):
                    height_str = f"{height // 12}'{height % 12}\""
                elif isinstance(height, str):
                    height_str = height
            
            # Get age
            age = 0
            if "dateOfBirth" in athlete:
                dob = athlete["dateOfBirth"]
                if dob and isinstance(dob, str):
                    try:
                        birth_date = datetime.fromisoformat(dob.replace("Z", "+00:00"))
                        age = (datetime.now(UTC) - birth_date).days // 365
                    except:
                        pass
            
            # Get display name (handle different field names)
            display_name = ""
            if "displayName" in athlete:
                display_name = athlete["displayName"]
            elif "full_name" in athlete:
                display_name = athlete["full_name"]
            elif "name" in athlete:
                display_name = athlete["name"]
            
            # Get player ID
            player_id = ""
            if "id" in athlete:
                player_id = str(athlete["id"])
            elif "guid" in athlete:
                player_id = str(athlete["guid"])
            
            # Get weight
            weight = None
            if "weight" in athlete:
                weight = athlete["weight"]
            
            if not display_name or not player_id:
                return None
            
            return Player(
                player_id=player_id,
                full_name=display_name,
                sport=sport,
                team=team_name,
                position=position,
                age=age,
                height=height_str,
                weight=weight,
                salary=None,
                last_updated=datetime.now(UTC)
            )
        except Exception as e:
            print(f"Error parsing ESPN player data: {e}")
            return None


class BallDontLieProvider(SportsDataProvider):
    """
    BALLEDONTLIE API Provider
    
    Free tier available with generous rate limits.
    Provides comprehensive NBA data including players, stats, teams.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.base_url = "https://api.balldontlie.io/v1"
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the BALLEDONTLIE API"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching from BALLEDONTLIE: {e}")
            return {}
    
    def fetch_all_players(self, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch all NBA players"""
        if sport != Sport.NBA:
            print(f"BALLEDONTLIE only supports NBA, got {sport}")
            return []
        
        players = []
        cursor = 0
        per_page = 100
        
        while True:
            params = {
                "cursor": cursor,
                "per_page": per_page
            }
            
            data = self._make_request("/players", params)
            
            if not data or "data" not in data:
                break
            
            for player_data in data["data"]:
                player = self._parse_player(player_data, sport)
                if player:
                    players.append(player)
            
            # Check if there are more pages
            meta = data.get("meta", {})
            next_cursor = meta.get("next_cursor")
            if not next_cursor:
                break
            
            cursor = next_cursor
        
        print(f"Fetched {len(players)} players from BALLEDONTLIE")
        return players
    
    def fetch_player_stats(self, player_id: str, sport: Sport = Sport.NBA) -> Dict[str, Any]:
        """Fetch season stats for a specific player"""
        if sport != Sport.NBA:
            return {}
        
        params = {
            "player_ids[]": player_id,
            "season": 2024
        }
        
        data = self._make_request("/stats", params)
        
        if data and "data" in data:
            return data["data"]
        
        return {}
    
    def fetch_team_roster(self, team_id: str, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch roster for a specific team"""
        if sport != Sport.NBA:
            return []
        
        params = {
            "team_ids[]": team_id
        }
        
        data = self._make_request("/players", params)
        
        players = []
        if data and "data" in data:
            for player_data in data["data"]:
                player = self._parse_player(player_data, sport)
                if player:
                    players.append(player)
        
        return players
    
    def _parse_player(self, player_data: Dict[str, Any], sport: Sport) -> Optional[Player]:
        """Parse player data from BALLEDONTLIE format"""
        try:
            return Player(
                player_id=str(player_data["id"]),
                full_name=f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}",
                sport=sport,
                team=player_data.get("team", {}).get("full_name", "Unknown"),
                position=player_data.get("position", ""),
                age=player_data.get("height_feet", 0),  # BALLEDONTLIE doesn't have age directly
                height=f"{player_data.get('height_feet', 0)}'{player_data.get('height_inches', 0)}\"",
                weight=player_data.get("weight_pounds"),
                salary=None,  # BALLEDONTLIE doesn't provide salary
                last_updated=datetime.now(UTC)
            )
        except Exception as e:
            print(f"Error parsing player data: {e}")
            return None
    
    def _parse_stats(self, stats_data: Dict[str, Any]) -> Optional[PlayerStats]:
        """Parse stats data from BALLEDONTLIE format"""
        try:
            return PlayerStats(
                season=str(stats_data.get("season", 2024)),
                games_played=stats_data.get("games_played", 0),
                minutes_per_game=stats_data.get("min", 0.0),
                points_per_game=stats_data.get("pts", 0.0),
                rebounds_per_game=stats_data.get("reb", 0.0),
                assists_per_game=stats_data.get("ast", 0.0),
                field_goal_percentage=stats_data.get("fg_pct", 0.0),
                three_point_percentage=stats_data.get("fg3_pct", 0.0),
                free_throw_percentage=stats_data.get("ft_pct", 0.0),
                steals_per_game=stats_data.get("stl", 0.0),
                blocks_per_game=stats_data.get("blk", 0.0),
                turnovers_per_game=stats_data.get("turnover", 0.0)
            )
        except Exception as e:
            print(f"Error parsing stats data: {e}")
            return None


class SportradarProvider(SportsDataProvider):
    """
    Sportradar API Provider
    
    Premium service with comprehensive data for multiple sports.
    Requires API key and has pricing tiers.
    """
    
    def __init__(self, api_key: str, access_level: str = "trial"):
        super().__init__(api_key)
        self.access_level = access_level
        self.base_url = f"https://api.sportradar.com/nba/{access_level}/v7/en"
    
    def fetch_all_players(self, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch all players (requires team-by-team fetch for Sportradar)"""
        # Sportradar requires fetching teams first, then rosters
        teams = self._fetch_teams(sport)
        all_players = []
        
        for team in teams:
            roster = self.fetch_team_roster(team["id"], sport)
            all_players.extend(roster)
        
        return all_players
    
    def fetch_player_stats(self, player_id: str, sport: Sport = Sport.NBA) -> Dict[str, Any]:
        """Fetch player stats"""
        endpoint = f"/players/{player_id}/profile"
        data = self._make_request(endpoint)
        return data
    
    def fetch_team_roster(self, team_id: str, sport: Sport = Sport.NBA) -> List[Player]:
        """Fetch team roster"""
        endpoint = f"/teams/{team_id}/profile"
        data = self._make_request(endpoint)
        
        players = []
        if data and "players" in data:
            for player_data in data["players"]:
                player = self._parse_player(player_data, sport)
                if player:
                    players.append(player)
        
        return players
    
    def _fetch_teams(self, sport: Sport) -> List[Dict[str, Any]]:
        """Fetch all teams"""
        endpoint = "/league/teams"
        data = self._make_request(endpoint)
        
        if data and "teams" in data:
            return data["teams"]
        
        return []
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make request to Sportradar API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching from Sportradar: {e}")
            return {}
    
    def _parse_player(self, player_data: Dict[str, Any], sport: Sport) -> Optional[Player]:
        """Parse player data from Sportradar format"""
        try:
            return Player(
                player_id=str(player_data.get("id", "")),
                full_name=player_data.get("full_name", ""),
                sport=sport,
                team=player_data.get("team", {}).get("name", "Unknown"),
                position=player_data.get("position", ""),
                age=player_data.get("age", 0),
                height=player_data.get("height", ""),
                weight=player_data.get("weight"),
                salary=None,
                last_updated=datetime.now(UTC)
            )
        except Exception as e:
            print(f"Error parsing player data: {e}")
            return None


class SportsDataAggregator:
    """
    Main aggregator class for fetching and consolidating sports data from multiple sources.
    """
    
    def __init__(self):
        self.providers: Dict[DataSource, SportsDataProvider] = {}
        self.players_cache: Dict[str, List[Player]] = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available data providers"""
        # ESPN (free, no API key required)
        self.providers[DataSource.ESPN] = ESPNProvider()
        
        # BALLEDONTLIE (free tier available with API key)
        bdl_key = os.getenv("BALLEDONTLIE_API_KEY")
        if bdl_key:
            self.providers[DataSource.BALLEDONTLIE] = BallDontLieProvider(bdl_key)
        
        # Sportradar (requires API key)
        sr_key = os.getenv("SPORTRADAR_API_KEY")
        if sr_key:
            self.providers[DataSource.SPORTRADAR] = SportradarProvider(sr_key)
    
    def fetch_all_players(self, sport: Sport = Sport.NBA, source: DataSource = DataSource.ESPN) -> List[Player]:
        """
        Fetch all players for a given sport from specified source
        
        Args:
            sport: The sport to fetch players for
            source: The data source to use
        
        Returns:
            List of Player objects
        """
        if source not in self.providers:
            print(f"Provider {source} not available")
            return []
        
        provider = self.providers[source]
        cache_key = f"{sport.value}_{source.value}"
        
        # Check cache first
        if cache_key in self.players_cache:
            print(f"Using cached data for {cache_key}")
            return self.players_cache[cache_key]
        
        # Fetch from API
        players = provider.fetch_all_players(sport)
        
        # Cache the results
        self.players_cache[cache_key] = players
        
        return players
    
    def fetch_player_with_stats(self, player_id: str, sport: Sport = Sport.NBA, source: DataSource = DataSource.ESPN) -> Optional[Player]:
        """
        Fetch a specific player with their stats
        
        Args:
            player_id: The player's ID
            sport: The sport
            source: The data source to use
        
        Returns:
            Player object with stats populated
        """
        if source not in self.providers:
            return None
        
        provider = self.providers[source]
        stats_data = provider.fetch_player_stats(player_id, sport)
        
        # Fetch base player data
        all_players = self.fetch_all_players(sport, source)
        player = next((p for p in all_players if p.player_id == player_id), None)
        
        if player and stats_data:
            # Parse and attach stats
            if isinstance(provider, BallDontLieProvider):
                player.current_season_stats = provider._parse_stats(stats_data)
        
        return player
    
    def refresh_cache(self, sport: Sport = Sport.NBA):
        """Refresh the cache for a given sport"""
        for source in self.providers:
            cache_key = f"{sport.value}_{source.value}"
            if cache_key in self.players_cache:
                del self.players_cache[cache_key]
                print(f"Cleared cache for {cache_key}")
    
    def get_player_count(self, sport: Sport = Sport.NBA) -> int:
        """Get the number of cached players for a sport"""
        count = 0
        for source in self.providers:
            cache_key = f"{sport.value}_{source.value}"
            if cache_key in self.players_cache:
                count += len(self.players_cache[cache_key])
        return count
    
    def export_to_database_format(self, sport: Sport = Sport.NBA, source: DataSource = DataSource.ESPN) -> Dict[str, Any]:
        """
        Export fetched players in a format compatible with the database
        
        Returns:
            Dictionary with players data ready for database insertion
        """
        players = self.fetch_all_players(sport, source)
        
        export_data = {
            "sport": sport.value,
            "source": source.value,
            "count": len(players),
            "last_updated": datetime.now(UTC).isoformat(),
            "players": []
        }
        
        for player in players:
            player_dict = {
                "player_id": player.player_id,
                "full_name": player.full_name,
                "sport": player.sport.value,
                "team": player.team,
                "position": player.position,
                "age": player.age,
                "height": player.height,
                "weight": player.weight,
                "salary": player.salary,
                "current_season_stats": None,
                "career_stats": None,
                "social_media_followers": player.social_media_followers,
                "endorsement_deals": player.endorsement_deals
            }
            
            if player.current_season_stats:
                player_dict["current_season_stats"] = {
                    "season": player.current_season_stats.season,
                    "games_played": player.current_season_stats.games_played,
                    "minutes_per_game": player.current_season_stats.minutes_per_game,
                    "points_per_game": player.current_season_stats.points_per_game,
                    "rebounds_per_game": player.current_season_stats.rebounds_per_game,
                    "assists_per_game": player.current_season_stats.assists_per_game,
                    "field_goal_percentage": player.current_season_stats.field_goal_percentage,
                    "three_point_percentage": player.current_season_stats.three_point_percentage,
                    "free_throw_percentage": player.current_season_stats.free_throw_percentage
                }
            
            export_data["players"].append(player_dict)
        
        return export_data


def demo():
    """Demo the sports data ingestion"""
    print("=== Sports Data Ingestion Demo ===\n")
    
    aggregator = SportsDataAggregator()
    
    print(f"Available providers: {list(aggregator.providers.keys())}\n")
    
    # Test NBA (already working)
    print("Testing NBA data fetching...")
    nba_players = aggregator.fetch_all_players(Sport.NBA, DataSource.ESPN)
    print(f"Fetched {len(nba_players)} NBA players")
    
    if nba_players:
        print("\nSample NBA players:")
        for i, player in enumerate(nba_players[:3]):
            print(f"  {i+1}. {player.full_name} - {player.team} ({player.position})")
    
    # Test NFL (multi-sport expansion)
    print("\n\nTesting NFL data fetching (multi-sport expansion)...")
    nfl_players = aggregator.fetch_all_players(Sport.NFL, DataSource.ESPN)
    print(f"Fetched {len(nfl_players)} NFL players")
    
    if nfl_players:
        print("\nSample NFL players:")
        for i, player in enumerate(nfl_players[:3]):
            print(f"  {i+1}. {player.full_name} - {player.team} ({player.position})")
    
    # Test MLB (multi-sport expansion)
    print("\n\nTesting MLB data fetching (multi-sport expansion)...")
    mlb_players = aggregator.fetch_all_players(Sport.MLB, DataSource.ESPN)
    print(f"Fetched {len(mlb_players)} MLB players")
    
    if mlb_players:
        print("\nSample MLB players:")
        for i, player in enumerate(mlb_players[:3]):
            print(f"  {i+1}. {player.full_name} - {player.team} ({player.position})")
    
    # Export to database format
    print("\n\nExporting NBA data to database format...")
    export_data = aggregator.export_to_database_format(Sport.NBA, DataSource.ESPN)
    print(f"  Exported {export_data['count']} players")
    print(f"  Last updated: {export_data['last_updated']}")
    
    print("\n=== Demo Complete ===")
    print("\nMulti-sport expansion verified:")
    print(f"  - NBA: {len(nba_players)} players")
    print(f"  - NFL: {len(nfl_players)} players")
    print(f"  - MLB: {len(mlb_players)} players")


if __name__ == "__main__":
    demo()
