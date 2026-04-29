"""
BetGenie — Backtesting System

Validates Player Impact Score (PIS) accuracy by:
1. Loading historical player performance data
2. Calculating PIS for historical events
3. Comparing PIS predictions vs actual outcomes
4. Generating accuracy reports
"""

import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import statistics
from pathlib import Path

from impact_score import calculate_impact_score, PlayerEvent, EventCategory
from database import BetGenieDatabase, PredictionDB


@dataclass
class BacktestResult:
    """Result of a single backtest."""
    player_name: str
    game_date: str
    pis_score: float
    projected_performance: float
    actual_performance: float
    error: float  # Difference between projected and actual
    events_count: int
    prediction_correct: bool  # Did PIS predict above/below average correctly?


@dataclass
class BacktestSummary:
    """Summary of all backtests."""
    total_games: int
    mean_absolute_error: float
    correlation: float
    direction_accuracy: float  # % of time PIS predicted direction correctly
    high_pis_accuracy: float  # Accuracy when PIS > 85
    low_pis_accuracy: float  # Accuracy when PIS < 65
    results: List[BacktestResult]


class Backtester:
    """
    Backtesting system for PIS validation.
    
    Tests how well PIS predicts player performance vs actual outcomes.
    """
    
    def __init__(self, db: BetGenieDatabase = None):
        self.db = db or BetGenieDatabase()
    
    def load_historical_data(self, player_name: str, season: str = "2024-25") -> List[Dict]:
        """
        Load historical game data for a player.
        
        In production, this would fetch from NBA API or database.
        For now, generates synthetic data for testing.
        """
        # Check database first
        db_data = self.db.get_player_performance_with_pis(player_name)
        if db_data:
            return db_data
        
        # Generate synthetic test data for backtesting
        # In real implementation, this would be actual NBA data
        print(f"No historical data found for {player_name}, generating synthetic test data...")
        return self._generate_synthetic_data(player_name)
    
    def _generate_synthetic_data(self, player_name: str) -> List[Dict]:
        """Generate synthetic historical data for testing."""
        import random
        
        # Base stats by player (simplified)
        base_ppg = {
            "nikola jokic": 29.4,
            "joel embiid": 34.7,
            "lebron james": 25.7,
            "jayson tatum": 27.2,
            "jalen brunson": 28.2,
        }.get(player_name.lower(), 20.0)
        
        games = []
        base_date = datetime(2024, 10, 22)  # NBA season start
        
        for i in range(60):  # 60 games
            game_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Random variation
            actual_ppg = base_ppg + random.uniform(-8, 8)
            
            # Occasionally add a "bad game" (simulating impact of events)
            if random.random() < 0.15:  # 15% chance of bad game
                actual_ppg -= random.uniform(5, 12)
            
            games.append({
                "player_name": player_name,
                "game_date": game_date,
                "points": round(actual_ppg, 1),
                "rebounds": round(random.uniform(5, 12), 1),
                "assists": round(random.uniform(3, 10), 1),
                "pis_score": 75.0,  # Will be calculated from events
                "events_count": 0,
                "opponent": f"OPP{i % 30}"
            })
        
        return games
    
    def create_historical_events(self, player_name: str, 
                                  event_type: str, date_str: str,
                                  severity: float = 0.8) -> List[PlayerEvent]:
        """
        Create historical PlayerEvent objects for backtesting.
        
        Args:
            player_name: Player name
            event_type: Type of event ('legal', 'family', 'health', 'trade')
            date_str: Date of event (YYYY-MM-DD)
            severity: Event severity (0.0-1.0)
        
        Returns:
            List of PlayerEvent objects
        """
        category_map = {
            "legal": EventCategory.LEGAL_ARREST,
            "family": EventCategory.FAMILY_NEGATIVE,
            "health": EventCategory.HEALTH_INJURY,
            "trade": EventCategory.TEAM_TRADE,
            "streak": EventCategory.PERFORMANCE_STREAK_COLD,
        }
        
        category = category_map.get(event_type, EventCategory.SOCIAL_CONTROVERSY)
        
        event_date = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
        
        return [PlayerEvent(
            event_id=f"hist-{player_name}-{date_str}",
            player_id=player_name,
            category=category,
            description=f"Historical {event_type} event",
            source_urls=["https://historical.example.com"],
            sentiment_score=-0.7 if "negative" in category.value else 0.0,
            severity=severity,
            date=event_date,
            confidence=0.95,
            verified=True
        )]
    
    def run_single_backtest(self, player_name: str, game_data: Dict,
                            events: List[PlayerEvent]) -> BacktestResult:
        """
        Run backtest for a single game.
        
        Args:
            player_name: Player name
            game_data: Historical game performance data
            events: List of events leading up to the game
        
        Returns:
            BacktestResult
        """
        # Calculate PIS
        pis_result = calculate_impact_score(events)
        pis_score = pis_result["overall"]
        
        # Get baseline performance (player's season average)
        baseline_ppg = game_data.get("baseline_ppg", 20.0)
        
        # Project performance based on PIS
        # PIS 75 = baseline, PIS 50 = -15%, PIS 100 = +15%
        performance_multiplier = 0.70 + (pis_score / 250)  # 0.70 + (75/250) = 1.0
        projected_performance = baseline_ppg * performance_multiplier
        
        # Get actual performance
        actual_performance = game_data.get("points", 0)
        
        # Calculate error
        error = abs(projected_performance - actual_performance)
        
        # Check if PIS predicted direction correctly
        # (above or below baseline)
        actual_vs_baseline = actual_performance - baseline_ppg
        projected_vs_baseline = projected_performance - baseline_ppg
        
        prediction_correct = (actual_vs_baseline * projected_vs_baseline) > 0
        # If both positive or both negative, prediction was directionally correct
        
        return BacktestResult(
            player_name=player_name,
            game_date=game_data.get("game_date", ""),
            pis_score=pis_score,
            projected_performance=round(projected_performance, 1),
            actual_performance=actual_performance,
            error=round(error, 2),
            events_count=len(events),
            prediction_correct=prediction_correct
        )
    
    def run_player_backtest(self, player_name: str, 
                            inject_events: List[Tuple[str, str, str, float]] = None) -> List[BacktestResult]:
        """
        Run backtest for a player across multiple games.
        
        Args:
            player_name: Player to test
            inject_events: List of (event_type, date, description, severity) tuples
        
        Returns:
            List of BacktestResult
        """
        print(f"\n🏀 Backtesting {player_name}...")
        
        # Load historical data
        games = self.load_historical_data(player_name)
        
        # Create event timeline
        event_timeline = {}
        if inject_events:
            for event_type, date_str, desc, severity in inject_events:
                if date_str not in event_timeline:
                    event_timeline[date_str] = []
                event_timeline[date_str].extend(
                    self.create_historical_events(player_name, event_type, date_str, severity)
                )
        
        # Run backtest for each game
        results = []
        active_events = []
        
        for game in sorted(games, key=lambda x: x["game_date"]):
            game_date = game["game_date"]
            
            # Add any new events for this date
            if game_date in event_timeline:
                active_events.extend(event_timeline[game_date])
            
            # Remove events older than 60 days
            game_datetime = datetime.fromisoformat(game_date).replace(tzinfo=timezone.utc)
            active_events = [
                e for e in active_events 
                if (game_datetime - e.date).days <= 60
            ]
            
            # Run backtest
            result = self.run_single_backtest(player_name, game, active_events)
            results.append(result)
            
            # Store in database for analysis
            self.db.add_historical_performance(
                player_name=player_name,
                game_date=game_date,
                points=game["points"],
                rebounds=game.get("rebounds", 0),
                assists=game.get("assists", 0),
                pis_score=result.pis_score,
                events_count=len(active_events),
                opponent=game.get("opponent", "Unknown")
            )
        
        return results
    
    def calculate_summary(self, results: List[BacktestResult]) -> BacktestSummary:
        """Calculate summary statistics from backtest results."""
        if not results:
            return BacktestSummary(0, 0, 0, 0, 0, 0, [])
        
        errors = [r.error for r in results]
        pis_scores = [r.pis_score for r in results]
        actuals = [r.actual_performance for r in results]
        
        # Mean absolute error
        mae = statistics.mean(errors)
        
        # Correlation between PIS and actual performance
        if len(pis_scores) > 1:
            try:
                correlation = statistics.correlation(pis_scores, actuals)
            except:
                correlation = 0.0
        else:
            correlation = 0.0
        
        # Direction accuracy
        direction_correct = sum(1 for r in results if r.prediction_correct)
        direction_accuracy = direction_correct / len(results) if results else 0
        
        # High PIS accuracy (PIS > 85)
        high_pis = [r for r in results if r.pis_score > 85]
        high_pis_correct = sum(1 for r in high_pis if r.prediction_correct)
        high_pis_accuracy = high_pis_correct / len(high_pis) if high_pis else 0
        
        # Low PIS accuracy (PIS < 65)
        low_pis = [r for r in results if r.pis_score < 65]
        low_pis_correct = sum(1 for r in low_pis if r.prediction_correct)
        low_pis_accuracy = low_pis_correct / len(low_pis) if low_pis else 0
        
        return BacktestSummary(
            total_games=len(results),
            mean_absolute_error=round(mae, 2),
            correlation=round(correlation, 3),
            direction_accuracy=round(direction_accuracy, 3),
            high_pis_accuracy=round(high_pis_accuracy, 3),
            low_pis_accuracy=round(low_pis_accuracy, 3),
            results=results
        )
    
    def print_backtest_report(self, summary: BacktestSummary, player_name: str):
        """Print formatted backtest report."""
        print("\n" + "=" * 70)
        print(f"  BACKTEST REPORT: {player_name.upper()}")
        print("=" * 70)
        
        print(f"\n📊 Summary Statistics:")
        print(f"  Total Games Analyzed: {summary.total_games}")
        print(f"  Mean Absolute Error: {summary.mean_absolute_error} points")
        print(f"  PIS-Performance Correlation: {summary.correlation:.3f}")
        print(f"  Direction Accuracy: {summary.direction_accuracy:.1%}")
        
        print(f"\n🎯 High/Low PIS Performance:")
        print(f"  High PIS (>85) Accuracy: {summary.high_pis_accuracy:.1%}")
        print(f"  Low PIS (<65) Accuracy: {summary.low_pis_accuracy:.1%}")
        
        print(f"\n📋 Sample Results:")
        for r in summary.results[:5]:  # Show first 5
            status = "✅" if r.prediction_correct else "❌"
            print(f"  {status} {r.game_date}: PIS={r.pis_score:.1f}, "
                  f"Proj={r.projected_performance:.1f}, Actual={r.actual_performance:.1f}, "
                  f"Err={r.error:.1f}")
        
        print("=" * 70)
    
    def run_full_backtest(self, players: List[str]) -> Dict[str, BacktestSummary]:
        """Run backtest for multiple players."""
        all_summaries = {}
        
        for player in players:
            # Create some test events for demonstration
            test_events = [
                ("legal", "2024-11-15", "DUI arrest", 0.85),
                ("family", "2024-12-20", "Family emergency", 0.70),
            ]
            
            results = self.run_player_backtest(player, test_events)
            summary = self.calculate_summary(results)
            all_summaries[player] = summary
            
            self.print_backtest_report(summary, player)
        
        # Print overall summary
        print("\n" + "=" * 70)
        print("  OVERALL BACKTEST SUMMARY")
        print("=" * 70)
        
        total_games = sum(s.total_games for s in all_summaries.values())
        avg_mae = statistics.mean([s.mean_absolute_error for s in all_summaries.values()]) if all_summaries else 0
        avg_corr = statistics.mean([s.correlation for s in all_summaries.values()]) if all_summaries else 0
        avg_dir = statistics.mean([s.direction_accuracy for s in all_summaries.values()]) if all_summaries else 0
        
        print(f"\n📊 Across {len(players)} Players:")
        print(f"  Total Games: {total_games}")
        print(f"  Average MAE: {avg_mae:.2f} points")
        print(f"  Average Correlation: {avg_corr:.3f}")
        print(f"  Average Direction Accuracy: {avg_dir:.1%}")
        
        return all_summaries


# ========== DEMO ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — BACKTESTING SYSTEM DEMO")
    print("=" * 70)
    
    backtester = Backtester()
    
    # Test players
    players = [
        "Nikola Jokic",
        "LeBron James",
        "Jayson Tatum"
    ]
    
    print("\n🏀 Running backtests for test players...")
    print("(Using synthetic data - replace with real NBA historical data)")
    
    results = backtester.run_full_backtest(players)
    
    print("\n" + "=" * 70)
    print("  BACKTESTING DEMO COMPLETE")
    print("=" * 70)
    
    print("\n💡 Next Steps:")
    print("  1. Load real NBA historical data (2020-2025)")
    print("  2. Integrate real news events from historical archives")
    print("  3. Run full backtest on 5+ seasons of data")
    print("  4. Tune PIS weights based on correlation results")
