"""
BoltOdds API Integration
Real-time sports betting odds via WebSocket
"""

import json
import asyncio
import websockets
from typing import Dict, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass
import os

@dataclass
class BoltOddsConfig:
    """Configuration for BoltOdds API"""
    api_key: str = "9ed66088-9cce-4529-a0c2-f4452aac05cb"
    websocket_url: str = "wss://spro.agency/api"
    rest_base_url: str = "https://spro.agency/api"
    
    # Subscription filters
    sports: List[str] = None
    sportsbooks: List[str] = None
    games: List[str] = None
    markets: List[str] = None
    
    def __post_init__(self):
        if self.sports is None:
            self.sports = ["NBA"]  # Focus on NBA first
        if self.sportsbooks is None:
            self.sportsbooks = ["draftkings", "fanduel", "betmgm", "caesars"]  # Major US books
        if self.games is None:
            self.games = []  # Empty = all games
        if self.markets is None:
            self.markets = ["Moneyline", "Spread", "Total", "Player Props"]  # Key markets

class BoltOddsAPI:
    """BoltOdds WebSocket API Client"""
    
    def __init__(self, config: BoltOddsConfig = None):
        self.config = config or BoltOddsConfig()
        self.websocket = None
        self.connected = False
        self.message_handlers = []
    
    def add_message_handler(self, handler: Callable):
        """Add a callback function to handle incoming messages"""
        self.message_handlers.append(handler)
    
    async def connect(self) -> bool:
        """Establish WebSocket connection"""
        uri = f"{self.config.websocket_url}?key={self.config.api_key}"
        
        try:
            self.websocket = await websockets.connect(uri, max_size=None)
            ack_message = await self.websocket.recv()
            print(f"BoltOdds Connected: {ack_message}")
            self.connected = True
            
            # Send subscription
            await self.subscribe()
            
            return True
        except Exception as e:
            print(f"Error connecting to BoltOdds: {e}")
            return False
    
    async def subscribe(self):
        """Subscribe to specific sports, books, games, markets"""
        subscribe_message = {
            "action": "subscribe",
            "filters": {
                "sports": self.config.sports,
                "sportsbooks": self.config.sportsbooks,
                "games": self.config.games,
                "markets": self.config.markets
            }
        }
        
        await self.websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to: Sports={self.config.sports}, Books={self.config.sportsbooks}, Markets={self.config.markets}")
    
    async def listen(self):
        """Listen for incoming messages"""
        if not self.connected:
            print("Not connected to BoltOdds")
            return
        
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # Call all registered handlers
                for handler in self.message_handlers:
                    await handler(data)
                    
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print("BoltOdds disconnected")
    
    def get_rest_url(self, endpoint: str) -> str:
        """Get REST API URL"""
        return f"{self.config.rest_base_url}/{endpoint}?key={self.config.api_key}"
    
    async def get_info(self) -> Dict:
        """Get available sports and sportsbooks (REST endpoint)"""
        import aiohttp
        
        url = self.get_rest_url("get_info")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def get_games(self) -> Dict:
        """Get available games (REST endpoint)"""
        import aiohttp
        
        url = self.get_rest_url("get_games")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def get_markets(self, sports: str = None, sportsbooks: str = None) -> Dict:
        """Get available markets (REST endpoint)"""
        import aiohttp
        
        params = {}
        if sports:
            params["sports"] = sports
        if sportsbooks:
            params["sportsbooks"] = sportsbooks
        
        url = self.get_rest_url("get_markets")
        if params:
            url += "&" + "&".join(f"{k}={v}" for k, v in params.items())
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
    
    async def get_parlays(self, sportsbook: str) -> List[Dict]:
        """Get parlay betting data for a specific sportsbook"""
        import aiohttp
        
        url = f"{self.config.rest_base_url}/get_parlays?key={self.config.api_key}&sportsbook={sportsbook}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

# Convenience function for testing
async def test_boltodds():
    """Test BoltOdds API connection and data retrieval"""
    config = BoltOddsConfig()
    api = BoltOddsAPI(config)
    
    print("Testing BoltOdds REST endpoints...")
    
    # Test REST endpoints
    info = await api.get_info()
    print(f"Available sports: {len(info.get('sports', []))}")
    print(f"Available sportsbooks: {len(info.get('sportsbooks', []))}")
    print(f"NBA available: {'NBA' in info.get('sports', [])}")
    
    # Get NBA games
    games = await api.get_games()
    nba_games = {k: v for k, v in games.items() if v.get('sport') == 'NBA'}
    print(f"Total NBA games: {len(nba_games)}")
    
    # Get NBA markets for DraftKings
    markets = await api.get_markets(sports="NBA", sportsbooks="draftkings")
    print(f"DraftKings NBA markets: {len(markets.get('draftkings', {}).get('NBA', []))}")
    
    # Get parlays
    parlays = await api.get_parlays("draftkings")
    print(f"Available parlays: {len(parlays)}")
    
    return info, games, markets, parlays

if __name__ == "__main__":
    asyncio.run(test_boltodds())
