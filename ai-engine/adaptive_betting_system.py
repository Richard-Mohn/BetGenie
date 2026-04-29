"""
BetGenie — Adaptive Betting System

Starts with small bets and automatically scales up based on proven win rate.
This is the "learning" component that gradually increases bet sizes as the system
demonstrates consistent profitability.

Philosophy:
- Start small ($1-2) to test the system
- Track win rate over rolling window (last 50 bets)
- Scale up incrementally as win rate improves
- Scale down immediately if win rate drops
- Always protect bankroll with maximum limits
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum
import json


class ScalingPhase(Enum):
    """Phases of adaptive betting."""
    TESTING = "testing"           # $1-2 bets, proving the system
    GROWTH = "growth"             # $5-10 bets, proven winner
    EXPANSION = "expansion"       # $20-50 bets, consistent profits
    MAXIMUM = "maximum"           # $50-100 bets, elite performance
    RETREAT = "retreat"           # Scale down after losses


@dataclass
class BetResult:
    """Result of a single bet."""
    bet_id: str
    timestamp: datetime
    player_name: str
    bet_type: str  # "points", "rebounds", etc.
    line: float
    direction: str  # "OVER" or "UNDER"
    bet_amount: float
    odds: int
    won: bool
    profit: float
    confidence: float  # AI confidence at time of bet
    phase: ScalingPhase


@dataclass
class AdaptiveSession:
    """Tracks the adaptive betting session."""
    session_id: str
    start_date: datetime
    initial_bankroll: float
    current_bankroll: float
    current_phase: ScalingPhase
    bet_history: List[BetResult] = field(default_factory=list)
    total_bets: int = 0
    wins: int = 0
    losses: int = 0
    pushes: int = 0
    total_profit: float = 0.0
    current_bet_size: float = 1.0  # Start at $1
    rolling_win_rate: float = 0.0
    rolling_window_size: int = 50  # Track last 50 bets


class AdaptiveBettingSystem:
    """
    Adaptive betting system that learns and scales based on performance.
    
    Scaling Rules:
    - TESTING phase: $1-2 bets (first 20 bets)
    - GROWTH phase: $5-10 bets (win rate > 55% over 50 bets)
    - EXPANSION phase: $20-50 bets (win rate > 60% over 50 bets)
    - MAXIMUM phase: $50-100 bets (win rate > 65% over 50 bets)
    - RETREAT phase: Scale down if win rate drops below 50%
    """
    
    def __init__(self, initial_bankroll: float, max_bet_percentage: float = 0.02):
        self.initial_bankroll = initial_bankroll
        self.max_bet_percentage = max_bet_percentage
        self.session = AdaptiveSession(
            session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            start_date=datetime.now(),
            initial_bankroll=initial_bankroll,
            current_bankroll=initial_bankroll,
            current_phase=ScalingPhase.TESTING,
            current_bet_size=1.0
        )
    
    def get_current_bet_size(self) -> float:
        """Get the current bet size based on phase."""
        return self.session.current_bet_size
    
    def record_bet(
        self,
        player_name: str,
        bet_type: str,
        line: float,
        direction: str,
        odds: int,
        confidence: float
    ) -> BetResult:
        """Place a bet and record it."""
        bet_amount = self.get_current_bet_size()
        
        # Calculate potential profit
        if odds > 0:
            potential_profit = bet_amount * (odds / 100)
        else:
            potential_profit = bet_amount * (100 / abs(odds))
        
        bet_result = BetResult(
            bet_id=f"bet_{self.session.total_bets + 1}",
            timestamp=datetime.now(),
            player_name=player_name,
            bet_type=bet_type,
            line=line,
            direction=direction,
            bet_amount=bet_amount,
            odds=odds,
            won=False,  # Will be updated when result comes in
            profit=0.0,
            confidence=confidence,
            phase=self.session.current_phase
        )
        
        self.session.bet_history.append(bet_result)
        self.session.total_bets += 1
        
        return bet_result
    
    def settle_bet(self, bet_id: str, won: bool) -> float:
        """Settle a bet and update session state."""
        bet = next((b for b in self.session.bet_history if b.bet_id == bet_id), None)
        if not bet:
            return 0.0
        
        bet.won = won
        
        if won:
            if bet.odds > 0:
                profit = bet.bet_amount * (bet.odds / 100)
            else:
                profit = bet.bet_amount * (100 / abs(bet.odds))
            self.session.wins += 1
            self.session.current_bankroll += profit
        else:
            profit = -bet.bet_amount
            self.session.losses += 1
            self.session.current_bankroll += profit
        
        bet.profit = profit
        self.session.total_profit += profit
        
        # Update rolling win rate
        self._update_rolling_win_rate()
        
        # Check if we should scale
        self._check_scaling()
        
        return profit
    
    def _update_rolling_win_rate(self):
        """Calculate rolling win rate over last N bets."""
        window = self.session.bet_history[-self.session.rolling_window_size:]
        if not window:
            self.session.rolling_win_rate = 0.0
            return
        
        settled_bets = [b for b in window if b.won is not None]
        if not settled_bets:
            self.session.rolling_win_rate = 0.0
            return
        
        wins = sum(1 for b in settled_bets if b.won)
        self.session.rolling_win_rate = wins / len(settled_bets)
    
    def _check_scaling(self):
        """Check if we should scale up or down based on performance."""
        settled_count = len([b for b in self.session.bet_history if b.won is not None])
        
        # Need at least 20 settled bets to make scaling decisions
        if settled_count < 20:
            return
        
        win_rate = self.session.rolling_win_rate
        
        # Scale up logic
        if win_rate >= 0.65 and self.session.current_phase != ScalingPhase.MAXIMUM:
            self._scale_to_phase(ScalingPhase.MAXIMUM)
        elif win_rate >= 0.60 and self.session.current_phase in [ScalingPhase.TESTING, ScalingPhase.GROWTH]:
            self._scale_to_phase(ScalingPhase.EXPANSION)
        elif win_rate >= 0.55 and self.session.current_phase == ScalingPhase.TESTING:
            self._scale_to_phase(ScalingPhase.GROWTH)
        
        # Scale down logic
        elif win_rate < 0.50 and self.session.current_phase != ScalingPhase.TESTING:
            self._scale_to_phase(ScalingPhase.RETREAT)
        elif win_rate < 0.45:
            self._scale_to_phase(ScalingPhase.TESTING)
    
    def _scale_to_phase(self, new_phase: ScalingPhase):
        """Scale to a new phase with appropriate bet size."""
        old_phase = self.session.current_phase
        self.session.current_phase = new_phase
        
        # Set bet size based on phase
        if new_phase == ScalingPhase.TESTING:
            self.session.current_bet_size = 1.0
        elif new_phase == ScalingPhase.GROWTH:
            self.session.current_bet_size = 5.0
        elif new_phase == ScalingPhase.EXPANSION:
            self.session.current_bet_size = 20.0
        elif new_phase == ScalingPhase.MAXIMUM:
            max_bet = self.session.current_bankroll * self.max_bet_percentage
            self.session.current_bet_size = min(100.0, max_bet)
        elif new_phase == ScalingPhase.RETREAT:
            self.session.current_bet_size = 2.0  # Conservative retreat
        
        print(f"SCALING: {old_phase.value} -> {new_phase.value}")
        print(f"  New bet size: ${self.session.current_bet_size:.2f}")
        print(f"  Rolling win rate: {self.session.rolling_win_rate:.1%}")
    
    def get_session_stats(self) -> dict:
        """Get current session statistics."""
        settled_bets = [b for b in self.session.bet_history if b.won is not None]
        
        return {
            "session_id": self.session.session_id,
            "current_phase": self.session.current_phase.value,
            "current_bet_size": self.session.current_bet_size,
            "total_bets": self.session.total_bets,
            "settled_bets": len(settled_bets),
            "wins": self.session.wins,
            "losses": self.session.losses,
            "pushes": self.session.pushes,
            "win_rate": self.session.wins / len(settled_bets) if settled_bets else 0.0,
            "rolling_win_rate": self.session.rolling_win_rate,
            "initial_bankroll": self.session.initial_bankroll,
            "current_bankroll": self.session.current_bankroll,
            "total_profit": self.session.total_profit,
            "roi": (self.session.total_profit / self.session.initial_bankroll * 100) if self.session.initial_bankroll > 0 else 0.0
        }
    
    def export_session(self) -> str:
        """Export session data to JSON."""
        data = {
            "session_id": self.session.session_id,
            "start_date": self.session.start_date.isoformat(),
            "initial_bankroll": self.session.initial_bankroll,
            "current_bankroll": self.session.current_bankroll,
            "current_phase": self.session.current_phase.value,
            "current_bet_size": self.session.current_bet_size,
            "total_bets": self.session.total_bets,
            "wins": self.session.wins,
            "losses": self.session.losses,
            "pushes": self.session.pushes,
            "total_profit": self.session.total_profit,
            "rolling_win_rate": self.session.rolling_win_rate,
            "bet_history": [
                {
                    "bet_id": b.bet_id,
                    "timestamp": b.timestamp.isoformat(),
                    "player_name": b.player_name,
                    "bet_type": b.bet_type,
                    "line": b.line,
                    "direction": b.direction,
                    "bet_amount": b.bet_amount,
                    "odds": b.odds,
                    "won": b.won,
                    "profit": b.profit,
                    "confidence": b.confidence,
                    "phase": b.phase.value
                }
                for b in self.session.bet_history
            ]
        }
        return json.dumps(data, indent=2)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — ADAPTIVE BETTING SYSTEM")
    print("  Start Small, Scale Up Based on Performance")
    print("=" * 70)
    
    # Initialize with $500 bankroll
    system = AdaptiveBettingSystem(initial_bankroll=500.0, max_bet_percentage=0.02)
    
    print(f"\nInitial Bankroll: ${system.session.initial_bankroll:.2f}")
    print(f"Starting Phase: {system.session.current_phase.value}")
    print(f"Starting Bet Size: ${system.session.current_bet_size:.2f}")
    
    print("\n" + "-" * 70)
    print("  SIMULATING BETS")
    print("-" * 70)
    
    # Simulate 30 bets with varying results
    import random
    
    players = ["LeBron James", "Stephen Curry", "Kevin Durant", "Luka Dončić", "Giannis"]
    
    for i in range(30):
        player = random.choice(players)
        bet = system.record_bet(
            player_name=player,
            bet_type="points",
            line=25.5,
            direction="OVER",
            odds=-110,
            confidence=75.0
        )
        
        # Simulate result (60% win rate for demo)
        won = random.random() < 0.60
        profit = system.settle_bet(bet.bet_id, won)
        
        if i % 10 == 0:
            print(f"\nBet {i+1}: {player} - ${bet.bet_amount:.2f} - {'WON' if won else 'LOST'}")
            print(f"  Bankroll: ${system.session.current_bankroll:.2f}")
            print(f"  Phase: {system.session.current_phase.value}")
            print(f"  Rolling Win Rate: {system.session.rolling_win_rate:.1%}")
    
    print("\n" + "-" * 70)
    print("  SESSION STATS")
    print("-" * 70)
    
    stats = system.get_session_stats()
    print(f"\nTotal Bets: {stats['total_bets']}")
    print(f"Settled Bets: {stats['settled_bets']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Win Rate: {stats['win_rate']:.1%}")
    print(f"Rolling Win Rate: {stats['rolling_win_rate']:.1%}")
    print(f"Current Phase: {stats['current_phase']}")
    print(f"Current Bet Size: ${stats['current_bet_size']:.2f}")
    print(f"Initial Bankroll: ${stats['initial_bankroll']:.2f}")
    print(f"Current Bankroll: ${stats['current_bankroll']:.2f}")
    print(f"Total Profit: ${stats['total_profit']:.2f}")
    print(f"ROI: {stats['roi']:.1f}%")
    
    print("\n" + "=" * 70)
    print("  ADAPTIVE BETTING SYSTEM — READY")
    print("  System learns and scales based on proven performance")
    print("=" * 70)
