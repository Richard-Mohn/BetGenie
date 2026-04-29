"""
BetGenie — Twitter/X API Integration for Social Media Monitoring

Fetches tweets mentioning NBA players to detect personal events,
sentiment, and real-time updates that affect performance.

Uses Twitter/X API v2 (free tier limited) to fetch tweets,
then analyzes sentiment and detects events.
"""

import os
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum


class Sentiment(Enum):
    """Sentiment classification for tweets."""
    POSITIVE = "positive"  # Good news, high confidence
    NEUTRAL = "neutral"    # Factual information
    NEGATIVE = "negative"  # Bad news, low confidence, distractions


@dataclass
class Tweet:
    """A tweet from Twitter/X API."""
    tweet_id: str
    text: str
    author: str
    created_at: datetime
    url: str
    public_metrics: Dict = None


@dataclass
class SocialEvent:
    """A detected social media event for a player."""
    player_name: str
    sentiment: Sentiment
    description: str
    severity: float  # 0.0-1.0
    date: datetime
    source_url: str
    confidence: float


class SocialMonitor:
    """
    Monitors Twitter/X for NBA player mentions and sentiment.
    
    Uses Twitter/X API v2 to fetch tweets, then analyzes sentiment
    and detects events that may affect performance.
    """
    
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        
        # Player name aliases for Twitter search
        self.player_search_terms = {
            "lebron james": ["LeBron James", "LeBron", "King James", "@KingJames"],
            "stephen curry": ["Stephen Curry", "Steph Curry", "Curry", "@StephenCurry30"],
            "kevin durant": ["Kevin Durant", "KD", "Durant", "@KDTrey5"],
            "luka doncic": ["Luka Doncic", "Luka", "Doncic", "@luka7doncic"],
            "giannis antetokounmpo": ["Giannis Antetokounmpo", "Giannis", "Greek Freak", "@Giannis_An34"],
            "joel embiid": ["Joel Embiid", "Embiid", "Joel", "@JoelEmbiid"],
            "jayson tatum": ["Jayson Tatum", "Tatum", "JT", "@jaytatum0"],
            "anthony edwards": ["Anthony Edwards", "Ant", "Edwards", "@TheAnt15"],
            "shai gilgeous-alexander": ["Shai Gilgeous-Alexander", "SGA", "Shai", "@ShaigilgeousA"],
            "victor wembanyama": ["Victor Wembanyama", "Wemby", "Wembanyama", "@wembanyama"],
            "tyrese haliburton": ["Tyrese Haliburton", "Haliburton", "Tyrese", "@TyreseHaliburton"],
            "paolo banchero": ["Paolo Banchero", "Paolo", "Banchero", "@paolobanchero"],
            "michael porter jr": ["Michael Porter Jr", "MPJ", "Michael Porter", "@MichaelPorterJr"],
            "derrick white": ["Derrick White", "DWhite", "Derrick White", "@DWhite921"],
            "malik monk": ["Malik Monk", "Monk", "Malik", "@MalikMonk5"],
            "austin reaves": ["Austin Reaves", "AR", "Austin Reaves", "@austinreaves"],
            "immanuel quickley": ["Immanuel Quickley", "IQ", "Quickley", "@ImmanuelQuickley"],
            "reed sheppard": ["Reed Sheppard", "Sheppard", "Reed", "@ReedSheppard"],
        }
        
        # Sentiment keywords
        self.positive_keywords = [
            "great", "amazing", "excellent", "dominant", "unstoppable",
            "mvp", "all-star", "champion", "winner", "clutch", "legend",
            "best", "incredible", "phenomenal", "elite", "star"
        ]
        
        self.negative_keywords = [
            "injury", "hurt", "struggling", "bad", "terrible", "awful",
            "disappointing", "struggle", "loss", "lose", "failed", "struggling",
            "injured", "out", "miss", "surgery", "hospital", "sick"
        ]
        
        self.event_keywords = {
            "legal": ["arrest", "charged", "lawsuit", "legal", "court", "police"],
            "family": ["wife", "husband", "child", "son", "daughter", "family", "death"],
            "health": ["injury", "hurt", "surgery", "hospital", "illness", "sick"],
            "contract": ["contract", "trade", "sign", "extension", "deal", "free agent"],
        }
    
    def search_tweets(self, query: str, max_results: int = 10) -> List[Tweet]:
        """Search for tweets using Twitter/X API v2."""
        url = f"{self.base_url}/tweets/search/recent"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "created_at,author_id,public_metrics,entities",
            "expansions": "author_id"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            tweets = []
            for tweet_data in data.get("data", []):
                tweets.append(Tweet(
                    tweet_id=tweet_data.get("id"),
                    text=tweet_data.get("text"),
                    author=tweet_data.get("author_id"),
                    created_at=datetime.fromisoformat(tweet_data.get("created_at").replace("Z", "+00:00")),
                    url=f"https://twitter.com/i/web/status/{tweet_data.get('id')}",
                    public_metrics=tweet_data.get("public_metrics")
                ))
            
            return tweets
        
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> tuple[Sentiment, float]:
        """
        Analyze sentiment of tweet text.
        
        Returns: (sentiment, confidence)
        """
        text_lower = text.lower()
        
        positive_count = sum(1 for kw in self.positive_keywords if kw in text_lower)
        negative_count = sum(1 for kw in self.negative_keywords if kw in text_lower)
        
        if positive_count > negative_count:
            confidence = min(1.0, positive_count / 3.0)
            return Sentiment.POSITIVE, confidence
        elif negative_count > positive_count:
            confidence = min(1.0, negative_count / 3.0)
            return Sentiment.NEGATIVE, confidence
        else:
            return Sentiment.NEUTRAL, 0.5
    
    def detect_event_type(self, text: str) -> tuple[str, float]:
        """
        Detect event type from tweet text.
        
        Returns: (event_type, confidence)
        """
        text_lower = text.lower()
        event_scores = {}
        
        for event_type, keywords in self.event_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                event_scores[event_type] = score
        
        if not event_scores:
            return "general", 0.3
        
        best_event = max(event_scores.items(), key=lambda x: x[1])
        confidence = min(1.0, best_event[1] / 2.0)
        
        return best_event[0], confidence
    
    def calculate_severity(self, sentiment: Sentiment, event_type: str) -> float:
        """Calculate severity based on sentiment and event type."""
        base_severity = {
            "legal": 0.8,
            "health": 0.7,
            "family": 0.6,
            "contract": 0.3,
            "general": 0.2
        }
        
        severity = base_severity.get(event_type, 0.3)
        
        # Adjust based on sentiment
        if sentiment == Sentiment.NEGATIVE:
            severity = min(1.0, severity + 0.2)
        elif sentiment == Sentiment.POSITIVE:
            severity = max(0.1, severity - 0.2)
        
        return severity
    
    def scan_for_events(self, hours_back: int = 24) -> List[SocialEvent]:
        """
        Scan recent tweets for player events.
        
        Returns: List of detected social events
        """
        events = []
        
        for player_name, search_terms in self.player_search_terms.items():
            # Search for each term
            for term in search_terms[:2]:  # Limit to first 2 terms per player
                tweets = self.search_tweets(f"{term} -is:retweet", max_results=5)
                
                for tweet in tweets:
                    # Filter by time
                    if datetime.now() - tweet.created_at > timedelta(hours=hours_back):
                        continue
                    
                    sentiment, sentiment_conf = self.analyze_sentiment(tweet.text)
                    event_type, event_conf = self.detect_event_type(tweet.text)
                    severity = self.calculate_severity(sentiment, event_type)
                    
                    # Skip positive events (they don't hurt performance)
                    if sentiment == Sentiment.POSITIVE:
                        continue
                    
                    event = SocialEvent(
                        player_name=player_name,
                        sentiment=sentiment,
                        description=tweet.text[:100],  # Truncate for display
                        severity=severity,
                        date=tweet.created_at,
                        source_url=tweet.url,
                        confidence=min(sentiment_conf, event_conf)
                    )
                    
                    events.append(event)
        
        return events
    
    def get_events_for_player(self, player_name: str, hours_back: int = 24) -> List[SocialEvent]:
        """Get all social events for a specific player in the last N hours."""
        all_events = self.scan_for_events(hours_back)
        return [e for e in all_events if e.player_name.lower() == player_name.lower()]


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — TWITTER/X SOCIAL MONITOR")
    print("  Social Media Event Detection")
    print("=" * 70)
    
    # Get API key from environment
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        print("\n⚠️  TWITTER_BEARER_TOKEN not found in environment variables")
        print("   Set it with: export TWITTER_BEARER_TOKEN=your_token_here")
        print("\nRunning demo with mock data...")
        
        # Demo with mock data
        monitor = SocialMonitor(bearer_token="demo_token")
        
        # Simulate a tweet
        mock_tweet = Tweet(
            tweet_id="123456789",
            text="LeBron James dealing with family emergency, will miss tonight's game",
            author="@NBA_Insider",
            created_at=datetime.now(),
            url="https://twitter.com/i/web/status/123456789"
        )
        
        print("\n" + "-" * 70)
        print("  MOCK TWEET ANALYSIS")
        print("-" * 70)
        print(f"\nTweet: {mock_tweet.text}")
        print(f"Author: {mock_tweet.author}")
        
        sentiment, conf = monitor.analyze_sentiment(mock_tweet.text)
        event_type, event_conf = monitor.detect_event_type(mock_tweet.text)
        severity = monitor.calculate_severity(sentiment, event_type)
        
        print(f"\nSentiment: {sentiment.value} ({conf:.1%})")
        print(f"Event Type: {event_type} ({event_conf:.1%})")
        print(f"Severity: {severity:.1f}")
        
    else:
        print(f"\n✓ TWITTER_BEARER_TOKEN found")
        print(f"  Scanning recent tweets for NBA players...")
        
        monitor = SocialMonitor(bearer_token=bearer_token)
        events = monitor.scan_for_events(hours_back=24)
        
        print(f"\n" + "-" * 70)
        print(f"  DETECTED SOCIAL EVENTS (Last 24 Hours)")
        print("-" * 70)
        print(f"\nTotal Events Found: {len(events)}")
        
        for event in events:
            print(f"\n{event.player_name.title()}")
            print(f"  Sentiment: {event.sentiment.value}")
            print(f"  Severity: {event.severity:.1f}")
            print(f"  Description: {event.description}")
            print(f"  Date: {event.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Source: {event.source_url}")
            print(f"  Confidence: {event.confidence:.1%}")
        
        if not events:
            print("\n  No significant social events detected.")
    
    print("\n" + "=" * 70)
    print("  TWITTER/X SOCIAL MONITOR — READY")
    print("=" * 70)
