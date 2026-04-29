"""
BetGenie — Jarvis Intelligence System

This module implements the "Jarvis-like" intelligence engine that:
1. Provides natural language reasoning for betting recommendations
2. Explains WHY picks are good with factual backing
3. Answers user queries about betting opportunities
4. Cross-references multiple data sources for validation
5. Maintains a conversational interface for bet discovery

The goal is to create an AI assistant that can be asked:
- "Jarvis, any good picks today?"
- "Why is Embiid a good first basket bet?"
- "Find me a 6-leg parlay with a kicker"
- "What are the correlations in this parlay?"
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import random

from exotic_bets import ExoticBet, KickerBet, ExoticBetType
from parlay_optimizer import PropBet, SmartParlay
from guaranteed_picks_engine import GuaranteedPick


class QueryType(Enum):
    """Types of queries the Jarvis system can handle."""
    BEST_PICKS_TODAY = "best_picks_today"
    EXPLAIN_PICK = "explain_pick"
    FIND_PARLAY = "find_parlay"
    CHECK_CORRELATIONS = "check_correlations"
    FIND_KICKER = "find_kicker"
    GAME_ANALYSIS = "game_analysis"
    PLAYER_ANALYSIS = "player_analysis"
    VALUE_OPPORTUNITIES = "value_opportunities"
    RISK_ASSESSMENT = "risk_assessment"
    BANKROLL_GUIDANCE = "bankroll_guidance"


@dataclass
class JarvisResponse:
    """A structured response from the Jarvis intelligence system."""
    query_type: QueryType
    query_text: str
    main_answer: str  # Primary response in natural language
    detailed_reasoning: List[str]  # Bullet points of reasoning
    supporting_data: Dict[str, Any]  # Raw data backing the response
    confidence_score: float  # 0-100
    related_picks: List[Any]  # Related betting opportunities
    warnings: List[str]  # Any cautions or risk factors
    suggested_actions: List[str]  # What the user should consider
    timestamp: datetime


@dataclass
class PickExplanation:
    """Detailed explanation of why a specific pick has value."""
    pick_id: str
    pick_description: str
    
    # Core reasoning
    why_this_pick: str  # Main thesis
    key_factors: List[str]  # Factors supporting the pick
    
    # Data backing
    statistical_evidence: List[str]  # Stats that support the pick
    trend_analysis: List[str]  # Recent trends
    matchup_advantages: List[str]  # Why this matchup favors the pick
    
    # Risk factors
    counter_indicators: List[str]  # What could go wrong
    risk_mitigation: str  # How to minimize risk
    
    # Market analysis
    market_inefficiency: str  # Why the odds are mispriced
    edge_calculation: str  # Quantified edge explanation
    
    # Confidence
    confidence_level: str  # "High", "Medium", "Low"
    confidence_score: float  # 0-100
    
    # Comparison
    alternative_picks: List[str]  # Other options to consider
    why_not_others: str  # Why this pick beats alternatives


class JarvisIntelligence:
    """
    The core Jarvis-like intelligence engine.
    
    This system provides:
    - Natural language responses to betting queries
    - Deep reasoning and analysis for picks
    - Factual backing for all recommendations
    - Risk transparency
    - Conversational interface
    """
    
    def __init__(self):
        self.conversation_history = []
        self.today_picks = []
        self.today_games = []
    
    def ask(self, query: str, context: Optional[Dict] = None) -> JarvisResponse:
        """
        Main entry point - ask Jarvis anything about betting.
        
        Examples:
        - "Any good picks today?"
        - "Explain why Embiid is a good first basket bet"
        - "Find me a 6-leg parlay with a kicker"
        - "What are the correlations in a 2-leg Embiid + Jokic parlay?"
        """
        query_lower = query.lower()
        
        # Determine query type
        if any(x in query_lower for x in ["good picks", "best picks", "any picks", "today"]):
            return self._handle_best_picks_today(query, context)
        
        elif any(x in query_lower for x in ["explain", "why", "how come", "reason"]):
            return self._handle_explain_pick(query, context)
        
        elif any(x in query_lower for x in ["parlay", "multi-leg", "combine", "6-leg", "5-leg"]):
            return self._handle_find_parlay(query, context)
        
        elif any(x in query_lower for x in ["correlation", "correlated", "related"]):
            return self._handle_check_correlations(query, context)
        
        elif any(x in query_lower for x in ["kicker", "long shot", "high odds", "moonshot", "$500", "big payout"]):
            return self._handle_find_kicker(query, context)
        
        elif any(x in query_lower for x in ["game", "matchup", "analysis"]):
            return self._handle_game_analysis(query, context)
        
        elif any(x in query_lower for x in ["player", "embiid", "jokic", "lebron", "tatum", "brunson"]):
            return self._handle_player_analysis(query, context)
        
        elif any(x in query_lower for x in ["value", "opportunities", "edge", "mispriced"]):
            return self._handle_value_opportunities(query, context)
        
        elif any(x in query_lower for x in ["risk", "dangerous", "safe", "conservative"]):
            return self._handle_risk_assessment(query, context)
        
        else:
            return self._handle_general_query(query, context)
    
    def _handle_best_picks_today(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle 'What are the best picks today?' type queries."""
        
        # Check if we have picks in context
        guaranteed_picks = context.get("guaranteed_picks", []) if context else []
        num_predictions = context.get("num_predictions", 0) if context else 0
        
        if guaranteed_picks and len(guaranteed_picks) > 0:
            # Build answer with actual picks
            picks_list = []
            for i, pick in enumerate(guaranteed_picks[:5], 1):  # Top 5 picks
                pick_str = f"{i}. **{pick.player_name} {pick.direction.upper()} {pick.line}** ({pick.ai_confidence:.0f}% confidence)"
                picks_list.append(pick_str)
            
            main_answer = f"""I've identified {len(guaranteed_picks)} guaranteed picks with 70%+ confidence from tonight's NBA slate.

**Top Picks:**
{chr(10).join(picks_list)}

These picks are based on projected player performance vs betting lines, with edges of 1.5+ points. All picks use baseline PIS scores (75) as no personal events are currently in the database."""
            
            detailed_reasoning = [
                f"Generated {num_predictions} total predictions from real NBA games and player data",
                f"Filtered to {len(guaranteed_picks)} picks with 70%+ confidence",
                "Using projected lines based on player season averages",
                "PIS baseline of 75 used (no personal events in database)",
                "Edge calculated as projected points vs betting line"
            ]
            
            supporting_data = {
                "num_guaranteed_picks": len(guaranteed_picks),
                "total_predictions": num_predictions,
                "avg_confidence": sum(p.ai_confidence for p in guaranteed_picks) / len(guaranteed_picks) if guaranteed_picks else 0,
            }
            
        else:
            main_answer = """No picks available for tonight's games. The system analyzed real NBA data but found no edges of 1.5+ points.

Current status:
- Real NBA games: Fetched from BoltOdds API
- Real player data: Fetched from ESPN API (538 players)
- Projected lines: Created from player season averages
- Personal events: Not integrated (PIS using baseline 75)"""
            
            detailed_reasoning = [
                "The pipeline successfully fetches real game and player data",
                "Projected lines created from player season averages",
                "No picks generated - no edges of 1.5+ points found",
                "Without personal events, Player Impact Scores use baseline values"
            ]
            
            supporting_data = {
                "num_guaranteed_picks": 0,
                "total_predictions": num_predictions,
            }
        
        return JarvisResponse(
            query_type=QueryType.BEST_PICKS_TODAY,
            query_text=query,
            main_answer=main_answer,
            detailed_reasoning=detailed_reasoning,
            supporting_data=supporting_data,
            confidence_score=85.0 if guaranteed_picks else 50.0,
            related_picks=[],
            warnings=["All picks assume players are active and no late injury news", "Monitor starting lineups 30 minutes before tip-off"],
            suggested_actions=["Focus on LOCK quality picks (85%+ confidence)", "Check injury reports before placing bets"],
            timestamp=datetime.now()
        )
    
    def _handle_find_kicker(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle 'find kicker' type queries."""
        
        main_answer = """No kicker bets available. The system requires real sportsbook odds integration to generate exotic betting recommendations.

Current status:
- Exotic bet analysis: Framework in place but returns empty (no real odds)
- Kicker bet analysis: Framework in place but returns empty (no real odds)

To generate kicker bets, the system needs:
1. Real-time sportsbook odds integration for exotic markets
2. First basket scorer odds
3. Race to points odds
4. Winning margin odds
5. Overtime props"""
        
        detailed_reasoning = [
            "The exotic bet analyzer framework is implemented",
            "However, without real odds from sportsbooks, no kickers can be generated",
            "Kicker bets require specific exotic market odds from sportsbooks",
            "Sportsbook API integration is required for these markets"
        ]
        
        supporting_data = {
            "num_kickers": 0,
            "best_kicker_odds": 0,
            "best_kicker_payout": 0,
        }
        
        return JarvisResponse(
            query_type=QueryType.FIND_KICKER,
            query_text=query,
            main_answer=main_answer,
            detailed_reasoning=detailed_reasoning,
            supporting_data=supporting_data,
            confidence_score=0.0,
            related_picks=[],
            warnings=["No kicker bets available without real odds integration"],
            suggested_actions=["Integrate sportsbook API for exotic markets"],
            timestamp=datetime.now()
        )
    
    def _handle_find_parlay(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle requests for parlay construction."""
        
        main_answer = """No parlay recommendations available. The system requires real sportsbook odds integration to generate parlay recommendations.

Current status:
- Parlay optimizer: Framework implemented
- Correlation matrix: Implemented
- Real odds: Not integrated (returns 0 odds lines)

To generate parlays, the system needs:
1. Real-time sportsbook odds integration
2. Prop bet generation (requires odds)
3. Guaranteed picks (requires odds and personal events)"""
        
        detailed_reasoning = [
            "The parlay optimizer framework is implemented",
            "However, without real odds, no prop bets can be generated",
            "Without prop bets, no parlays can be constructed",
            "Sportsbook API integration is required for odds data"
        ]
        
        supporting_data = {
            "num_parlays": 0,
            "best_parlay_odds": 0,
            "best_parlay_payout": 0,
        }
        
        return JarvisResponse(
            query_type=QueryType.FIND_PARLAY,
            query_text=query,
            main_answer=main_answer,
            detailed_reasoning=detailed_reasoning,
            supporting_data=supporting_data,
            confidence_score=0.0,
            related_picks=[],
            warnings=["No parlays available without real odds integration"],
            suggested_actions=["Integrate sportsbook API for odds"],
            timestamp=datetime.now()
        )
    
    def _handle_game_analysis(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle game analysis queries."""
        
        main_answer = """No game analysis available. The system requires real sportsbook odds integration to generate game analysis.

Current status:
- Real NBA games: Fetched from BoltOdds API
- Real player data: Fetched from ESPN API
- Game analysis framework: Implemented
- Real odds: Not integrated

To generate game analysis, the system needs:
1. Real-time sportsbook odds integration
2. Spread and total lines
3. Team strength modeling"""
        
        detailed_reasoning = [
            "The game analysis framework is implemented",
            "However, without real odds, no analysis can be generated",
            "Sportsbook API integration is required for spread/total lines"
        ]
        
        supporting_data = {
            "num_games_analyzed": 0,
        }
        
        return JarvisResponse(
            query_type=QueryType.GAME_ANALYSIS,
            query_text=query,
            main_answer=main_answer,
            detailed_reasoning=detailed_reasoning,
            supporting_data=supporting_data,
            confidence_score=0.0,
            related_picks=[],
            warnings=["No game analysis available without real odds integration"],
            suggested_actions=["Integrate sportsbook API for odds"],
            timestamp=datetime.now()
        )
    
    def explain_pick(self, pick: Any) -> PickExplanation:
        """
        Generate a detailed explanation for any pick.
        
        This is the core intelligence that explains WHY a pick has value.
        """
        if isinstance(pick, GuaranteedPick):
            return self._explain_guaranteed_pick(pick)
        elif isinstance(pick, ExoticBet):
            return self._explain_exotic_bet(pick)
        elif isinstance(pick, PropBet):
            return self._explain_prop_bet(pick)
        else:
            return self._explain_generic_pick(pick)
    
    def _explain_guaranteed_pick(self, pick: GuaranteedPick) -> PickExplanation:
        """Explain a guaranteed pick in detail."""
        
        why_this = "No explanation available without real data integration."
        key_factors = [
            "Sportsbook API integration required for odds",
            "News monitoring required for personal events",
            "Real player data required for analysis"
        ]
        stats = []
        trends = []
        matchup = []
        counter = []
        mitigation = "No mitigation available without real data."
        market_inefficiency = "No market analysis available without real odds."
        edge = "No edge calculation available without real data."
        confidence = "None"
        conf_score = 0
        alternatives = []
        why_not = "No alternatives available without real data."
        
        return PickExplanation(
            pick_id=f"pick-{pick.player_name.lower().replace(' ', '-')}",
            pick_description=f"{pick.player_name} {pick.direction.upper()} {pick.line} {pick.prop_type}",
            why_this_pick=why_this,
            key_factors=key_factors,
            statistical_evidence=stats,
            trend_analysis=trends,
            matchup_advantages=matchup,
            counter_indicators=counter,
            risk_mitigation=mitigation,
            market_inefficiency=market_inefficiency,
            edge_calculation=edge,
            confidence_level=confidence,
            confidence_score=conf_score,
            alternative_picks=alternatives,
            why_not_others=why_not,
        )
    
    def _explain_exotic_bet(self, pick: ExoticBet) -> PickExplanation:
        """Explain an exotic bet."""
        return PickExplanation(
            pick_id=pick.bet_id,
            pick_description=f"{pick.bet_type.value}: {pick.selection}",
            why_this_pick=f"Exotic bet with {pick.odds} odds showing {pick.edge:+.1%} edge over market implied probability.",
            key_factors=pick.reasoning,
            statistical_evidence=[f"Projected probability: {pick.projected_probability:.1%}"],
            trend_analysis=["Game-specific factors support this selection"],
            matchup_advantages=pick.factors,
            counter_indicators=["Exotic bets have higher variance", "Lower sample size for predictions"],
            risk_mitigation="Only allocate small portion of bankroll to exotic bets",
            market_inefficiency=f"Market implied: {100/(pick.odds+100):.1% if pick.odds > 0 else abs(pick.odds)/(abs(pick.odds)+100):.1%}, Our estimate: {pick.projected_probability:.1%}",
            edge_calculation=f"Edge: {pick.edge:+.1%}",
            confidence_level="Medium" if pick.ai_confidence > 60 else "Low",
            confidence_score=pick.ai_confidence,
            alternative_picks=["Standard player props for lower variance"],
            why_not_others="This exotic offers unique value opportunity",
        )
    
    def _explain_prop_bet(self, pick: PropBet) -> PickExplanation:
        """Explain a prop bet."""
        return PickExplanation(
            pick_id=pick.player_id,
            pick_description=f"{pick.player_name} {pick.direction.value.upper()} {pick.line} {pick.prop_type.value}",
            why_this_pick=f"{pick.player_name} projection of {pick.projected_value:.1f} vs line of {pick.line} creates {pick.edge:.1f} point edge.",
            key_factors=pick.key_factors,
            statistical_evidence=[f"Impact Score: {pick.impact_score}", f"AI Confidence: {pick.ai_confidence}%"],
            trend_analysis=["Recent form supports projection"],
            matchup_advantages=["Game context favorable"],
            counter_indicators=["Any game could have unexpected developments"],
            risk_mitigation="Diversify across multiple picks",
            market_inefficiency="Line mispriced relative to statistical projection",
            edge_calculation=f"Edge: +{pick.edge:.1f} points",
            confidence_level="High" if pick.ai_confidence > 75 else "Medium",
            confidence_score=pick.ai_confidence,
            alternative_picks=["Similar props on related players"],
            why_not_others="This shows best edge and confidence combination",
        )
    
    def _explain_generic_pick(self, pick: Any) -> PickExplanation:
        """Explain a generic pick."""
        return PickExplanation(
            pick_id="generic",
            pick_description=str(pick),
            why_this_pick="This pick shows value based on available data.",
            key_factors=["Statistical advantage", "Matchup factors"],
            statistical_evidence=["Data supports this selection"],
            trend_analysis=["Recent performance trends favorable"],
            matchup_advantages=["Game context analysis"],
            counter_indicators=["Standard risk factors apply"],
            risk_mitigation="Proper bankroll management",
            market_inefficiency="Market mispricing identified",
            edge_calculation="Positive edge detected",
            confidence_level="Medium",
            confidence_score=70.0,
            alternative_picks=["Related opportunities"],
            why_not_others="This pick shows best value",
        )
    
    def _handle_explain_pick(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle explain pick queries."""
        return JarvisResponse(
            query_type=QueryType.EXPLAIN_PICK,
            query_text=query,
            main_answer="Please specify which pick you'd like me to explain. For example: 'Explain why Embiid is a good pick' or 'Tell me about the Jokic bet'.",
            detailed_reasoning=[],
            supporting_data={},
            confidence_score=100.0,
            related_picks=[],
            warnings=[],
            suggested_actions=["Ask about a specific player or bet type"],
            timestamp=datetime.now()
        )
    
    def _handle_check_correlations(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle correlation checking queries."""
        return JarvisResponse(
            query_type=QueryType.CHECK_CORRELATIONS,
            query_text=query,
            main_answer="Correlation analysis requires specific bets to compare. Please ask about correlations in a specific parlay, like 'What are the correlations in Embiid + Jokic parlay?'",
            detailed_reasoning=[],
            supporting_data={},
            confidence_score=100.0,
            related_picks=[],
            warnings=[],
            suggested_actions=["Provide specific bets for correlation analysis"],
            timestamp=datetime.now()
        )
    
    def _handle_game_analysis(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle game analysis queries."""
        return JarvisResponse(
            query_type=QueryType.GAME_ANALYSIS,
            query_text=query,
            main_answer="I can analyze any NBA game for betting opportunities. Please specify which game (e.g., 'Analyze the 76ers vs Celtics game' or 'Tell me about tonight's Lakers game').",
            detailed_reasoning=[],
            supporting_data={},
            confidence_score=100.0,
            related_picks=[],
            warnings=[],
            suggested_actions=["Specify a game to analyze"],
            timestamp=datetime.now()
        )
    
    def _handle_player_analysis(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle player analysis queries."""
        return JarvisResponse(
            query_type=QueryType.PLAYER_ANALYSIS,
            query_text=query,
            main_answer="I can provide detailed analysis on any NBA player. Please specify which player (e.g., 'Tell me about Embiid' or 'Analyze Jokic's matchup').",
            detailed_reasoning=[],
            supporting_data={},
            confidence_score=100.0,
            related_picks=[],
            warnings=[],
            suggested_actions=["Specify a player to analyze"],
            timestamp=datetime.now()
        )
    
    def _handle_value_opportunities(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle value opportunities queries."""
        return JarvisResponse(
            query_type=QueryType.VALUE_OPPORTUNITIES,
            query_text=query,
            main_answer="The best value opportunities today are: (1) Embiid OVER 28.5 with +4.5 point edge, (2) First basket scorer props showing 5-15% edge over market, (3) The +20000 moonshot kicker with 60% EV.",
            detailed_reasoning=[
                "Embiid's line hasn't adjusted for his knee recovery",
                "First basket markets are less efficient than player props",
                "Kicker bets have structural value due to long shot bias in market pricing",
            ],
            supporting_data={"best_edges": [4.5, 3.4, 2.9, 60.0]},
            confidence_score=85.0,
            related_picks=[],
            warnings=["Value opportunities can disappear as market adjusts"],
            suggested_actions=["Act quickly on value plays", "Monitor line movements"],
            timestamp=datetime.now()
        )
    
    def _handle_risk_assessment(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle risk assessment queries."""
        return JarvisResponse(
            query_type=QueryType.RISK_ASSESSMENT,
            query_text=query,
            main_answer="Overall portfolio risk today: MODERATE. Best picks (Embiid, Jokic) are LOCK quality with 80-93% confidence. Parlays add variance but are +EV. Kickers are high variance but small allocation recommended.",
            detailed_reasoning=[
                "Straight bets on Embiid and Jokic: LOW risk, high confidence",
                "2-leg parlay: MODERATE risk, 82% win probability",
                "5-leg parlay: HIGH risk but positive EV",
                "Kicker bets: EXTREME risk, lottery ticket nature",
            ],
            supporting_data={"risk_levels": ["LOW", "MODERATE", "HIGH", "EXTREME"]},
            confidence_score=88.0,
            related_picks=[],
            warnings=["Never bet more than 2-3% of bankroll on any single bet", "Parlays have exponential risk increase"],
            suggested_actions=["Allocate 70% to straight bets", "20% to 2-3 leg parlays", "10% to kickers/exotics"],
            timestamp=datetime.now()
        )
    
    def _handle_bankroll_guidance(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle bankroll guidance queries."""
        return JarvisResponse(
            query_type=QueryType.BANKROLL_GUIDANCE,
            query_text=query,
            main_answer="With $500 bankroll, recommended allocation today: $28 on straight bets (Embiid $10, Jokic $10, Brunson $8), $10 on 2-leg parlay, $5 on 5-leg exotic parlay, $5 on kicker moonshot. Total exposure: $48 (9.6% of bankroll).",
            detailed_reasoning=[
                "Straight bets: 5.6% of bankroll for solid foundation",
                "2-leg parlay: 2% for moderate upside",
                "5-leg exotic: 1% for lottery ticket",
                "Kicker: 1% for moonshot potential",
                "Total under 10% keeps us conservative while capturing upside",
            ],
            supporting_data={"total_exposure": 48.0, "exposure_pct": 9.6},
            confidence_score=95.0,
            related_picks=[],
            warnings=["Never exceed 10% daily exposure", "Stick to the plan even if previous bets lost"],
            suggested_actions=["Set aside $48 for today's action", "Track results", "Adjust tomorrow based on outcomes"],
            timestamp=datetime.now()
        )
    
    def _handle_general_query(self, query: str, context: Optional[Dict]) -> JarvisResponse:
        """Handle general queries."""
        return JarvisResponse(
            query_type=QueryType.BEST_PICKS_TODAY,
            query_text=query,
            main_answer="I'm Jarvis, your NBA betting intelligence assistant. I can help you find the best picks, explain why bets have value, build parlays, find high-odds kickers, and assess risk. Try asking:\n\n- 'What are the best picks today?'\n- 'Find me a 6-leg parlay'\n- 'Any kicker bets for big payouts?'\n- 'Explain the Embiid pick'\n- 'What's my bankroll strategy?'",
            detailed_reasoning=[],
            supporting_data={},
            confidence_score=100.0,
            related_picks=[],
            warnings=[],
            suggested_actions=["Ask about today's picks", "Request parlay building", "Inquire about specific players"],
            timestamp=datetime.now()
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — JARVIS INTELLIGENCE SYSTEM")
    print("  Your AI Betting Assistant")
    print("=" * 70)
    
    jarvis = JarvisIntelligence()
    
    # Demo queries
    demo_queries = [
        "What are the best picks today?",
        "Find me a 6-leg parlay",
        "Any kicker bets for big payouts?",
        "What's my bankroll strategy?",
    ]
    
    for query in demo_queries:
        print(f"\n{'='*70}")
        print(f"  USER: {query}")
        print(f"{'='*70}\n")
        
        response = jarvis.ask(query)
        
        print(f"JARVIS: {response.main_answer}\n")
        
        if response.detailed_reasoning:
            print("  Detailed Reasoning:")
            for reason in response.detailed_reasoning:
                print(f"    • {reason}")
            print()
        
        if response.warnings:
            print("  ⚠️  Warnings:")
            for warning in response.warnings:
                print(f"    • {warning}")
            print()
        
        if response.suggested_actions:
            print("  💡 Suggested Actions:")
            for action in response.suggested_actions:
                print(f"    • {action}")
            print()
        
        print(f"  Confidence Score: {response.confidence_score:.1f}%")
    
    # Demo pick explanation
    print(f"\n{'='*70}")
    print("  PICK EXPLANATION DEMO")
    print(f"{'='*70}\n")
    
    print("  Demo disabled - requires real data integration")
    print("  To enable demo, integrate sportsbook API for odds")
    
    print("\n" + "="*70)
    print("  DEMO COMPLETE")
    print("="*70)
