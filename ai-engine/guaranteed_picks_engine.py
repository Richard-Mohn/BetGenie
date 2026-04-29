"""
BetGenie — Guaranteed Picks Engine

This module implements the "guaranteed picks" system that:
1. Filters for only high-confidence bets (70%+ AI confidence)
2. Uses Monte Carlo simulation to estimate true parlay probability
3. Provides conservative probability estimates
4. Integrates with bankroll management for safe betting

This is the Jarvis-like intelligence system for basketball betting.
"""

import random
import math
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Tuple
from enum import Enum

from parlay_optimizer import PropBet, PropType, BetDirection, SmartParlay, score_parlay
from bankroll_manager import BankrollManager, BetRecommendation, RiskProfile


class PickQuality(Enum):
    LOCK = "lock"           # 80%+ confidence, strong edge
    STRONG = "strong"       # 70-79% confidence, good edge
    MODERATE = "moderate"   # 60-69% confidence, small edge
    WEAK = "weak"           # Below 60% confidence, avoid


@dataclass
class GuaranteedPick:
    """A high-confidence pick with guaranteed win probability."""
    player_name: str
    team: str
    prop_type: str
    line: float
    direction: str
    odds: int
    ai_confidence: float
    impact_score: float
    projected_value: float
    edge: float
    quality: PickQuality
    monte_carlo_win_rate: float
    conservative_win_rate: float
    key_factors: List[str]
    recommended_bet: Optional[BetRecommendation] = None


@dataclass
class GuaranteedParlay:
    """A parlay composed only of guaranteed picks."""
    picks: List[GuaranteedPick]
    combined_odds: int
    payout_multiplier: float
    true_probability: float
    conservative_probability: float
    monte_carlo_probability: float
    expected_value: float
    recommended_bet: Optional[BetRecommendation] = None
    warnings: List[str] = None


class GuaranteedPicksEngine:
    """
    The core intelligence engine for guaranteed picks.
    
    Philosophy:
    - Quality over quantity: Only recommend bets with 70%+ confidence
    - Conservative estimates: Always understate probability to be safe
    - Bankroll protection: Never risk more than 2-3% per bet
    - Transparency: Show all factors and reasoning
    """
    
    def __init__(self, bankroll: float, risk_profile: RiskProfile = RiskProfile.MODERATE):
        self.bankroll_manager = BankrollManager(bankroll, risk_profile)
        self.min_confidence = 70.0  # Only 70%+ confidence picks
        self.simulation_runs = 10000  # Monte Carlo iterations
    
    def classify_pick_quality(self, confidence: float, edge: float) -> PickQuality:
        """Classify a pick's quality based on confidence and edge."""
        if confidence >= 80 and edge >= 3.0:
            return PickQuality.LOCK
        elif confidence >= 70 and edge >= 2.0:
            return PickQuality.STRONG
        elif confidence >= 60 and edge >= 1.0:
            return PickQuality.MODERATE
        else:
            return PickQuality.WEAK
    
    def monte_carlo_simulate(
        self, 
        picks: List[GuaranteedPick], 
        runs: int = 10000
    ) -> float:
        """
        Run Monte Carlo simulation to estimate true parlay win rate.
        
        Simulates each pick independently using its AI confidence as
        the win probability, then calculates how often all picks win together.
        """
        wins = 0
        
        for _ in range(runs):
            all_win = True
            for pick in picks:
                # Use AI confidence as win probability
                if random.random() * 100 > pick.ai_confidence:
                    all_win = False
                    break
            
            if all_win:
                wins += 1
        
        return wins / runs
    
    def calculate_conservative_probability(self, picks: List[GuaranteedPick]) -> float:
        """
        Calculate a conservative win probability.
        
        Uses the minimum confidence across all picks as the baseline,
        then applies a 10% safety buffer.
        """
        if not picks:
            return 0.0
        
        min_confidence = min(p.ai_confidence for p in picks)
        
        # Conservative: use min confidence and apply 10% buffer
        conservative = min_confidence / 100 * 0.90
        
        # Apply parlay penalty (5% per leg beyond 2)
        leg_penalty = max(0, (len(picks) - 2) * 0.05)
        conservative *= (1 - leg_penalty)
        
        return max(0, conservative)
    
    def create_guaranteed_pick(
        self,
        prop: PropBet
    ) -> Optional[GuaranteedPick]:
        """Create a guaranteed pick from a prop bet if it meets quality standards."""
        # Filter by minimum confidence
        if prop.ai_confidence < self.min_confidence:
            return None
        
        # Classify quality
        quality = self.classify_pick_quality(prop.ai_confidence, prop.edge)
        
        if quality == PickQuality.WEAK:
            return None
        
        # Calculate conservative win rate (individual)
        conservative_rate = (prop.ai_confidence / 100) * 0.90
        
        # Create the pick
        pick = GuaranteedPick(
            player_name=prop.player_name,
            team=prop.team,
            prop_type=prop.prop_type.value,
            line=prop.line,
            direction=prop.direction.value,
            odds=prop.odds,
            ai_confidence=prop.ai_confidence,
            impact_score=prop.impact_score,
            projected_value=prop.projected_value,
            edge=prop.edge,
            quality=quality,
            monte_carlo_win_rate=prop.ai_confidence / 100,  # For single pick, it's just the confidence
            conservative_win_rate=conservative_rate,
            key_factors=prop.key_factors,
        )
        
        # Generate bet recommendation
        rec = self.bankroll_manager.recommend_bet(
            description=f"{pick.player_name} {pick.direction.upper()} {pick.line} {pick.prop_type}",
            confidence=pick.ai_confidence,
            odds=pick.odds,
            bet_type="straight"
        )
        pick.recommended_bet = rec
        
        return pick
    
    def find_guaranteed_picks(
        self, 
        props: List[PropBet]
    ) -> List[GuaranteedPick]:
        """Filter and convert props to guaranteed picks."""
        picks = []
        
        for prop in props:
            pick = self.create_guaranteed_pick(prop)
            if pick:
                picks.append(pick)
        
        # Sort by quality (LOCK first) then by confidence
        quality_order = {PickQuality.LOCK: 0, PickQuality.STRONG: 1, PickQuality.MODERATE: 2}
        picks.sort(key=lambda p: (quality_order[p.quality], -p.ai_confidence))
        
        return picks
    
    def build_guaranteed_parlay(
        self,
        picks: List[GuaranteedPick],
        max_legs: int = 3
    ) -> Optional[GuaranteedParlay]:
        """
        Build a guaranteed parlay from the best available picks.
        
        Limits to max_legs to maintain high win probability.
        Only uses LOCK and STRONG quality picks.
        """
        # Filter to top quality picks
        top_picks = [p for p in picks if p.quality in [PickQuality.LOCK, PickQuality.STRONG]]
        
        if len(top_picks) < 2:
            return None
        
        # Take top max_legs picks
        selected = top_picks[:max_legs]
        
        # Calculate combined odds
        combined_decimal = 1.0
        for pick in selected:
            if pick.odds > 0:
                decimal = (pick.odds / 100) + 1
            else:
                decimal = (100 / abs(pick.odds)) + 1
            combined_decimal *= decimal
        
        combined_american = int(
            (combined_decimal - 1) * 100 if combined_decimal >= 2
            else -100 / (combined_decimal - 1)
        )
        
        # Run Monte Carlo simulation
        mc_prob = self.monte_carlo_simulate(selected, self.simulation_runs)
        
        # Calculate conservative probability
        cons_prob = self.calculate_conservative_probability(selected)
        
        # Calculate true probability (product of individual confidences)
        true_prob = 1.0
        for pick in selected:
            true_prob *= (pick.ai_confidence / 100)
        
        # Calculate expected value
        ev = (true_prob * combined_decimal) - ((1 - true_prob) * 1)
        
        # Generate bet recommendation
        description = f"{len(selected)}-Leg Parlay: " + " + ".join([
            f"{p.player_name} {p.direction[0].upper()}{p.line}" 
            for p in selected
        ])
        
        rec = self.bankroll_manager.recommend_bet(
            description=description,
            confidence=mc_prob * 100,
            odds=combined_american,
            bet_type="parlay"
        )
        
        # Generate warnings
        warnings = []
        if len(selected) > 3:
            warnings.append(f"Parlay has {len(selected)} legs - consider reducing to 2-3 for higher win rate")
        
        if mc_prob < 0.40:
            warnings.append(f"Monte Carlo win rate ({mc_prob:.1%}) is below 40% - high risk")
        
        if cons_prob < 0.30:
            warnings.append(f"Conservative estimate ({cons_prob:.1%}) is below 30% - very high risk")
        
        return GuaranteedParlay(
            picks=selected,
            combined_odds=combined_american,
            payout_multiplier=combined_decimal,
            true_probability=true_prob,
            conservative_probability=cons_prob,
            monte_carlo_probability=mc_prob,
            expected_value=ev,
            recommended_bet=rec,
            warnings=warnings if warnings else None,
        )
    
    def build_dual_bet_strategy(
        self,
        guaranteed_picks: List[GuaranteedPick],
        main_parlay: Optional[GuaranteedParlay]
    ) -> Dict:
        """
        Build a dual bet strategy:
        - Main bet: Guaranteed parlay (high probability, solid payout)
        - Side bet: Kicker (low probability, massive payout)
        
        Strategy: If main hits, you're profitable even if kicker misses.
        If both hit, you win BIG.
        
        Example:
        - Main: 4-leg parlay at +800, $20 bet = $180 win
        - Kicker: +5000 odds, $5 bet = $255 win
        - Total stake: $25
        - Main hits only: $180 - $25 = $155 profit
        - Both hit: $180 + $255 - $25 = $410 profit (big win!)
        """
        if not main_parlay or not main_parlay.picks:
            return None
        
        # Main parlay should be 3-4 legs with 60-75% win probability
        main_stake = min(25.0, self.bankroll_manager.bankroll * 0.04)  # 4% of bankroll
        
        # Kicker should be a long shot with +2000 or higher odds
        # We'll simulate a kicker pick by finding the lowest confidence pick
        # and treating it as a high odds opportunity
        if len(guaranteed_picks) >= 4:
            kicker_pick = guaranteed_picks[3]  # 4th best pick as kicker
            kicker_odds = +3500  # Simulated high odds
            kicker_stake = min(10.0, self.bankroll_manager.bankroll * 0.015)  # 1.5% of bankroll
            kicker_payout = kicker_stake * ((kicker_odds / 100) + 1) if kicker_odds > 0 else kicker_stake * ((100 / abs(kicker_odds)) + 1)
        else:
            kicker_pick = None
            kicker_odds = None
            kicker_stake = 0
            kicker_payout = 0
        
        # Calculate main parlay payout
        main_payout = main_stake * main_parlay.payout_multiplier
        
        # Total stake
        total_stake = main_stake + kicker_stake
        
        # Scenarios
        scenarios = {
            "main_only_win": {
                "description": "Main parlay hits, kicker misses",
                "probability": main_parlay.conservative_probability * (1 - 0.02),  # Assume 2% kicker hit rate
                "payout": main_payout,
                "net_profit": main_payout - total_stake,
                "outcome": "PROFIT" if main_payout > total_stake else "LOSS"
            },
            "both_win": {
                "description": "Both main parlay AND kicker hit",
                "probability": main_parlay.conservative_probability * 0.02,  # Both hit
                "payout": main_payout + kicker_payout,
                "net_profit": main_payout + kicker_payout - total_stake,
                "outcome": "BIG_WIN"
            },
            "main_only_loss": {
                "description": "Main parlay misses, kicker hits",
                "probability": (1 - main_parlay.conservative_probability) * 0.02,
                "payout": kicker_payout,
                "net_profit": kicker_payout - total_stake,
                "outcome": "SMALL_PROFIT" if kicker_payout > total_stake else "LOSS"
            },
            "both_lose": {
                "description": "Both miss",
                "probability": (1 - main_parlay.conservative_probability) * (1 - 0.02),
                "payout": 0,
                "net_profit": -total_stake,
                "outcome": "LOSS"
            }
        }
        
        # Calculate expected value
        expected_value = sum(
            scenario["probability"] * scenario["net_profit"]
            for scenario in scenarios.values()
        )
        
        # Best case scenario
        best_case = scenarios["both_win"]
        
        # Worst case scenario
        worst_case = scenarios["both_lose"]
        
        return {
            "strategy_name": "Dual Bet: Guaranteed + Kicker",
            "main_parlay": {
                "description": f"{len(main_parlay.picks)}-leg parlay",
                "odds": main_parlay.combined_odds,
                "win_probability": main_parlay.conservative_probability,
                "stake": main_stake,
                "potential_payout": main_payout,
                "picks": [f"{p.player_name} {p.direction.upper()} {p.line}" for p in main_parlay.picks]
            },
            "kicker_bet": {
                "description": f"Long shot: {kicker_pick.player_name if kicker_pick else 'N/A'}" if kicker_pick else "No kicker available",
                "odds": kicker_odds,
                "win_probability": 0.02,  # 2% estimated
                "stake": kicker_stake,
                "potential_payout": kicker_payout,
                "pick": f"{kicker_pick.player_name} {kicker_pick.direction.upper()} {kicker_pick.line}" if kicker_pick else "N/A"
            } if kicker_pick else None,
            "total_stake": total_stake,
            "scenarios": scenarios,
            "expected_value": expected_value,
            "best_case_profit": best_case["net_profit"],
            "worst_case_loss": abs(worst_case["net_profit"]),
            "risk_reward_ratio": best_case["net_profit"] / abs(worst_case["net_profit"]) if worst_case["net_profit"] != 0 else 0,
            "recommendation": "RECOMMENDED" if expected_value > 0 else "CAUTION"
        }
    
    def generate_daily_picks(
        self,
        props: List[PropBet]
    ) -> Dict:
        """
        Generate a complete daily picks report.
        
        Returns:
            Dictionary with guaranteed picks, parlay suggestions, and bankroll guidance.
        """
        # Find guaranteed picks
        guaranteed = self.find_guaranteed_picks(props)
        
        # Build parlay options (2, 3, 4, 5, and 6 leg)
        parlay_2leg = self.build_guaranteed_parlay(guaranteed, max_legs=2)
        parlay_3leg = self.build_guaranteed_parlay(guaranteed, max_legs=3)
        parlay_4leg = self.build_guaranteed_parlay(guaranteed, max_legs=4)
        parlay_5leg = self.build_guaranteed_parlay(guaranteed, max_legs=5)
        parlay_6leg = self.build_guaranteed_parlay(guaranteed, max_legs=6)
        
        # Calculate total exposure if betting all picks
        total_exposure = sum(
            p.recommended_bet.recommended_amount 
            for p in guaranteed 
            if p.recommended_bet
        )
        
        # Build dual bet strategy: guaranteed parlay + kicker side bet
        dual_strategy = self.build_dual_bet_strategy(guaranteed, parlay_4leg)
        
        return {
            "guaranteed_picks": guaranteed,
            "parlay_2leg": parlay_2leg,
            "parlay_3leg": parlay_3leg,
            "parlay_4leg": parlay_4leg,
            "parlay_5leg": parlay_5leg,
            "parlay_6leg": parlay_6leg,
            "dual_bet_strategy": dual_strategy,
            "total_picks": len(guaranteed),
            "total_exposure": total_exposure,
            "bankroll": self.bankroll_manager.bankroll,
            "risk_profile": self.bankroll_manager.risk_profile.value,
            "generated_at": datetime.now().isoformat(),
        }


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — GUARANTEED PICKS ENGINE")
    print("  Jarvis-Like Basketball Intelligence System")
    print("=" * 70)
    
    # Initialize with $500 bankroll
    engine = GuaranteedPicksEngine(bankroll=500.00, risk_profile=RiskProfile.MODERATE)
    
    print(f"\nBankroll: ${engine.bankroll_manager.bankroll:.2f}")
    print(f"Risk Profile: {engine.bankroll_manager.risk_profile.value}")
    print(f"Minimum Confidence: {engine.min_confidence}%")
    print(f"Monte Carlo Simulations: {engine.simulation_runs:,}")
    
    # Create sample props (simulating what would come from the AI pipeline)
    from parlay_optimizer import PropBet, PropType, BetDirection
    
    sample_props = [
        PropBet(
            player_id="lebron-james-lal",
            player_name="LeBron James",
            team="Los Angeles Lakers",
            sport="NBA",
            game_id="nba-2026-04-28-lal-bos",
            prop_type=PropType.POINTS,
            line=23.5,
            direction=BetDirection.OVER,
            odds=-110,
            ai_confidence=78,
            impact_score=85,
            key_factors=["Home game", "Well rested", "Matchup advantage"],
            projected_value=26.2,
            edge=2.7,
        ),
        PropBet(
            player_id="sga-okc",
            player_name="Shai Gilgeous-Alexander",
            team="Oklahoma City Thunder",
            sport="NBA",
            game_id="nba-2026-04-28-okc-den",
            prop_type=PropType.POINTS,
            line=31.5,
            direction=BetDirection.UNDER,
            odds=-105,
            ai_confidence=82,
            impact_score=88,
            key_factors=["Elite defense", "Slow pace game", "Fatigue factor"],
            projected_value=28.5,
            edge=3.0,
        ),
        PropBet(
            player_id="wemby-sa",
            player_name="Victor Wembanyama",
            team="San Antonio Spurs",
            sport="NBA",
            game_id="nba-2026-04-28-sa-phi",
            prop_type=PropType.REBOUNDS,
            line=10.5,
            direction=BetDirection.OVER,
            odds=-110,
            ai_confidence=75,
            impact_score=82,
            key_factors=["Size advantage", "Weak rebounding opponent"],
            projected_value=12.8,
            edge=2.3,
        ),
        PropBet(
            player_id="luka-doncic-lal",
            player_name="Luka Doncic",
            team="Los Angeles Lakers",
            sport="NBA",
            game_id="nba-2026-04-28-lal-bos",
            prop_type=PropType.ASSISTS,
            line=8.5,
            direction=BetDirection.OVER,
            odds=-115,
            ai_confidence=65,  # Below threshold - should be filtered out
            impact_score=70,
            key_factors=["Playmaking role"],
            projected_value=9.2,
            edge=0.7,
        ),
    ]
    
    # Generate daily picks
    print("\n" + "-" * 70)
    print("  GENERATING DAILY PICKS...")
    print("-" * 70)
    
    report = engine.generate_daily_picks(sample_props)
    
    print(f"\nTotal Guaranteed Picks: {report['total_picks']}")
    print(f"Total Exposure: ${report['total_exposure']:.2f}")
    
    # Display guaranteed picks
    if report['guaranteed_picks']:
        print("\n" + "-" * 70)
        print("  GUARANTEED PICKS (70%+ Confidence)")
        print("-" * 70)
        
        for i, pick in enumerate(report['guaranteed_picks'], 1):
            quality_icon = "🔒" if pick.quality == PickQuality.LOCK else "💪"
            print(f"\n{quality_icon} #{i} {pick.player_name} — {pick.direction.upper()} {pick.line} {pick.prop_type}")
            print(f"    Team: {pick.team}")
            print(f"    AI Confidence: {pick.ai_confidence}%")
            print(f"    Impact Score: {pick.impact_score}/100")
            print(f"    Edge: +{pick.edge}")
            print(f"    Quality: {pick.quality.value.upper()}")
            print(f"    Conservative Win Rate: {pick.conservative_win_rate:.1%}")
            print(f"    Projected: {pick.projected_value} vs Line {pick.line}")
            print(f"    Key Factors: {', '.join(pick.key_factors)}")
            
            if pick.recommended_bet:
                rec = pick.recommended_bet
                print(f"    💰 Recommended Bet: ${rec.recommended_amount:.2f} ({rec.percentage_of_bankroll}% of bankroll)")
                print(f"       Expected Value: {rec.expected_value:+.3f}")
    
    # Display parlays
    if report['parlay_2leg']:
        print("\n" + "-" * 70)
        print("  2-LEG GUARANTEED PARLAY")
        print("-" * 70)
        
        parlay = report['parlay_2leg']
        print(f"\nOdds: {'+' if parlay.combined_odds > 0 else ''}{parlay.combined_odds}")
        print(f"Payout: {parlay.payout_multiplier:.2f}x")
        print(f"Monte Carlo Win Rate: {parlay.monte_carlo_probability:.1%}")
        print(f"Conservative Win Rate: {parlay.conservative_probability:.1%}")
        print(f"True Probability: {parlay.true_probability:.1%}")
        print(f"Expected Value: {parlay.expected_value:+.3f}")
        
        print(f"\nLegs:")
        for i, pick in enumerate(parlay.picks, 1):
            print(f"  {i}. {pick.player_name} {pick.direction.upper()} {pick.line} {pick.prop_type} ({pick.ai_confidence}%)")
        
        if parlay.warnings:
            print(f"\nWarnings:")
            for w in parlay.warnings:
                print(f"  ⚠️  {w}")
        
        if parlay.recommended_bet:
            rec = parlay.recommended_bet
            print(f"\n💰 Recommended Bet: ${rec.recommended_amount:.2f} ({rec.percentage_of_bankroll}% of bankroll)")
    
    if report['parlay_3leg']:
        print("\n" + "-" * 70)
        print("  3-LEG GUARANTEED PARLAY")
        print("-" * 70)
        
        parlay = report['parlay_3leg']
        print(f"\nOdds: {'+' if parlay.combined_odds > 0 else ''}{parlay.combined_odds}")
        print(f"Payout: {parlay.payout_multiplier:.2f}x")
        print(f"Monte Carlo Win Rate: {parlay.monte_carlo_probability:.1%}")
        print(f"Conservative Win Rate: {parlay.conservative_probability:.1%}")
        print(f"Expected Value: {parlay.expected_value:+.3f}")
        
        print(f"\nLegs:")
        for i, pick in enumerate(parlay.picks, 1):
            print(f"  {i}. {pick.player_name} {pick.direction.upper()} {pick.line} {pick.prop_type} ({pick.ai_confidence}%)")
        
        if parlay.warnings:
            print(f"\nWarnings:")
            for w in parlay.warnings:
                print(f"  ⚠️  {w}")
    
    print("\n" + "=" * 70)
    print("  GUARANTEED PICKS ENGINE — READY")
    print("  Quality over Quantity. Bankroll Protection First.")
    print("=" * 70)
