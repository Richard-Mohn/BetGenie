"""
BetGenie — Personal Event Manager

Integrates news monitoring with database storage.
Processes news articles, detects player events, stores in DB.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

from database import BetGenieDatabase, PersonalEventDB
from news_monitor import NewsMonitor
from impact_score import calculate_impact_score, PlayerEvent, EventCategory


class PersonalEventManager:
    """
    Manages personal events for players.
    
    Responsibilities:
    - Scan news sources for player events
    - Store events in database
    - Calculate PIS from stored events
    - Provide event timeline for players
    """
    
    def __init__(self, db: BetGenieDatabase = None, news_api_key: str = None):
        self.db = db or BetGenieDatabase()
        self.news_monitor = NewsMonitor(api_key=news_api_key) if news_api_key else None
    
    def process_news_article(self, title: str, description: str, 
                             source_url: str, published_at: str) -> List[PersonalEventDB]:
        """
        Process a news article and extract player events.
        
        Returns:
            List of detected events
        """
        events = []
        
        # Simple keyword-based detection (in production, use NLP)
        text = f"{title} {description}".lower()
        
        # Player database for matching
        all_players = self.db.get_all_players()
        
        for player in all_players:
            # Check if player mentioned
            if player.full_name.lower() not in text:
                continue
            
            # Detect event type
            event_category = self._classify_event(text)
            if not event_category:
                continue
            
            # Calculate severity
            severity = self._calculate_severity(event_category, text)
            
            # Create event
            event_id = f"news-{player.full_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            event = PersonalEventDB(
                event_id=event_id,
                player_name=player.full_name,
                category=event_category,
                description=title[:200],
                severity=severity,
                date=published_at,
                source_url=source_url,
                verified=False,  # News events start as unverified
                created_at=datetime.now(timezone.utc).isoformat()
            )
            
            # Store in database
            self.db.add_personal_event(event)
            events.append(event)
            
            print(f"  Detected event: {player.full_name} - {event_category} (severity: {severity})")
        
        return events
    
    def _classify_event(self, text: str) -> Optional[str]:
        """Classify event type from text."""
        text_lower = text.lower()
        
        # Legal events
        if any(word in text_lower for word in ["arrest", "charged", "lawsuit", "court", "dui", "police"]):
            return "legal_arrest"
        
        # Health events
        if any(word in text_lower for word in ["injury", "injured", "surgery", "hurt", "out", "day-to-day", "doubtful"]):
            return "health_injury"
        
        # Family events
        if any(word in text_lower for word in ["family", "wife", "husband", "child", "baby", "born", "death", "passed away"]):
            if "born" in text_lower or "baby" in text_lower:
                return "family_positive"
            return "family_negative"
        
        # Trade/team events
        if any(word in text_lower for word in ["trade", "traded", "sign", "signed", "contract", "free agent"]):
            return "team_trade"
        
        # Social events
        if any(word in text_lower for word in ["controversy", "scandal", "apologize", "twitter", "instagram", "social media"]):
            return "social_controversy"
        
        return None
    
    def _calculate_severity(self, category: str, text: str) -> float:
        """Calculate event severity (0.0-1.0)."""
        text_lower = text.lower()
        
        # Base severity by category
        base_severity = {
            "legal_arrest": 0.80,
            "health_injury": 0.70,
            "family_negative": 0.60,
            "social_controversy": 0.40,
            "team_trade": 0.30,
            "family_positive": 0.20,
        }
        
        severity = base_severity.get(category, 0.50)
        
        # Adjust based on keywords
        severe_keywords = ["serious", "major", "career-threatening", "suspended", " felony"]
        mild_keywords = ["minor", "precautionary", "day-to-day", "rest"]
        
        if any(kw in text_lower for kw in severe_keywords):
            severity = min(1.0, severity + 0.15)
        elif any(kw in text_lower for kw in mild_keywords):
            severity = max(0.1, severity - 0.15)
        
        return round(severity, 2)
    
    def get_player_pis(self, player_name: str) -> Dict:
        """
        Calculate current PIS for a player from stored events.
        
        Returns:
            PIS result dict
        """
        # Get events from last 30 days
        db_events = self.db.get_player_events(player_name, days_back=30)
        
        if not db_events:
            # Return baseline
            return {
                "overall": 75.0,
                "physical": 75.0,
                "emotional": 75.0,
                "psychological": 75.0,
                "situational": 75.0,
                "active_factors": [],
                "events_count": 0
            }
        
        # Convert to PlayerEvent format
        category_map = {
            "legal_arrest": EventCategory.LEGAL_ARREST,
            "legal_suspension": EventCategory.LEGAL_SUSPENSION,
            "family_negative": EventCategory.FAMILY_NEGATIVE,
            "family_positive": EventCategory.FAMILY_POSITIVE,
            "health_injury": EventCategory.HEALTH_INJURY,
            "health_recovery": EventCategory.HEALTH_RECOVERY,
            "team_trade": EventCategory.TEAM_TRADE,
            "social_controversy": EventCategory.SOCIAL_CONTROVERSY,
        }
        
        player_events = []
        for e in db_events:
            cat = category_map.get(e.category)
            if cat:
                player_events.append(PlayerEvent(
                    event_id=e.event_id,
                    player_id=player_name,
                    category=cat,
                    description=e.description,
                    source_urls=[e.source_url],
                    sentiment_score=-0.7 if "negative" in e.category else 0.5,
                    severity=e.severity,
                    date=datetime.fromisoformat(e.date.replace('Z', '+00:00')),
                    confidence=0.90 if e.verified else 0.65,
                    verified=e.verified
                ))
        
        # Calculate PIS
        pis_result = calculate_impact_score(player_events)
        pis_result["events_count"] = len(db_events)
        
        return pis_result
    
    def scan_and_store_events(self, days_back: int = 7) -> int:
        """
        Scan news and store detected events.
        
        Returns:
            Number of events detected
        """
        if not self.news_monitor:
            print("News monitor not configured (no API key)")
            return 0
        
        print(f"\n🔍 Scanning news for player events (last {days_back} days)...")
        
        # Fetch news
        articles = self.news_monitor.fetch_sports_news(days_back)
        
        total_events = 0
        for article in articles[:20]:  # Process first 20 articles
            events = self.process_news_article(
                title=article.title,
                description=article.description,
                source_url=article.url,
                published_at=article.published_at.isoformat()
            )
            total_events += len(events)
        
        print(f"✅ Stored {total_events} events from {len(articles)} articles")
        return total_events
    
    def get_all_active_players_with_events(self) -> List[Dict]:
        """Get all players who have recent events."""
        recent_events = self.db.get_all_recent_events(days_back=30)
        
        # Group by player
        player_events = {}
        for event in recent_events:
            if event.player_name not in player_events:
                player_events[event.player_name] = []
            player_events[event.player_name].append(event)
        
        # Calculate PIS for each
        results = []
        for player_name, events in player_events.items():
            pis = self.get_player_pis(player_name)
            results.append({
                "player_name": player_name,
                "events_count": len(events),
                "pis_score": pis["overall"],
                "latest_event": events[0].description if events else None
            })
        
        # Sort by PIS (lowest first - most concerning)
        results.sort(key=lambda x: x["pis_score"])
        
        return results
    
    def generate_daily_impact_report(self) -> Dict:
        """Generate daily report of players with impact events."""
        players_with_events = self.get_all_active_players_with_events()
        
        # Categorize
        high_impact = [p for p in players_with_events if p["pis_score"] < 65]
        medium_impact = [p for p in players_with_events if 65 <= p["pis_score"] < 80]
        low_impact = [p for p in players_with_events if p["pis_score"] >= 80]
        
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_players_with_events": len(players_with_events),
            "high_impact_players": high_impact,
            "medium_impact_players": medium_impact,
            "low_impact_players": low_impact,
            "monitoring_summary": {
                "critical": len(high_impact),
                "elevated": len(medium_impact),
                "normal": len(low_impact)
            }
        }


# ========== DEMO ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — PERSONAL EVENT MANAGER DEMO")
    print("=" * 70)
    
    manager = PersonalEventManager()
    
    # Test 1: Add test events to database
    print("\n[1/4] Adding test events to database...")
    
    test_events = [
        {
            "player_name": "Jamal Murray",
            "category": "legal_arrest",
            "description": "DUI arrest on Feb 28, 2026",
            "severity": 0.85,
            "date": "2026-02-28T00:00:00+00:00"
        },
        {
            "player_name": "Anthony Edwards",
            "category": "family_positive",
            "description": "Wife gives birth to baby girl",
            "severity": 0.30,
            "date": "2026-03-15T00:00:00+00:00"
        },
        {
            "player_name": "Zion Williamson",
            "category": "health_injury",
            "description": "Hamstring strain - out 2-3 weeks",
            "severity": 0.75,
            "date": "2026-03-20T00:00:00+00:00"
        }
    ]
    
    for event_data in test_events:
        event_id = f"test-{event_data['player_name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        event = PersonalEventDB(
            event_id=event_id,
            player_name=event_data["player_name"],
            category=event_data["category"],
            description=event_data["description"],
            severity=event_data["severity"],
            date=event_data["date"],
            source_url="https://test.example.com",
            verified=True,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        manager.db.add_personal_event(event)
        print(f"  Added: {event_data['player_name']} - {event_data['category']}")
    
    # Test 2: Calculate PIS for players
    print("\n[2/4] Calculating Player Impact Scores...")
    
    for player in ["Jamal Murray", "Anthony Edwards", "Zion Williamson"]:
        pis = manager.get_player_pis(player)
        print(f"  {player}: PIS = {pis['overall']:.1f} ({pis['events_count']} events)")
    
    # Test 3: Get players with events
    print("\n[3/4] Getting players with recent events...")
    
    players_with_events = manager.get_all_active_players_with_events()
    print(f"  Found {len(players_with_events)} players with events")
    
    for p in players_with_events[:5]:
        print(f"  • {p['player_name']}: PIS={p['pis_score']:.1f}, Events={p['events_count']}")
    
    # Test 4: Generate impact report
    print("\n[4/4] Generating daily impact report...")
    
    report = manager.generate_daily_impact_report()
    print(f"  Total players with events: {report['total_players_with_events']}")
    print(f"  Critical (PIS < 65): {report['monitoring_summary']['critical']}")
    print(f"  Elevated (PIS 65-80): {report['monitoring_summary']['elevated']}")
    print(f"  Normal (PIS > 80): {report['monitoring_summary']['normal']}")
    
    print("\n" + "=" * 70)
    print("  PERSONAL EVENT MANAGER DEMO COMPLETE")
    print("=" * 70)
