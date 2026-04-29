"""
Multi-Source News Aggregator Module

This module aggregates news from multiple sources (NewsAPI, Google News, Reddit)
for comprehensive event detection and verification. This ensures accuracy and enables
cross-referencing of player-related news across different platforms.

Author: BetGenie AI Team
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from enum import Enum
import os
import requests
import json
from collections import defaultdict


class NewsSource(Enum):
    """News data sources"""
    NEWSAPI = "newsapi"
    GOOGLE_NEWS = "google_news"
    REDDIT = "reddit"


class EventCategory(Enum):
    """Categories of personal events affecting players"""
    LEGAL = "legal"
    FAMILY = "family"
    HEALTH = "health"
    RELATIONSHIP = "relationship"
    FINANCIAL = "financial"
    CONTRACT = "contract"
    TRADE = "trade"
    INJURY = "injury"
    PERSONAL = "personal"
    OTHER = "other"


@dataclass
class NewsArticle:
    """Represents a news article from a source"""
    source: NewsSource
    title: str
    content: str
    url: str
    published_at: datetime
    author: Optional[str] = None
    source_name: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def get_age_hours(self) -> float:
        """Get age of article in hours"""
        return (datetime.utcnow() - self.published_at).total_seconds() / 3600


@dataclass
class PlayerEvent:
    """Detected event affecting a player"""
    player_name: str
    category: EventCategory
    description: str
    severity: float  # 0.0 to 1.0
    sources: List[NewsSource] = field(default_factory=list)
    articles: List[NewsArticle] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def source_count(self) -> int:
        """Number of sources reporting this event"""
        return len(set(self.sources))
    
    @property
    def article_count(self) -> int:
        """Number of articles about this event"""
        return len(self.articles)
    
    @property
    def confidence_score(self) -> float:
        """
        Confidence score based on multiple sources and recency (0.0 to 1.0)
        Higher score = more sources reporting + more recent
        """
        # More sources = higher confidence
        source_bonus = min(self.source_count / 3.0, 1.0) * 0.5
        
        # More articles = higher confidence
        article_bonus = min(self.article_count / 5.0, 1.0) * 0.2
        
        # More recent = higher confidence
        age_hours = (datetime.utcnow() - self.detected_at).total_seconds() / 3600
        recency_bonus = max(0, 1.0 - (age_hours / 48.0)) * 0.3  # Decay over 48 hours
        
        return source_bonus + article_bonus + recency_bonus


@dataclass
class NewsConsensus:
    """Consensus news about a specific topic/player"""
    topic: str
    events: List[PlayerEvent] = field(default_factory=list)
    articles: List[NewsArticle] = field(default_factory=list)
    
    @property
    def sources(self) -> Set[NewsSource]:
        """Unique sources contributing to this consensus"""
        sources = set()
        for event in self.events:
            sources.update(event.sources)
        return sources
    
    @property
    def total_articles(self) -> int:
        """Total articles about this topic"""
        return len(self.articles)
    
    def get_events_by_category(self, category: EventCategory) -> List[PlayerEvent]:
        """Get all events of a specific category"""
        return [e for e in self.events if e.category == category]
    
    def get_high_severity_events(self, threshold: float = 0.7) -> List[PlayerEvent]:
        """Get events with severity above threshold"""
        return [e for e in self.events if e.severity >= threshold]


class MultiNewsAggregator:
    """
    Main aggregator class for fetching and consolidating news from multiple sources.
    """
    
    def __init__(self):
        self.consensuses: Dict[str, NewsConsensus] = {}
        self.api_keys = {
            NewsSource.NEWSAPI: os.getenv("NEWS_API_KEY", "712e8b10ba594f3ba4738e74b3817979"),
            NewsSource.REDDIT_CLIENT_ID: os.getenv("REDDIT_CLIENT_ID"),
            NewsSource.REDDIT_CLIENT_SECRET: os.getenv("REDDIT_CLIENT_SECRET"),
        }
    
    def fetch_from_newsapi(self, query: str, days_back: int = 7) -> List[NewsArticle]:
        """
        Fetch news from NewsAPI
        
        Args:
            query: Search query (e.g., "LeBron James injury")
            days_back: How many days back to search
        """
        api_key = self.api_keys[NewsSource.NEWSAPI]
        if not api_key:
            print("Warning: NewsAPI key not set")
            return []
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "from": (datetime.utcnow() - timedelta(days=days_back)).isoformat()
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                article = NewsArticle(
                    source=NewsSource.NEWSAPI,
                    title=item.get("title", ""),
                    content=item.get("description", "") or item.get("content", ""),
                    url=item.get("url", ""),
                    published_at=datetime.fromisoformat(item.get("publishedAt", "").replace("Z", "+00:00")),
                    author=item.get("author"),
                    source_name=item.get("source", {}).get("name")
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []
    
    def fetch_from_google_news(self, query: str) -> List[NewsArticle]:
        """
        Fetch news from Google News (via RSS or scraping)
        
        Note: Google News doesn't have a public API. This implementation
        uses a placeholder approach. In production, you might use:
        - Google News RSS feeds
        - Third-party aggregators
        - Web scraping (with proper permissions)
        """
        # Placeholder for Google News integration
        # In production, implement RSS parsing or use a service like GNews API
        return []
    
    def fetch_from_reddit(self, query: str, subreddit: str = "NBA") -> List[NewsArticle]:
        """
        Fetch posts from Reddit about NBA players
        
        Args:
            query: Search query
            subreddit: Subreddit to search (default: NBA)
        """
        client_id = self.api_keys.get("REDDIT_CLIENT_ID")
        client_secret = self.api_keys.get("REDDIT_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            print("Warning: Reddit API credentials not set")
            return []
        
        try:
            # Authenticate with Reddit
            auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
            data = {
                "grant_type": "client_credentials"
            }
            response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, timeout=10)
            response.raise_for_status()
            token_response = response.json()
            access_token = token_response.get("access_token")
            
            if not access_token:
                print("Error: Could not get Reddit access token")
                return []
            
            # Search for posts
            headers = {
                "Authorization": f"bearer {access_token}",
                "User-Agent": "BetGenie/0.1"
            }
            params = {
                "q": query,
                "subreddit": subreddit,
                "sort": "new",
                "limit": 50
            }
            response = requests.get("https://oauth.reddit.com/r/NBA/search", headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for post in data.get("data", {}).get("children", []):
                post_data = post.get("data", {})
                article = NewsArticle(
                    source=NewsSource.REDDIT,
                    title=post_data.get("title", ""),
                    content=post_data.get("selftext", "")[:500],  # Limit content length
                    url=f"https://reddit.com{post_data.get('permalink', '')}",
                    published_at=datetime.fromtimestamp(post_data.get("created_utc", 0)),
                    author=post_data.get("author"),
                    source_name=f"r/{subreddit}"
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error fetching from Reddit: {e}")
            return []
    
    def fetch_all_sources(self, query: str, subreddit: str = "NBA", days_back: int = 7) -> Dict[NewsSource, List[NewsArticle]]:
        """
        Fetch news from all configured sources
        """
        all_news = {}
        
        # Fetch from each source
        all_news[NewsSource.NEWSAPI] = self.fetch_from_newsapi(query, days_back)
        all_news[NewsSource.GOOGLE_NEWS] = self.fetch_from_google_news(query)
        all_news[NewsSource.REDDIT] = self.fetch_from_reddit(query, subreddit)
        
        return all_news
    
    def detect_player_events(self, articles: List[NewsArticle], player_name: str) -> List[PlayerEvent]:
        """
        Detect events affecting a player from news articles
        
        Args:
            articles: List of news articles to analyze
            player_name: Name of the player to search for
        """
        events = []
        
        # Keywords for each event category
        category_keywords = {
            EventCategory.LEGAL: ["lawsuit", "arrest", "charged", "court", "legal", "attorney"],
            EventCategory.FAMILY: ["family", "child", "parent", "spouse", "wife", "husband", "birth", "death"],
            EventCategory.HEALTH: ["injury", "surgery", "illness", "health", "hospital", "concussion"],
            EventCategory.RELATIONSHIP: ["breakup", "divorce", "dating", "relationship", "girlfriend", "boyfriend"],
            EventCategory.FINANCIAL: ["money", "investment", "debt", "financial", "bankruptcy"],
            EventCategory.CONTRACT: ["contract", "extension", "sign", "negotiation", "deal"],
            EventCategory.TRADE: ["trade", "traded", "acquired", "deal", "swap"],
            EventCategory.INJURY: ["injured", "hurt", "strain", "sprain", "fracture", "torn"],
            EventCategory.PERSONAL: ["personal", "private", "matter", "issue"],
        }
        
        for article in articles:
            # Check if article mentions the player
            text = (article.title + " " + article.content).lower()
            if player_name.lower() not in text:
                continue
            
            # Detect category based on keywords
            detected_category = EventCategory.OTHER
            severity = 0.3  # Default low severity
            
            for category, keywords in category_keywords.items():
                if any(keyword in text for keyword in keywords):
                    detected_category = category
                    
                    # Assign severity based on category
                    if category in [EventCategory.LEGAL, EventCategory.HEALTH, EventCategory.INJURY]:
                        severity = 0.8
                    elif category in [EventCategory.FAMILY, EventCategory.TRADE]:
                        severity = 0.6
                    elif category in [EventCategory.CONTRACT, EventCategory.FINANCIAL]:
                        severity = 0.5
                    break
            
            # Create event if category detected
            if detected_category != EventCategory.OTHER:
                event = PlayerEvent(
                    player_name=player_name,
                    category=detected_category,
                    description=article.title,
                    severity=severity,
                    sources=[article.source],
                    articles=[article]
                )
                events.append(event)
        
        return events
    
    def consolidate_events(self, all_news: Dict[NewsSource, List[NewsArticle]], player_name: str) -> Dict[str, NewsConsensus]:
        """
        Consolidate news from multiple sources and detect events
        """
        # Combine all articles
        all_articles = []
        for source, articles in all_news.items():
            all_articles.extend(articles)
        
        # Detect events
        events = self.detect_player_events(all_articles, player_name)
        
        # Group events by category/description
        event_groups = defaultdict(list)
        for event in events:
            key = f"{event.category.value}_{event.description}"
            event_groups[key].append(event)
        
        # Create consensuses
        consensuses = {}
        for key, group_events in event_groups.items():
            # Merge events from same category/description
            merged_event = group_events[0]
            for event in group_events[1:]:
                merged_event.sources.extend(event.sources)
                merged_event.articles.extend(event.articles)
                # Update severity to average
                merged_event.severity = (merged_event.severity + event.severity) / 2
            
            # Remove duplicates
            merged_event.sources = list(set(merged_event.sources))
            merged_event.articles = list({a.url: a for a in merged_event.articles}.values())
            
            consensus = NewsConsensus(
                topic=player_name,
                events=[merged_event],
                articles=merged_event.articles
            )
            consensuses[key] = consensus
        
        return consensuses
    
    def verify_event(self, player_name: str, event_description: str, min_sources: int = 2) -> bool:
        """
        Verify that an event is reported by multiple sources
        
        Args:
            player_name: Name of the player
            event_description: Description of the event
            min_sources: Minimum number of sources required for verification
        
        Returns:
            True if event is verified by multiple sources
        """
        for consensus in self.consensuses.values():
            if consensus.topic == player_name:
                for event in consensus.events:
                    if event_description.lower() in event.description.lower():
                        return event.source_count >= min_sources
        return False
    
    def get_player_news(self, player_name: str, subreddit: str = "NBA", days_back: int = 7) -> Dict[str, NewsConsensus]:
        """
        Get all news about a specific player from all sources
        
        Args:
            player_name: Name of the player
            subreddit: Reddit subreddit to search
            days_back: How many days back to search
        """
        # Build search query
        query = f"{player_name} NBA"
        
        # Fetch from all sources
        all_news = self.fetch_all_sources(query, subreddit, days_back)
        
        # Consolidate and detect events
        self.consensuses = self.consolidate_events(all_news, player_name)
        
        return self.consensuses
    
    def get_high_impact_events(self, severity_threshold: float = 0.7) -> List[PlayerEvent]:
        """
        Get all events with severity above threshold across all consensuses
        """
        high_impact = []
        for consensus in self.consensuses.values():
            high_impact.extend(consensus.get_high_severity_events(severity_threshold))
        return high_impact


def demo():
    """Demo the multi-news aggregator"""
    print("=== Multi-Source News Aggregator Demo ===\n")
    
    # Create aggregator
    aggregator = MultiNewsAggregator()
    
    # Get news for a player (using mock data for demo)
    print("Fetching news for LeBron James...")
    
    # Add some mock articles for demonstration
    mock_articles = [
        NewsArticle(
            source=NewsSource.NEWSAPI,
            title="LeBron James listed as questionable for tonight's game",
            content="Los Angeles Lakers star LeBron James is questionable for tonight's game against the Celtics due to ankle soreness.",
            url="https://example.com/news/lebron-questionable",
            published_at=datetime.utcnow() - timedelta(hours=2),
            source_name="ESPN"
        ),
        NewsArticle(
            source=NewsSource.REDDIT,
            title="LeBron injury update from practice",
            content="Saw LeBron limping at practice today, hoping it's not serious.",
            url="https://reddit.com/r/NBA/comments/lebron-practice",
            published_at=datetime.utcnow() - timedelta(hours=5),
            source_name="r/NBA",
            author="nba_fan123"
        ),
        NewsArticle(
            source=NewsSource.NEWSAPI,
            title="LeBron James signs new endorsement deal",
            content="LeBron James has signed a new multi-year endorsement deal with a major sportswear brand.",
            url="https://example.com/news/lebron-endorsement",
            published_at=datetime.utcnow() - timedelta(hours=12),
            source_name="Sports Illustrated"
        ),
    ]
    
    # Detect events
    events = aggregator.detect_player_events(mock_articles, "LeBron James")
    
    print(f"\nDetected {len(events)} events:")
    for event in events:
        print(f"\n  Event: {event.description}")
        print(f"  Category: {event.category.value}")
        print(f"  Severity: {event.severity:.2f}")
        print(f"  Sources: {', '.join(s.value for s in event.sources)}")
        print(f"  Articles: {event.article_count}")
        print(f"  Confidence Score: {event.confidence_score:.2f}")
    
    # Create consensus
    if events:
        consensus = NewsConsensus(
            topic="LeBron James",
            events=events,
            articles=mock_articles
        )
        
        print(f"\n\nConsensus for {consensus.topic}:")
        print(f"  Total Articles: {consensus.total_articles}")
        print(f"  Sources: {', '.join(s.value for s in consensus.sources)}")
        print(f"  High Severity Events: {len(consensus.get_high_severity_events(0.7))}")
    
    # Verify event
    print("\n\nEvent Verification:")
    is_verified = aggregator.verify_event("LeBron James", "injury", min_sources=2)
    print(f"  Injury event verified: {is_verified}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
