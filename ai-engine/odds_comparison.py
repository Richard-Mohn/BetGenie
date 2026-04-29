"""
BetGenie — Odds Comparison System

This module aggregates odds from multiple sportsbooks to:
1. Find the best available lines for each bet
2. Identify arbitrage opportunities
3. Calculate expected value differences across books
4. Recommend which sportsbook to use for each bet
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import requests
import os


class Sportsbook(Enum):
    DRAFTKINGS = "DraftKings"
    FANDUEL = "FanDuel"
    BETMGM = "BetMGM"
    CAESARS = "Caesars"
    POINTSBET = "PointsBet"
    BETRIVERS = "BetRivers"
    BARRERA = "Barstool Bets"
    WYNNBET = "WynnBET"


@dataclass
class OddsEntry:
    """A single odds entry from a sportsbook."""
    sportsbook: str
    player_name: str
    team: str
    prop_type: str
    line: float
    over_odds: int
    under_odds: int
    last_updated: datetime


@dataclass
class BestOdds:
    """The best available odds for a specific bet."""
    player_name: str
    team: str
    prop_type: str
    line: float
    best_over: OddsEntry
    best_under: OddsEntry
    over_ev: float
    under_ev: float
    recommendation: str


@dataclass
class ArbitrageOpportunity:
    """An arbitrage opportunity (guaranteed profit)."""
    player_name: str
    prop_type: str
    line: float
    over_book: str
    over_odds: int
    under_book: str
    under_odds: int
    guaranteed_profit: float  # Percentage
    total_investment: float
    recommended_distribution: Dict[str, float]  # Book -> amount


class OddsComparison:
    """Aggregates and compares odds across multiple sportsbooks."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        self.odds_cache: List[OddsEntry] = []
        self.last_fetch: Optional[datetime] = None
    
    def fetch_all_odds(self) -> List[OddsEntry]:
        """Fetch odds from all available sources."""
        if not self.api_key:
            return self._get_mock_odds()
        
        try:
            # In production, this would call The Odds API
            # For now, use mock data
            return self._get_mock_odds()
        except Exception as e:
            print(f"Error fetching odds: {e}")
            return self._get_mock_odds()
    
    def _get_mock_odds(self) -> List[OddsEntry]:
        """Generate mock odds from multiple sportsbooks for testing."""
        return [
            # LeBron James points
            OddsEntry("DraftKings", "LeBron James", "Los Angeles Lakers", "points", 23.5, -110, -110, datetime.now()),
            OddsEntry("FanDuel", "LeBron James", "Los Angeles Lakers", "points", 23.5, -115, -105, datetime.now()),
            OddsEntry("BetMGM", "LeBron James", "Los Angeles Lakers", "points", 24.5, -105, -115, datetime.now()),
            OddsEntry("Caesars", "LeBron James", "Los Angeles Lakers", "points", 23.5, -108, -112, datetime.now()),
            
            # SGA points
            OddsEntry("DraftKings", "Shai Gilgeous-Alexander", "Oklahoma City Thunder", "points", 31.5, -110, -110, datetime.now()),
            OddsEntry("FanDuel", "Shai Gilgeous-Alexander", "Oklahoma City Thunder", "points", 31.5, -115, -105, datetime.now()),
            OddsEntry("BetMGM", "Shai Gilgeous-Alexander", "Oklahoma City Thunder", "points", 32.5, -105, -115, datetime.now()),
            
            # Wemby rebounds
            OddsEntry("DraftKings", "Victor Wembanyama", "San Antonio Spurs", "rebounds", 10.5, -110, -110, datetime.now()),
            OddsEntry("FanDuel", "Victor Wembanyama", "San Antonio Spurs", "rebounds", 10.5, -112, -108, datetime.now()),
            OddsEntry("BetMGM", "Victor Wembanyama", "San Antonio Spurs", "rebounds", 11.5, -105, -115, datetime.now()),
        ]
    
    def find_best_odds(self, player_name: str, prop_type: str, line: float) -> Optional[BestOdds]:
        """Find the best odds across all sportsbooks for a specific bet."""
        odds = self.fetch_all_odds()
        
        # Filter for this player/prop
        matching = [
            o for o in odds 
            if o.player_name == player_name 
            and o.prop_type == prop_type
            and abs(o.line - line) <= 1.0  # Allow slight line variation
        ]
        
        if not matching:
            return None
        
        # Find best over (highest odds / least negative)
        best_over = max(matching, key=lambda o: o.over_odds)
        
        # Find best under (highest odds / least negative)
        best_under = max(matching, key=lambda o: o.under_odds)
        
        # Calculate EV for each (assuming 50% win rate for comparison)
        over_decimal = (best_over.over_odds / 100 + 1) if best_over.over_odds > 0 else (100 / abs(best_over.over_odds) + 1)
        under_decimal = (best_under.under_odds / 100 + 1) if best_under.under_odds > 0 else (100 / abs(best_under.under_odds) + 1)
        
        over_ev = (0.5 * over_decimal) - (0.5 * 1)
        under_ev = (0.5 * under_decimal) - (0.5 * 1)
        
        # Generate recommendation
        if over_ev > under_ev and over_ev > 0:
            recommendation = f"Bet OVER at {best_over.sportsbook} (best value)"
        elif under_ev > over_ev and under_ev > 0:
            recommendation = f"Bet UNDER at {best_under.sportsbook} (best value)"
        elif over_ev == under_ev:
            recommendation = f"Equal value - choose based on line preference"
        else:
            recommendation = f"No positive EV - consider skipping"
        
        return BestOdds(
            player_name=player_name,
            team=matching[0].team,
            prop_type=prop_type,
            line=line,
            best_over=best_over,
            best_under=best_under,
            over_ev=over_ev,
            under_ev=under_ev,
            recommendation=recommendation,
        )
    
    def find_arbitrage_opportunities(self, min_profit: float = 1.0) -> List[ArbitrageOpportunity]:
        """
        Find arbitrage opportunities across sportsbooks.
        
        Arbitrage exists when: (1/over_odds_decimal) + (1/under_odds_decimal) < 1
        This means you can bet both sides and guarantee profit regardless of outcome.
        """
        odds = self.fetch_all_odds()
        opportunities = []
        
        # Group by player and prop
        groups: Dict[tuple, List[OddsEntry]] = {}
        for o in odds:
            key = (o.player_name, o.prop_type, o.line)
            if key not in groups:
                groups[key] = []
            groups[key].append(o)
        
        for (player_name, prop_type, line), entries in groups.items():
            # Check all combinations for arbitrage
            for over_entry in entries:
                for under_entry in entries:
                    if over_entry.sportsbook == under_entry.sportsbook:
                        continue  # Must be different books
                    
                    # Convert to decimal
                    over_decimal = (over_entry.over_odds / 100 + 1) if over_entry.over_odds > 0 else (100 / abs(over_entry.over_odds) + 1)
                    under_decimal = (under_entry.under_odds / 100 + 1) if under_entry.under_odds > 0 else (100 / abs(under_entry.under_odds) + 1)
                    
                    # Calculate implied probabilities
                    over_prob = 1 / over_decimal
                    under_prob = 1 / under_decimal
                    total_prob = over_prob + under_prob
                    
                    # Arbitrage exists if total_prob < 1
                    if total_prob < 1:
                        profit = (1 - total_prob) * 100
                        
                        if profit >= min_profit:
                            # Calculate optimal distribution
                            over_amount = (under_prob / total_prob) * 100
                            under_amount = (over_prob / total_prob) * 100
                            
                            opportunities.append(ArbitrageOpportunity(
                                player_name=player_name,
                                prop_type=prop_type,
                                line=line,
                                over_book=over_entry.sportsbook,
                                over_odds=over_entry.over_odds,
                                under_book=under_entry.sportsbook,
                                under_odds=under_entry.under_odds,
                                guaranteed_profit=profit,
                                total_investment=100.0,
                                recommended_distribution={
                                    over_entry.sportsbook: over_amount,
                                    under_entry.sportsbook: under_amount,
                                },
                            ))
        
        return opportunities
    
    def compare_all_lines(self) -> Dict[str, BestOdds]:
        """Compare odds for all available players and props."""
        odds = self.fetch_all_odds()
        
        # Get unique player/prop combinations
        unique_combos = set((o.player_name, o.prop_type, o.line) for o in odds)
        
        results = {}
        for player_name, prop_type, line in unique_combos:
            best = self.find_best_odds(player_name, prop_type, line)
            if best:
                key = f"{player_name}_{prop_type}_{line}"
                results[key] = best
        
        return results


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — ODDS COMPARISON SYSTEM")
    print("=" * 70)
    
    comparison = OddsComparison()
    
    # Find best odds for specific players
    print("\n" + "-" * 70)
    print("  BEST ODDS BY PLAYER")
    print("-" * 70)
    
    queries = [
        ("LeBron James", "points", 23.5),
        ("Shai Gilgeous-Alexander", "points", 31.5),
        ("Victor Wembanyama", "rebounds", 10.5),
    ]
    
    for player_name, prop_type, line in queries:
        best = comparison.find_best_odds(player_name, prop_type, line)
        if best:
            print(f"\n{best.player_name} — {best.prop_type} {best.line}")
            print(f"  Best OVER: {best.best_over.sportsbook} @ {'+' if best.best_over.over_odds > 0 else ''}{best.best_over.over_odds}")
            print(f"  Best UNDER: {best.best_under.sportsbook} @ {'+' if best.best_under.under_odds > 0 else ''}{best.best_under.under_odds}")
            print(f"  Over EV: {best.over_ev:+.3f}")
            print(f"  Under EV: {best.under_ev:+.3f}")
            print(f"  💡 {best.recommendation}")
    
    # Check for arbitrage opportunities
    print("\n" + "-" * 70)
    print("  ARBITRAGE OPPORTUNITIES")
    print("-" * 70)
    
    arbs = comparison.find_arbitrage_opportunities(min_profit=0.5)
    
    if arbs:
        for arb in arbs:
            print(f"\n🎯 ARBITRAGE FOUND: {arb.player_name} {arb.prop_type} {arb.line}")
            print(f"   OVER: {arb.over_book} @ {'+' if arb.over_odds > 0 else ''}{arb.over_odds}")
            print(f"   UNDER: {arb.under_book} @ {'+' if arb.under_odds > 0 else ''}{arb.under_odds}")
            print(f"   💰 Guaranteed Profit: {arb.guaranteed_profit:.2f}%")
            print(f"   Investment: ${arb.total_investment:.2f}")
            print(f"   Distribution:")
            for book, amount in arb.recommended_distribution.items():
                print(f"     {book}: ${amount:.2f}")
    else:
        print("\n  No arbitrage opportunities found (which is normal).")
    
    # Compare all lines
    print("\n" + "-" * 70)
    print("  ALL AVAILABLE LINES")
    print("-" * 70)
    
    all_lines = comparison.compare_all_lines()
    for key, best in all_lines.items():
        print(f"\n{key}:")
        print(f"  Best OVER: {best.best_over.sportsbook} ({best.best_over.over_odds})")
        print(f"  Best UNDER: {best.best_under.sportsbook} ({best.best_under.under_odds})")
    
    print("\n" + "=" * 70)
