"""
Multi-Odds Aggregator Module

This module aggregates odds from multiple sources (OpticOdds, Sportradar, The Odds API)
for data verification and cross-referencing. This ensures accuracy and enables line shopping,
arbitrage detection, and confidence scoring based on consensus across sources.

Author: BetGenie AI Team
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum
import os
from collections import defaultdict
import requests
import json


class OddsSource(Enum):
    """Odds data sources"""
    OPTICODDS = "opticodds"
    SPORTRADAR = "sportradar"
    THE_ODDS_API = "the_odds_api"


class BetType(Enum):
    """Types of bets"""
    MONEYLINE = "moneyline"
    SPREAD = "spread"
    TOTAL = "total"
    PROP_POINTS = "prop_points"
    PROP_REBOUNDS = "prop_rebounds"
    PROP_ASSISTS = "prop_assists"


@dataclass
class OddsLine:
    """Represents a single odds line from a source"""
    source: OddsSource
    sportsbook: str
    bet_type: BetType
    selection: str  # e.g., "Lakers -5.5" or "LeBron Over 25.5 points"
    odds: float  # American odds (e.g., -110, +150) or decimal (e.g., 1.91)
    is_decimal: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_decimal_odds(self) -> float:
        """Convert American odds to decimal if needed"""
        if self.is_decimal:
            return self.odds
        
        if self.odds > 0:
            return (self.odds / 100) + 1
        else:
            return (100 / abs(self.odds)) + 1
    
    def to_american_odds(self) -> int:
        """Convert decimal odds to American if needed"""
        if not self.is_decimal:
            return int(self.odds)
        
        if self.odds >= 2.0:
            return int((self.odds - 1) * 100)
        else:
            return int(-100 / (self.odds - 1))


@dataclass
class OddsConsensus:
    """Consensus odds across multiple sources"""
    selection: str
    bet_type: BetType
    lines: List[OddsLine] = field(default_factory=list)
    
    @property
    def sources(self) -> Set[OddsSource]:
        """Unique sources contributing to this consensus"""
        return {line.source for line in self.lines}
    
    @property
    def sportsbooks(self) -> Set[str]:
        """Unique sportsbooks contributing to this consensus"""
        return {line.sportsbook for line in self.lines}
    
    @property
    def average_decimal_odds(self) -> float:
        """Average decimal odds across all lines"""
        decimal_odds = [line.to_decimal_odds() for line in self.lines]
        return sum(decimal_odds) / len(decimal_odds) if decimal_odds else 0.0
    
    @property
    def best_decimal_odds(self) -> float:
        """Best (highest) decimal odds for this selection"""
        decimal_odds = [line.to_decimal_odds() for line in self.lines]
        return max(decimal_odds) if decimal_odds else 0.0
    
    @property
    def worst_decimal_odds(self) -> float:
        """Worst (lowest) decimal odds for this selection"""
        decimal_odds = [line.to_decimal_odds() for line in self.lines]
        return min(decimal_odds) if decimal_odds else 0.0
    
    @property
    def confidence_score(self) -> float:
        """
        Confidence score based on consensus strength (0.0 to 1.0)
        Higher score = more sources agree on similar odds
        """
        if not self.lines:
            return 0.0
        
        # More sources = higher confidence
        source_bonus = min(len(self.sources) / 3.0, 1.0) * 0.3
        
        # Lower variance = higher confidence
        decimal_odds = [line.to_decimal_odds() for line in self.lines]
        if len(decimal_odds) < 2:
            variance_bonus = 0.5
        else:
            mean_odds = sum(decimal_odds) / len(decimal_odds)
            variance = sum((x - mean_odds) ** 2 for x in decimal_odds) / len(decimal_odds)
            variance_penalty = min(variance / 0.1, 1.0)  # Normalize variance
            variance_bonus = (1.0 - variance_penalty) * 0.7
        
        return source_bonus + variance_bonus
    
    def detect_arbitrage(self) -> Optional[Dict]:
        """
        Detect arbitrage opportunity for this selection
        Returns None if no arbitrage, or dict with arbitrage details
        """
        if len(self.lines) < 2:
            return None
        
        # For simple two-way arbitrage detection
        decimal_odds = [line.to_decimal_odds() for line in self.lines]
        if len(decimal_odds) < 2:
            return None
        
        # Check if sum of inverse odds < 1 (arbitrage condition)
        inverse_sum = sum(1.0 / odds for odds in decimal_odds)
        
        if inverse_sum < 1.0:
            profit_margin = (1.0 - inverse_sum) * 100
            return {
                "has_arbitrage": True,
                "profit_margin": profit_margin,
                "best_odds": self.best_decimal_odds,
                "worst_odds": self.worst_decimal_odds,
                "selection": self.selection
            }
        
        return None


@dataclass
class EventOdds:
    """All odds for a specific event/game"""
    event_id: str
    event_name: str
    sport: str = "NBA"
    start_time: Optional[datetime] = None
    consensuses: Dict[str, OddsConsensus] = field(default_factory=dict)
    
    def get_consensus(self, selection: str) -> Optional[OddsConsensus]:
        """Get consensus for a specific selection"""
        return self.consensuses.get(selection)
    
    def add_line(self, line: OddsLine):
        """Add an odds line to the appropriate consensus"""
        selection = line.selection
        if selection not in self.consensuses:
            self.consensuses[selection] = OddsConsensus(
                selection=selection,
                bet_type=line.bet_type
            )
        self.consensuses[selection].lines.append(line)
    
    def detect_arbitrage_opportunities(self) -> List[Dict]:
        """Detect all arbitrage opportunities for this event"""
        opportunities = []
        for consensus in self.consensuses.values():
            arb = consensus.detect_arbitrage()
            if arb:
                opportunities.append(arb)
        return opportunities


class MultiOddsAggregator:
    """
    Main aggregator class for fetching and consolidating odds from multiple sources.
    """
    
    def __init__(self):
        self.events: Dict[str, EventOdds] = {}
        self.api_keys = {
            OddsSource.OPTICODDS: os.getenv("OPTICODDS_API_KEY"),
            OddsSource.SPORTRADAR: os.getenv("SPORTRADAR_API_KEY"),
            OddsSource.THE_ODDS_API: os.getenv("THE_ODDS_API_KEY")
        }
    
    def fetch_from_opticodds(self, sport: str = "NBA") -> List[OddsLine]:
        """
        Fetch odds from OpticOdds API
        
        Note: This is a placeholder implementation. Actual implementation
        would use the OpticOdds API documentation.
        """
        api_key = self.api_keys[OddsSource.OPTICODDS]
        if not api_key:
            print("Warning: OpticOdds API key not set")
            return []
        
        # Placeholder for actual API call
        # response = requests.get(
        #     f"https://api.opticodds.com/odds/{sport}",
        #     headers={"Authorization": f"Bearer {api_key}"}
        # )
        # data = response.json()
        
        # Simulated data for demo
        return []
    
    def fetch_from_sportradar(self, sport: str = "NBA") -> List[OddsLine]:
        """
        Fetch odds from Sportradar API
        
        Note: This is a placeholder implementation. Actual implementation
        would use the Sportradar API documentation.
        """
        api_key = self.api_keys[OddsSource.SPORTRADAR]
        if not api_key:
            print("Warning: Sportradar API key not set")
            return []
        
        # Placeholder for actual API call
        # response = requests.get(
        #     f"https://api.sportradar.com/nba/trial/v7/en/games/{season}/schedule.json",
        #     headers={"api_key": api_key}
        # )
        # data = response.json()
        
        # Simulated data for demo
        return []
    
    def fetch_from_the_odds_api(self, sport: str = "NBA") -> List[OddsLine]:
        """
        Fetch odds from The Odds API
        
        Note: This is a placeholder implementation. Actual implementation
        would use The Odds API documentation.
        """
        api_key = self.api_keys[OddsSource.THE_ODDS_API]
        if not api_key:
            print("Warning: The Odds API key not set")
            return []
        
        # Placeholder for actual API call
        # response = requests.get(
        #     f"https://api.the-odds-api.com/v4/sports/{sport}/odds",
        #     params={"apiKey": api_key}
        # )
        # data = response.json()
        
        # Simulated data for demo
        return []
    
    def fetch_all_sources(self, sport: str = "NBA") -> Dict[OddsSource, List[OddsLine]]:
        """
        Fetch odds from all configured sources
        """
        all_odds = {}
        
        # Fetch from each source
        all_odds[OddsSource.OPTICODDS] = self.fetch_from_opticodds(sport)
        all_odds[OddsSource.SPORTRADAR] = self.fetch_from_sportradar(sport)
        all_odds[OddsSource.THE_ODDS_API] = self.fetch_from_the_odds_api(sport)
        
        return all_odds
    
    def consolidate_odds(self, all_odds: Dict[OddsSource, List[OddsLine]]) -> Dict[str, EventOdds]:
        """
        Consolidate odds from multiple sources into EventOdds objects
        """
        # Group lines by event
        event_lines = defaultdict(list)
        
        for source, lines in all_odds.items():
            for line in lines:
                # Extract event_id from line (implementation depends on API structure)
                # For now, using a simple grouping approach
                event_key = f"{line.selection}_{line.bet_type.value}"
                event_lines[event_key].append(line)
        
        # Create EventOdds objects
        consolidated = {}
        for event_key, lines in event_lines.items():
            if not lines:
                continue
            
            # Create event odds
            event_odds = EventOdds(
                event_id=event_key,
                event_name=event_key,
                sport="NBA"
            )
            
            # Add all lines
            for line in lines:
                event_odds.add_line(line)
            
            consolidated[event_key] = event_odds
        
        return consolidated
    
    def verify_odds(self, selection: str, expected_odds: float, tolerance: float = 0.05) -> bool:
        """
        Verify that odds from multiple sources are consistent within tolerance
        
        Args:
            selection: The bet selection to verify
            expected_odds: The expected odds (decimal format)
            tolerance: Acceptable variance (default 5%)
        
        Returns:
            True if odds are consistent within tolerance across sources
        """
        # Find all events with this selection
        matching_events = []
        for event in self.events.values():
            if selection in event.consensuses:
                matching_events.append(event)
        
        if not matching_events:
            return False
        
        # Check variance across sources
        for event in matching_events:
            consensus = event.consensuses[selection]
            avg_odds = consensus.average_decimal_odds
            
            if avg_odds == 0:
                continue
            
            variance = abs(avg_odds - expected_odds) / expected_odds
            if variance > tolerance:
                return False
        
        return True
    
    def get_best_line(self, selection: str, bet_type: BetType) -> Optional[OddsLine]:
        """
        Get the best (highest odds) line for a specific selection across all sources
        """
        best_line = None
        best_decimal_odds = 0.0
        
        for event in self.events.values():
            consensus = event.get_consensus(selection)
            if consensus and consensus.bet_type == bet_type:
                for line in consensus.lines:
                    decimal_odds = line.to_decimal_odds()
                    if decimal_odds > best_decimal_odds:
                        best_decimal_odds = decimal_odds
                        best_line = line
        
        return best_line
    
    def detect_all_arbitrage(self) -> List[Dict]:
        """
        Detect all arbitrage opportunities across all events
        """
        opportunities = []
        for event in self.events.values():
            opportunities.extend(event.detect_arbitrage_opportunities())
        return opportunities
    
    def update_odds(self, sport: str = "NBA"):
        """
        Update odds from all sources and consolidate
        """
        # Fetch from all sources
        all_odds = self.fetch_all_sources(sport)
        
        # Consolidate
        self.events = self.consolidate_odds(all_odds)
        
        print(f"Updated odds for {len(self.events)} events")
        
        # Report arbitrage opportunities
        arbs = self.detect_all_arbitrage()
        if arbs:
            print(f"Found {len(arbs)} arbitrage opportunities")
            for arb in arbs:
                print(f"  - {arb['selection']}: {arb['profit_margin']:.2f}% margin")


def demo():
    """Demo the multi-odds aggregator"""
    print("=== Multi-Odds Aggregator Demo ===\n")
    
    # Create aggregator
    aggregator = MultiOddsAggregator()
    
    # Add some mock data for demonstration
    mock_lines = [
        OddsLine(
            source=OddsSource.THE_ODDS_API,
            sportsbook="DraftKings",
            bet_type=BetType.MONEYLINE,
            selection="Lakers vs Celtics",
            odds=-110,
            is_decimal=False
        ),
        OddsLine(
            source=OddsSource.OPTICODDS,
            sportsbook="FanDuel",
            bet_type=BetType.MONEYLINE,
            selection="Lakers vs Celtics",
            odds=-108,
            is_decimal=False
        ),
        OddsLine(
            source=OddsSource.SPORTRADAR,
            sportsbook="BetMGM",
            bet_type=BetType.MONEYLINE,
            selection="Lakers vs Celtics",
            odds=-112,
            is_decimal=False
        ),
        OddsLine(
            source=OddsSource.THE_ODDS_API,
            sportsbook="DraftKings",
            bet_type=BetType.PROP_POINTS,
            selection="LeBron Over 25.5 points",
            odds=-110,
            is_decimal=False
        ),
        OddsLine(
            source=OddsSource.OPTICODDS,
            sportsbook="FanDuel",
            bet_type=BetType.PROP_POINTS,
            selection="LeBron Over 25.5 points",
            odds=-105,
            is_decimal=False
        ),
    ]
    
    # Create event and add lines
    event = EventOdds(
        event_id="lakers_celtics_20250415",
        event_name="Lakers vs Celtics"
    )
    
    for line in mock_lines:
        event.add_line(line)
    
    aggregator.events[event.event_id] = event
    
    # Display consensuses
    print("Event Odds Consensuses:")
    for selection, consensus in event.consensuses.items():
        print(f"\n  Selection: {selection}")
        print(f"  Bet Type: {consensus.bet_type.value}")
        print(f"  Sources: {', '.join(s.value for s in consensus.sources)}")
        print(f"  Sportsbooks: {', '.join(consensus.sportsbooks)}")
        print(f"  Average Decimal Odds: {consensus.average_decimal_odds:.3f}")
        print(f"  Best Decimal Odds: {consensus.best_decimal_odds:.3f}")
        print(f"  Worst Decimal Odds: {consensus.worst_decimal_odds:.3f}")
        print(f"  Confidence Score: {consensus.confidence_score:.2f}")
        
        # Check for arbitrage
        arb = consensus.detect_arbitrage()
        if arb:
            print(f"  ⚠ ARBITRAGE OPPORTUNITY: {arb['profit_margin']:.2f}% margin")
    
    # Get best line
    print("\n\nBest Line Search:")
    best_line = aggregator.get_best_line("LeBron Over 25.5 points", BetType.PROP_POINTS)
    if best_line:
        print(f"  Selection: {best_line.selection}")
        print(f"  Source: {best_line.source.value}")
        print(f"  Sportsbook: {best_line.sportsbook}")
        print(f"  Odds: {best_line.odds}")
        print(f"  Decimal: {best_line.to_decimal_odds():.3f}")
    
    # Verify odds
    print("\n\nOdds Verification:")
    is_verified = aggregator.verify_odds("Lakers vs Celtics", 1.91, tolerance=0.05)
    print(f"  Lakers vs Celtics odds verified: {is_verified}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
