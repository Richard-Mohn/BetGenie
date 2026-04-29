"""
BetGenie — The Odds API Integration

Real sportsbook odds via The Odds API (the-odds-api.com)
Free tier: 500 requests/month
Paid tier: 10,000+ requests/month
"""

import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class RealOddsLine:
    """Real odds from sportsbook."""
    sportsbook: str
    player_name: str
    team: str
    prop_type: str  # 'points', 'rebounds', 'assists', etc.
    line: float
    over_odds: int
    under_odds: int
    last_updated: datetime
    game_id: Optional[str] = None


class TheOddsAPI:
    """
    Client for The Odds API (https://the-odds-api.com)
    
    Provides real-time sportsbook odds for player props.
    """
    
    BASE_URL = "https://api.the-odds-api.com/v4"
    
    # Supported player prop markets
    PLAYER_PROP_MARKETS = {
        "player_points": "Points",
        "player_rebounds": "Rebounds", 
        "player_assists": "Assists",
        "player_threes": "Three Pointers Made",
        "player_blocks": "Blocks",
        "player_steals": "Steals",
        "player_turnovers": "Turnovers",
        "player_points_rebounds_assists": "PRA",
        "player_points_rebounds": "Points + Rebounds",
        "player_points_assists": "Points + Assists",
        "player_rebounds_assists": "Rebounds + Assists",
    }
    
    SUPPORTED_BOOKS = [
        "draftkings", "fanduel", "betmgm", "caesars", "pointsbet",
        "bet365", "bovada", "wynnbet", "unibet", "barstool"
    ]
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("THE_ODDS_API_KEY")
        if not self.api_key:
            print("WARNING: No API key provided. Set THE_ODDS_API_KEY environment variable.")
            print("Get free API key at: https://the-odds-api.com")
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make API request with error handling."""
        if not self.api_key:
            return None
        
        url = f"{self.BASE_URL}/{endpoint}"
        params = params or {}
        params["apiKey"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            # Check rate limit remaining
            remaining = response.headers.get("X-Requests-Remaining")
            if remaining:
                print(f"API requests remaining: {remaining}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("ERROR: Invalid API key")
            elif e.response.status_code == 429:
                print("ERROR: Rate limit exceeded")
            else:
                print(f"HTTP Error: {e}")
            return None
        
        except Exception as e:
            print(f"API request failed: {e}")
            return None
    
    def get_sports(self) -> List[Dict]:
        """Get list of available sports."""
        data = self._make_request("sports")
        return data if data else []
    
    def get_nba_events(self, date: Optional[str] = None) -> List[Dict]:
        """
        Get NBA events (games) for today or specific date.
        
        Args:
            date: Date in ISO format (YYYY-MM-DD). If None, gets today's games.
        
        Returns:
            List of event dictionaries with game info
        """
        if date:
            endpoint = f"sports/basketball_nba/events/{date}"
        else:
            endpoint = "sports/basketball_nba/events"
        
        data = self._make_request(endpoint, {"regions": "us"})
        return data if data else []
    
    def get_player_props(self, event_id: str, markets: List[str] = None, 
                         sportsbooks: List[str] = None) -> List[RealOddsLine]:
        """
        Get player prop odds for a specific game.
        
        Args:
            event_id: The event ID from get_nba_events
            markets: List of market keys (e.g., ['player_points', 'player_rebounds'])
            sportsbooks: List of sportsbook keys to include
        
        Returns:
            List of RealOddsLine objects
        """
        markets = markets or ["player_points"]
        sportsbooks = sportsbooks or ["draftkings", "fanduel"]
        
        params = {
            "regions": "us",
            "markets": ",".join(markets),
            "oddsFormat": "american",
            "bookmakers": ",".join(sportsbooks),
        }
        
        data = self._make_request(f"sports/basketball_nba/events/{event_id}/odds", params)
        
        if not data:
            return []
        
        odds_lines = []
        
        # Parse bookmaker data
        for bookmaker_data in data.get("bookmakers", []):
            bookmaker = bookmaker_data.get("key", "unknown")
            
            for market in bookmaker_data.get("markets", []):
                market_key = market.get("key", "")
                
                # Skip non-player-prop markets
                if not market_key.startswith("player_"):
                    continue
                
                prop_type = self.PLAYER_PROP_MARKETS.get(market_key, market_key)
                
                # Process each outcome
                for outcome in market.get("outcomes", []):
                    player_name = outcome.get("description", "")
                    name = outcome.get("name", "").lower()
                    price = outcome.get("price", 0)
                    point = outcome.get("point", 0)
                    
                    if not player_name or not point:
                        continue
                    
                    # Find matching over/under pair
                    matching_line = None
                    for existing in odds_lines:
                        if (existing.player_name == player_name and 
                            existing.prop_type == prop_type and
                            existing.line == point and
                            existing.sportsbook == bookmaker):
                            matching_line = existing
                            break
                    
                    if matching_line:
                        if "over" in name:
                            matching_line.over_odds = price
                        elif "under" in name:
                            matching_line.under_odds = price
                    else:
                        # Create new line
                        is_over = "over" in name
                        odds_lines.append(RealOddsLine(
                            sportsbook=bookmaker,
                            player_name=player_name,
                            team="",  # Will need to map from player data
                            prop_type=prop_type.lower(),
                            line=float(point),
                            over_odds=price if is_over else -110,
                            under_odds=price if not is_over else -110,
                            last_updated=datetime.now(timezone.utc),
                            game_id=event_id
                        ))
        
        return odds_lines
    
    def get_all_player_props_today(self, sportsbooks: List[str] = None) -> List[RealOddsLine]:
        """
        Get all player props for today's NBA games.
        
        Returns:
            List of RealOddsLine from all games
        """
        sportsbooks = sportsbooks or ["draftkings", "fanduel"]
        
        print("Fetching today's NBA games...")
        events = self.get_nba_events()
        
        if not events:
            print("No NBA events found")
            return []
        
        print(f"Found {len(events)} NBA games")
        
        all_odds = []
        markets = ["player_points", "player_rebounds", "player_assists"]
        
        for event in events:
            event_id = event.get("id")
            home_team = event.get("home_team", "Unknown")
            away_team = event.get("away_team", "Unknown")
            
            print(f"  Fetching props for: {away_team} @ {home_team}")
            
            odds = self.get_player_props(event_id, markets, sportsbooks)
            
            # Add game info to each odds line
            for line in odds:
                line.game_id = event_id
            
            all_odds.extend(odds)
        
        return all_odds
    
    def get_usage_stats(self) -> Optional[Dict]:
        """Get API usage statistics."""
        if not self.api_key:
            return None
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/sports",
                params={"apiKey": self.api_key},
                timeout=10
            )
            
            return {
                "remaining": response.headers.get("X-Requests-Remaining"),
                "used": response.headers.get("X-Requests-Used"),
                "resets_at": response.headers.get("X-Requests-Reset")
            }
        except:
            return None


# ========== DEMO ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — THE ODDS API DEMO")
    print("=" * 70)
    
    api = TheOddsAPI()
    
    if not api.api_key:
        print("\n❌ No API key configured")
        print("Get your free API key at: https://the-odds-api.com")
        print("Set environment variable: THE_ODDS_API_KEY=your_key")
        print("\nDEMO MODE: Showing example data structure...")
        
        # Demo with fake data
        example_odds = [
            RealOddsLine(
                sportsbook="DraftKings",
                player_name="LeBron James",
                team="Los Angeles Lakers",
                prop_type="points",
                line=26.5,
                over_odds=-110,
                under_odds=-110,
                last_updated=datetime.now(timezone.utc)
            ),
            RealOddsLine(
                sportsbook="DraftKings",
                player_name="Nikola Jokic",
                team="Denver Nuggets",
                prop_type="points",
                line=28.5,
                over_odds=-115,
                under_odds=-105,
                last_updated=datetime.now(timezone.utc)
            ),
        ]
        
        print(f"\n📊 Example odds lines:")
        for odds in example_odds:
            print(f"  • {odds.player_name} {odds.line} {odds.prop_type} (o{odds.over_odds}/u{odds.under_odds}) [{odds.sportsbook}]")
    
    else:
        print("\n✅ API key configured")
        
        # Check usage
        usage = api.get_usage_stats()
        if usage:
            print(f"\n📊 API Usage:")
            print(f"  Remaining: {usage.get('remaining', 'N/A')}")
            print(f"  Used: {usage.get('used', 'N/A')}")
        
        # Get today's games
        print("\n🏀 Today's NBA Games:")
        events = api.get_nba_events()
        for event in events[:5]:  # Show first 5
            home = event.get("home_team", "Unknown")
            away = event.get("away_team", "Unknown")
            commence = event.get("commence_time", "Unknown")
            print(f"  • {away} @ {home} ({commence})")
        
        # Get player props for first game
        if events:
            print(f"\n🎯 Player Props for {events[0].get('away_team')} @ {events[0].get('home_team')}:")
            props = api.get_player_props(events[0]["id"], ["player_points"], ["draftkings"])
            
            for prop in props[:10]:  # Show first 10
                print(f"  • {prop.player_name}: {prop.line} {prop.prop_type} (o{prop.over_odds}/u{prop.under_odds})")
    
    print("\n" + "=" * 70)
    print("  THE ODDS API DEMO COMPLETE")
    print("=" * 70)
