"""
BetGenie — Consensus Module

This module aggregates multiple intelligence sources to create a Unified Confidence Score:
1. Player Impact Score (PIS) - Our human-factor analysis
2. Sharp Money Movement - Professional betting data from exchanges
3. Expert Aggregation - Third-party pro picks from reputable sources
4. Market Sentiment - Public betting percentages and line movement

The goal is to identify when all sources align (high confidence) or when there are conflicts (trap games).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import math


class SourceType(Enum):
    PIS = "player_impact_score"           # Our internal analysis
    SHARP_MONEY = "sharp_money"            # Exchange data
    EXPERT_PICK = "expert_pick"            # Pro tipsters
    PUBLIC_SENTIMENT = "public_sentiment"  # Betting percentages
    LINE_MOVEMENT = "line_movement"        # Odds changes


class ConflictType(Enum):
    NONE = "none"                          # All sources aligned
    PIS_VS_SHARP = "pis_vs_sharp"          # Our analysis vs sharp money
    PIS_VS_EXPERTS = "pis_vs_experts"      # Our analysis vs experts
    SHARP_VS_PUBLIC = "sharp_vs_public"    # Sharp vs public (fade opportunity)
    ALL_CONFLICT = "all_conflict"          # Complete disagreement


@dataclass
class IntelligenceSource:
    """A single intelligence source for a pick."""
    source_type: SourceType
    source_name: str  # e.g., "BetGenie PIS", "OpticOdds Sharp", "Action Network"
    confidence: float  # 0-100
    direction: str  # "OVER" or "UNDER"
    weight: float  # How much to trust this source (0-1)
    timestamp: datetime
    metadata: Dict = None


@dataclass
class ConsensusResult:
    """The aggregated result from all intelligence sources."""
    player_name: str
    team: str
    prop_type: str
    line: float
    unified_confidence: float  # 0-100
    unified_direction: str
    sources: List[IntelligenceSource]
    conflict_type: ConflictType
    conflict_severity: float  # 0-1, how severe is the disagreement
    is_trap_game: bool
    reasoning: List[str]
    recommended_action: str  # "BET", "FADE", "AVOID", "WAIT"


class ConsensusModule:
    """
    Aggregates multiple intelligence sources to create a Unified Confidence Score.
    
    Philosophy:
    - When all sources align: Maximum confidence
    - When sources conflict: Flag as potential trap game
    - Weight sharp money higher than public sentiment
    - Weight our PIS based on strength of personal events
    """
    
    def __init__(self):
        self.source_weights = {
            SourceType.PIS: 0.35,           # Our analysis is 35% of decision
            SourceType.SHARP_MONEY: 0.30,    # Sharp money is 30%
            SourceType.EXPERT_PICK: 0.20,    # Expert picks are 20%
            SourceType.PUBLIC_SENTIMENT: 0.10, # Public is 10% (fade value)
            SourceType.LINE_MOVEMENT: 0.05,  # Line movement is 5%
        }
    
    def add_source(
        self,
        sources: List[IntelligenceSource],
        source_type: SourceType,
        source_name: str,
        confidence: float,
        direction: str,
        weight_override: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> List[IntelligenceSource]:
        """Add an intelligence source to the list."""
        weight = weight_override or self.source_weights.get(source_type, 0.2)
        
        source = IntelligenceSource(
            source_type=source_type,
            source_name=source_name,
            confidence=confidence,
            direction=direction,
            weight=weight,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        
        sources.append(source)
        return sources
    
    def calculate_unified_confidence(
        self,
        sources: List[IntelligenceSource]
    ) -> tuple[float, str]:
        """
        Calculate the unified confidence score and direction.
        
        Returns:
            (confidence_0_100, direction)
        """
        if not sources:
            return 0.0, "NONE"
        
        # Separate by direction
        over_sources = [s for s in sources if s.direction == "OVER"]
        under_sources = [s for s in sources if s.direction == "UNDER"]
        
        # Calculate weighted confidence for each direction
        over_score = sum(s.confidence * s.weight for s in over_sources)
        under_score = sum(s.confidence * s.weight for s in under_sources)
        
        # Determine direction
        if over_score > under_score:
            direction = "OVER"
            total_weight = sum(s.weight for s in over_sources)
            if total_weight == 0:
                return 0.0, "OVER"
            confidence = over_score / total_weight
        elif under_score > over_score:
            direction = "UNDER"
            total_weight = sum(s.weight for s in under_sources)
            if total_weight == 0:
                return 0.0, "UNDER"
            confidence = under_score / total_weight
        else:
            # Tie - return lower confidence
            direction = "NONE"
            confidence = (over_score + under_score) / 2
        
        return min(100, max(0, confidence)), direction
    
    def detect_conflicts(
        self,
        sources: List[IntelligenceSource],
        unified_direction: str
    ) -> tuple[ConflictType, float]:
        """
        Detect conflicts between intelligence sources.
        
        Returns:
            (conflict_type, severity_0_1)
        """
        if len(sources) < 2:
            return ConflictType.NONE, 0.0
        
        # Group by direction
        over_sources = [s for s in sources if s.direction == "OVER"]
        under_sources = [s for s in sources if s.direction == "UNDER"]
        
        # Check for conflicts
        pis_sources = [s for s in sources if s.source_type == SourceType.PIS]
        sharp_sources = [s for s in sources if s.source_type == SourceType.SHARP_MONEY]
        expert_sources = [s for s in sources if s.source_type == SourceType.EXPERT_PICK]
        public_sources = [s for s in sources if s.source_type == SourceType.PUBLIC_SENTIMENT]
        
        conflicts = []
        
        # PIS vs Sharp Money
        if pis_sources and sharp_sources:
            pis_dir = pis_sources[0].direction
            sharp_dir = sharp_sources[0].direction
            if pis_dir != sharp_dir:
                conflicts.append(ConflictType.PIS_VS_SHARP)
        
        # PIS vs Experts
        if pis_sources and expert_sources:
            pis_dir = pis_sources[0].direction
            expert_dir = expert_sources[0].direction
            if pis_dir != expert_dir:
                conflicts.append(ConflictType.PIS_VS_EXPERTS)
        
        # Sharp vs Public (fade opportunity)
        if sharp_sources and public_sources:
            sharp_dir = sharp_sources[0].direction
            public_dir = public_sources[0].direction
            if sharp_dir != public_dir:
                conflicts.append(ConflictType.SHARP_VS_PUBLIC)
        
        # Calculate severity based on confidence differences
        if not conflicts:
            return ConflictType.NONE, 0.0
        
        # Calculate average confidence difference
        max_conf = max(s.confidence for s in sources)
        min_conf = min(s.confidence for s in sources)
        severity = (max_conf - min_conf) / 100
        
        # If multiple conflicts, it's severe
        if len(conflicts) >= 2:
            return ConflictType.ALL_CONFLICT, min(1.0, severity * 1.5)
        
        return conflicts[0], severity
    
    def generate_reasoning(
        self,
        sources: List[IntelligenceSource],
        conflict_type: ConflictType,
        unified_confidence: float
    ) -> List[str]:
        """Generate human-readable reasoning for the consensus result."""
        reasoning = []
        
        # Add source breakdown
        for source in sources:
            reasoning.append(
                f"{source.source_name}: {source.direction} ({source.confidence}%)"
            )
        
        # Add conflict reasoning
        if conflict_type != ConflictType.NONE:
            if conflict_type == ConflictType.PIS_VS_SHARP:
                reasoning.append("⚠️ CONFLICT: Our PIS disagrees with sharp money movement")
            elif conflict_type == ConflictType.PIS_VS_EXPERTS:
                reasoning.append("⚠️ CONFLICT: Our PIS disagrees with expert picks")
            elif conflict_type == ConflictType.SHARP_VS_PUBLIC:
                reasoning.append("💡 OPPORTUNITY: Sharp money fading public sentiment")
            elif conflict_type == ConflictType.ALL_CONFLICT:
                reasoning.append("🚨 MAJOR CONFLICT: All sources disagree - AVOID")
        
        # Add confidence reasoning
        if unified_confidence >= 80:
            reasoning.append("🔒 Strong consensus across sources")
        elif unified_confidence >= 60:
            reasoning.append("💪 Moderate consensus with some variance")
        elif unified_confidence >= 40:
            reasoning.append("⚡ Weak consensus - proceed with caution")
        else:
            reasoning.append("❌ No clear consensus - avoid")
        
        return reasoning
    
    def determine_recommended_action(
        self,
        unified_confidence: float,
        conflict_type: ConflictType,
        conflict_severity: float,
        unified_direction: str
    ) -> str:
        """Determine the recommended action based on consensus."""
        # Major conflict - always avoid
        if conflict_type == ConflictType.ALL_CONFLICT:
            return "AVOID"
        
        # High severity conflict - avoid unless sharp vs public (fade opportunity)
        if conflict_severity > 0.5 and conflict_type != ConflictType.SHARP_VS_PUBLIC:
            return "AVOID"
        
        # Sharp vs public with high severity - fade the public
        if conflict_type == ConflictType.SHARP_VS_PUBLIC and conflict_severity > 0.3:
            return "FADE"
        
        # High confidence with no conflict - bet
        if unified_confidence >= 70 and conflict_type == ConflictType.NONE:
            return "BET"
        
        # Moderate confidence with minor conflict - wait
        if unified_confidence >= 60 and conflict_severity < 0.3:
            return "BET"
        
        # Low confidence - avoid
        if unified_confidence < 50:
            return "AVOID"
        
        # Default - wait for more data
        return "WAIT"
    
    def analyze_consensus(
        self,
        player_name: str,
        team: str,
        prop_type: str,
        line: float,
        pis_confidence: float,
        pis_direction: str,
        sharp_confidence: Optional[float] = None,
        sharp_direction: Optional[str] = None,
        expert_confidence: Optional[float] = None,
        expert_direction: Optional[str] = None,
        public_confidence: Optional[float] = None,
        public_direction: Optional[str] = None,
    ) -> ConsensusResult:
        """
        Full consensus analysis for a single pick.
        
        Args:
            player_name: Player name
            team: Team name
            prop_type: Prop type (points, rebounds, etc.)
            line: Betting line
            pis_confidence: Our PIS confidence (0-100)
            pis_direction: Our PIS direction (OVER/UNDER)
            sharp_confidence: Sharp money confidence (optional)
            sharp_direction: Sharp money direction (optional)
            expert_confidence: Expert pick confidence (optional)
            expert_direction: Expert pick direction (optional)
            public_confidence: Public betting confidence (optional)
            public_direction: Public betting direction (optional)
        """
        sources = []
        
        # Add PIS (always present)
        sources = self.add_source(
            sources,
            SourceType.PIS,
            "BetGenie PIS",
            pis_confidence,
            pis_direction
        )
        
        # Add Sharp Money if available
        if sharp_confidence is not None and sharp_direction is not None:
            sources = self.add_source(
                sources,
                SourceType.SHARP_MONEY,
                "OpticOdds Sharp",
                sharp_confidence,
                sharp_direction
            )
        
        # Add Expert Pick if available
        if expert_confidence is not None and expert_direction is not None:
            sources = self.add_source(
                sources,
                SourceType.EXPERT_PICK,
                "Expert Consensus",
                expert_confidence,
                expert_direction
            )
        
        # Add Public Sentiment if available
        if public_confidence is not None and public_direction is not None:
            sources = self.add_source(
                sources,
                SourceType.PUBLIC_SENTIMENT,
                "Public Betting",
                public_confidence,
                public_direction
            )
        
        # Calculate unified confidence
        unified_confidence, unified_direction = self.calculate_unified_confidence(sources)
        
        # Detect conflicts
        conflict_type, conflict_severity = self.detect_conflicts(sources, unified_direction)
        
        # Determine if trap game
        is_trap_game = (
            conflict_type in [ConflictType.PIS_VS_SHARP, ConflictType.ALL_CONFLICT] and
            conflict_severity > 0.4
        )
        
        # Generate reasoning
        reasoning = self.generate_reasoning(sources, conflict_type, unified_confidence)
        
        # Determine recommended action
        recommended_action = self.determine_recommended_action(
            unified_confidence,
            conflict_type,
            conflict_severity,
            unified_direction
        )
        
        return ConsensusResult(
            player_name=player_name,
            team=team,
            prop_type=prop_type,
            line=line,
            unified_confidence=unified_confidence,
            unified_direction=unified_direction,
            sources=sources,
            conflict_type=conflict_type,
            conflict_severity=conflict_severity,
            is_trap_game=is_trap_game,
            reasoning=reasoning,
            recommended_action=recommended_action,
        )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — CONSENSUS MODULE")
    print("  Intelligence Aggregation System")
    print("=" * 70)
    
    module = ConsensusModule()
    
    print("\n" + "-" * 70)
    print("  SCENARIO 1: All Sources Aligned (Strong Bet)")
    print("-" * 70)
    
    result1 = module.analyze_consensus(
        player_name="Shai Gilgeous-Alexander",
        team="Oklahoma City Thunder",
        prop_type="points",
        line=31.5,
        pis_confidence=82,
        pis_direction="UNDER",
        sharp_confidence=78,
        sharp_direction="UNDER",
        expert_confidence=75,
        expert_direction="UNDER",
        public_confidence=60,
        public_direction="UNDER",
    )
    
    print(f"\nPlayer: {result1.player_name}")
    print(f"Unified Confidence: {result1.unified_confidence:.1f}%")
    print(f"Unified Direction: {result1.unified_direction}")
    print(f"Conflict Type: {result1.conflict_type.value}")
    print(f"Conflict Severity: {result1.conflict_severity:.2f}")
    print(f"Trap Game: {result1.is_trap_game}")
    print(f"Recommended Action: {result1.recommended_action}")
    print(f"\nReasoning:")
    for reason in result1.reasoning:
        print(f"  {reason}")
    
    print("\n" + "-" * 70)
    print("  SCENARIO 2: PIS vs Sharp Money (Trap Game)")
    print("-" * 70)
    
    result2 = module.analyze_consensus(
        player_name="LeBron James",
        team="Los Angeles Lakers",
        prop_type="points",
        line=23.5,
        pis_confidence=78,
        pis_direction="OVER",
        sharp_confidence=72,
        sharp_direction="UNDER",  # Sharp money disagrees
        expert_confidence=65,
        expert_direction="UNDER",  # Experts also disagree
        public_confidence=70,
        public_direction="OVER",  # Public agrees with PIS
    )
    
    print(f"\nPlayer: {result2.player_name}")
    print(f"Unified Confidence: {result2.unified_confidence:.1f}%")
    print(f"Unified Direction: {result2.unified_direction}")
    print(f"Conflict Type: {result2.conflict_type.value}")
    print(f"Conflict Severity: {result2.conflict_severity:.2f}")
    print(f"Trap Game: {result2.is_trap_game}")
    print(f"Recommended Action: {result2.recommended_action}")
    print(f"\nReasoning:")
    for reason in result2.reasoning:
        print(f"  {reason}")
    
    print("\n" + "-" * 70)
    print("  SCENARIO 3: Sharp vs Public (Fade Opportunity)")
    print("-" * 70)
    
    result3 = module.analyze_consensus(
        player_name="Victor Wembanyama",
        team="San Antonio Spurs",
        prop_type="rebounds",
        line=10.5,
        pis_confidence=65,
        pis_direction="OVER",
        sharp_confidence=75,
        sharp_direction="UNDER",  # Sharp fading
        expert_confidence=70,
        expert_direction="UNDER",  # Experts also fading
        public_confidence=80,
        public_direction="OVER",  # Public loves the over
    )
    
    print(f"\nPlayer: {result3.player_name}")
    print(f"Unified Confidence: {result3.unified_confidence:.1f}%")
    print(f"Unified Direction: {result3.unified_direction}")
    print(f"Conflict Type: {result3.conflict_type.value}")
    print(f"Conflict Severity: {result3.conflict_severity:.2f}")
    print(f"Trap Game: {result3.is_trap_game}")
    print(f"Recommended Action: {result3.recommended_action}")
    print(f"\nReasoning:")
    for reason in result3.reasoning:
        print(f"  {reason}")
    
    print("\n" + "=" * 70)
    print("  CONSENSUS MODULE — READY")
    print("  Aggregating intelligence from multiple sources")
    print("=" * 70)
