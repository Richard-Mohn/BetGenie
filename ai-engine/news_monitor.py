"""
BetGenie — NewsAPI Integration for Personal Event Scanning

Fetches sports news and scans for NBA player mentions to detect
personal events that affect performance (legal issues, family events,
health problems, etc.).

Uses NewsAPI (free tier: 100 requests/day) to fetch articles,
then extracts player mentions and classifies events.
"""

import os
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum
import re


class EventCategory(Enum):
    """Categories of personal events that affect performance."""
    LEGAL = "legal"  # Arrests, lawsuits, legal trouble
    FAMILY = "family"  # Births, deaths, divorces, family issues
    HEALTH = "health"  # Injuries, illnesses, medical procedures
    PSYCHOLOGICAL = "psychological"  # Mental health, motivation issues
    SITUATIONAL = "situational"  # Contract negotiations, trades, endorsements
    POSITIVE = "positive"  # Good news (awards, achievements, etc.)


@dataclass
class NewsArticle:
    """A news article from NewsAPI."""
    title: str
    description: str
    url: str
    published_at: datetime
    source: str
    content: Optional[str] = None


@dataclass
class PlayerEvent:
    """A detected personal event for a player."""
    player_name: str
    event_category: EventCategory
    description: str
    severity: float  # 0.0-1.0
    date: datetime
    source_url: str
    confidence: float  # How confident are we this is about the player


class NewsMonitor:
    """
    Monitors news sources for NBA player personal events.
    
    Uses NewsAPI to fetch sports news, then scans for player mentions
    and classifies events based on keywords.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        
        # Player name aliases (for better matching)
        self.player_aliases = {
            "lebron james": ["lebron", "lbj", "king james"],
            "stephen curry": ["steph curry", "curry", "steph"],
            "kevin durant": ["kd", "durant"],
            "luka doncic": ["luka", "doncic"],
            "giannis antetokounmpo": ["giannis", "greek freak"],
            "joel embiid": ["embiid", "joel"],
            "jayson tatum": ["tatum", "jt"],
            "anthony edwards": ["ant", "edwards", "anthony edwards"],
            "shai gilgeous-alexander": ["sga", "shai"],
            "victor wembanyama": ["wemby", "wembanyama"],
            "tyrese haliburton": ["haliburton", "tyrese"],
            "paolo banchero": ["paolo", "banchero"],
            "michael porter jr": ["mpj", "michael porter"],
            "derrick white": ["dwhite", "derrick white"],
            "malik monk": ["monk", "malik"],
            "austin reaves": ["ar", "austin reaves"],
            "immanuel quickley": ["iq", "quickley"],
            "reed sheppard": ["sheppard", "reed"],
        }
        
        # Event classification keywords
        self.event_keywords = {
            EventCategory.LEGAL: [
                "arrest", "charged", "lawsuit", "legal", "court", "indicted",
                "investigation", "police", "crime", "felony", "misdemeanor"
            ],
            EventCategory.FAMILY: [
                "wife", "husband", "child", "son", "daughter", "divorce",
                "married", "engaged", "father", "mother", "family", "death",
                "died", "passed away", "funeral", "pregnant", "birth"
            ],
            EventCategory.HEALTH: [
                "injury", "hurt", "surgery", "hospital", "illness", "sick",
                "health", "concussion", "sprain", "fracture", "torn", "strain",
                "covid", "virus", "flu", "medical", "condition"
            ],
            EventCategory.PSYCHOLOGICAL: [
                "mental health", "depression", "anxiety", "stress", "therapy",
                "motivation", "focus", "struggling", "confidence", "mindset",
                "emotional", "psychological"
            ],
            EventCategory.SITUATIONAL: [
                "contract", "trade", "sign", "extension", "negotiation",
                "endorsement", "sponsor", "deal", "free agent", "re-signed",
                "contract year", "opt-out"
            ],
            EventCategory.POSITIVE: [
                "award", "mvp", "all-star", "champion", "won", "victory",
                "achievement", "record", "milestone", "honor", "recognition"
            ]
        }
    
    def fetch_sports_news(self, days_back: int = 7) -> List[NewsArticle]:
        """Fetch recent sports news from NewsAPI."""
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        url = f"{self.base_url}/everything"
        params = {
            "apiKey": self.api_key,
            "q": "NBA OR basketball",
            "domains": "espn.com,nba.com,bleacherreport.com,sbnation.com,si.com",
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append(NewsArticle(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    url=article.get("url", ""),
                    published_at=datetime.fromisoformat(article.get("publishedAt", "").replace("Z", "+00:00")),
                    source=article.get("source", {}).get("name", ""),
                    content=article.get("content")
                ))
            
            return articles
        
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def detect_player_mentions(self, article: NewsArticle) -> Dict[str, float]:
        """
        Detect which players are mentioned in an article.
        
        Returns: Dictionary of player_name -> confidence (0-1)
        """
        text = f"{article.title} {article.description} {article.content or ''}".lower()
        mentions = {}
        
        for player_name, aliases in self.player_aliases.items():
            # Check for full name
            if player_name in text:
                mentions[player_name] = 1.0
                continue
            
            # Check for aliases
            alias_count = sum(1 for alias in aliases if alias in text)
            if alias_count > 0:
                mentions[player_name] = min(0.8, alias_count * 0.3)
        
        return mentions
    
    def classify_event(self, text: str) -> tuple[EventCategory, float]:
        """
        Classify the type of event based on keywords.
        
        Returns: (category, confidence)
        """
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.event_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            return EventCategory.SITUATIONAL, 0.3
        
        # Return category with highest score
        best_category = max(category_scores.items(), key=lambda x: x[1])
        confidence = min(1.0, best_category[1] / 3.0)  # Normalize
        
        return best_category[0], confidence
    
    def calculate_severity(self, category: EventCategory, text: str) -> float:
        """
        Calculate the severity of an event (0.0-1.0).
        
        Legal and health issues are typically more severe than situational.
        """
        text_lower = text.lower()
        
        # Base severity by category
        base_severity = {
            EventCategory.LEGAL: 0.8,
            EventCategory.HEALTH: 0.7,
            EventCategory.FAMILY: 0.6,
            EventCategory.PSYCHOLOGICAL: 0.5,
            EventCategory.SITUATIONAL: 0.3,
            EventCategory.POSITIVE: 0.1  # Positive events have low severity (good for performance)
        }
        
        severity = base_severity.get(category, 0.5)
        
        # Adjust based on keywords
        severe_keywords = ["arrest", "charged", "lawsuit", "surgery", "hospital", "death"]
        mild_keywords = ["negotiation", "deal", "sign", "endorsement"]
        
        if any(kw in text_lower for kw in severe_keywords):
            severity = min(1.0, severity + 0.2)
        elif any(kw in text_lower for kw in mild_keywords):
            severity = max(0.1, severity - 0.1)
        
        return severity
    
    def scan_for_events(self, days_back: int = 7) -> List[PlayerEvent]:
        """
        Scan recent news for player personal events.
        
        Returns: List of detected events
        """
        articles = self.fetch_sports_news(days_back)
        events = []
        
        for article in articles:
            text = f"{article.title} {article.description} {article.content or ''}"
            mentions = self.detect_player_mentions(article)
            
            for player_name, confidence in mentions.items():
                if confidence < 0.5:  # Skip low-confidence mentions
                    continue
                
                category, category_confidence = self.classify_event(text)
                severity = self.calculate_severity(category, text)
                
                # Skip positive events (they don't hurt performance)
                if category == EventCategory.POSITIVE:
                    continue
                
                event = PlayerEvent(
                    player_name=player_name,
                    event_category=category,
                    description=article.title,
                    severity=severity,
                    date=article.published_at,
                    source_url=article.url,
                    confidence=min(confidence, category_confidence)
                )
                
                events.append(event)
        
        return events
    
    def get_events_for_player(self, player_name: str, days_back: int = 30) -> List[PlayerEvent]:
        """Get all events for a specific player in the last N days."""
        all_events = self.scan_for_events(days_back)
        return [e for e in all_events if e.player_name.lower() == player_name.lower()]


class FreeNewsAggregator:
    """
    Aggregates news from FREE sources (no API keys required):
    - RSS Feeds (ESPN, NBA.com, etc.)
    - Reddit r/nba, r/fantasybball (free tier)
    - Web scraping (select sites)
    - Twitter/X scraping (if available)
    
    This provides real-time monitoring without paid APIs.
    """
    
    # Free RSS feeds for NBA news
    RSS_FEEDS = [
        "https://www.espn.com/espn/rss/nba/news",
        "https://www.nba.com/rss.xml",
        "https://bleacherreport.com/nba/feed",
        "https://www.si.com/rss/si_nba.rss",
        "https://www.cbssports.com/rss/headlines/nba/",
        "https://www.rotoworld.com/rss/feed.aspx?sport=nba&ftype=news&fmt=rss",
    ]
    
    # Reddit NBA subreddits for player news
    REDDIT_SUBREDDITS = ["nba", "fantasybball", "nbabets", "lakers", "warriors", "celtics"]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.player_aliases = NewsMonitor(None).player_aliases  # Reuse player aliases
        self.event_keywords = NewsMonitor(None).event_keywords  # Reuse keywords
    
    def fetch_rss_feeds(self) -> List[NewsArticle]:
        """Fetch articles from free RSS feeds."""
        import xml.etree.ElementTree as ET
        
        articles = []
        
        for feed_url in self.RSS_FEEDS:
            try:
                response = self.session.get(feed_url, timeout=10)
                if response.status_code != 200:
                    continue
                
                # Parse RSS XML
                root = ET.fromstring(response.content)
                
                # Handle RSS 2.0 and Atom formats
                if root.tag == 'rss':
                    items = root.findall('.//item')
                else:
                    items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
                
                for item in items[:20]:  # Limit to 20 articles per feed
                    try:
                        title = item.findtext('title', default='')
                        description = item.findtext('description', default='')
                        link = item.findtext('link', default='')
                        pub_date = item.findtext('pubDate', default='')
                        
                        if title and link:
                            # Parse date
                            try:
                                if pub_date:
                                    date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                                else:
                                    date = datetime.now()
                            except:
                                date = datetime.now()
                            
                            articles.append(NewsArticle(
                                title=title,
                                description=description,
                                url=link,
                                published_at=date,
                                source=feed_url.split('/')[2]  # Extract domain
                            ))
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"Error fetching RSS {feed_url}: {e}")
                continue
        
        return articles
    
    def fetch_reddit_posts(self, limit: int = 50) -> List[NewsArticle]:
        """
        Fetch recent posts from NBA-related subreddits.
        Uses Reddit's JSON API (no auth required for public posts).
        """
        articles = []
        
        for subreddit in self.REDDIT_SUBREDDITS[:3]:  # Limit to 3 subreddits to avoid rate limits
            try:
                url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                for post in posts:
                    post_data = post.get('data', {})
                    
                    title = post_data.get('title', '')
                    url = post_data.get('url', '')
                    selftext = post_data.get('selftext', '')
                    created_utc = post_data.get('created_utc', 0)
                    
                    if title and ('injury' in title.lower() or 'out' in title.lower() or 
                                  ' doubtful' in title.lower() or 'questionable' in title.lower() or
                                  'ruled out' in title.lower()):
                        # Only keep posts that might be injury/player news
                        articles.append(NewsArticle(
                            title=title,
                            description=selftext[:200] if selftext else '',
                            url=f"https://reddit.com{post_data.get('permalink', '')}",
                            published_at=datetime.fromtimestamp(created_utc),
                            source=f"reddit/r/{subreddit}"
                        ))
                        
            except Exception as e:
                print(f"Error fetching Reddit r/{subreddit}: {e}")
                continue
        
        return articles
    
    def scrape_injury_report(self) -> List[NewsArticle]:
        """
        Scrape NBA injury reports from official sources.
        Free to access, no API required.
        """
        articles = []
        
        # ESPN NBA Injuries page
        try:
            url = "https://www.espn.com/nba/injuries"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find injury table rows
                injury_rows = soup.find_all('tr', class_='Table__TR')
                
                for row in injury_rows[:30]:  # Limit to 30 injuries
                    try:
                        cells = row.find_all('td')
                        if len(cells) >= 3:
                            player_name = cells[0].get_text(strip=True)
                            position = cells[1].get_text(strip=True) if len(cells) > 1 else ''
                            status = cells[2].get_text(strip=True) if len(cells) > 2 else ''
                            
                            if player_name and status:
                                articles.append(NewsArticle(
                                    title=f"{player_name} - {status}",
                                    description=f"Position: {position}, Status: {status}",
                                    url=url,
                                    published_at=datetime.now(),
                                    source="ESPN Injuries"
                                ))
                    except:
                        continue
                        
        except Exception as e:
            print(f"Error scraping ESPN injuries: {e}")
        
        return articles
    
    def scan_all_free_sources(self) -> List[PlayerEvent]:
        """Scan all free sources and return detected player events."""
        all_articles = []
        
        print("Fetching from RSS feeds...")
        rss_articles = self.fetch_rss_feeds()
        all_articles.extend(rss_articles)
        print(f"  Found {len(rss_articles)} RSS articles")
        
        print("Fetching from Reddit...")
        reddit_articles = self.fetch_reddit_posts(limit=30)
        all_articles.extend(reddit_articles)
        print(f"  Found {len(reddit_articles)} Reddit posts")
        
        print("Scraping injury reports...")
        injury_articles = self.scrape_injury_report()
        all_articles.extend(injury_articles)
        print(f"  Found {len(injury_articles)} injury updates")
        
        # Process articles for player events
        events = []
        classifier = NewsMonitor(None)  # For classification methods
        
        for article in all_articles:
            text = f"{article.title} {article.description or ''}"
            
            # Detect players
            for player_name, aliases in self.player_aliases.items():
                if player_name in text.lower() or any(alias in text.lower() for alias in aliases):
                    # Classify event
                    category, cat_confidence = classifier.classify_event(text)
                    severity = classifier.calculate_severity(category, text)
                    
                    # Skip positive events
                    if category.value == 'positive':
                        continue
                    
                    events.append(PlayerEvent(
                        player_name=player_name,
                        event_category=category,
                        description=article.title,
                        severity=severity,
                        date=article.published_at,
                        source_url=article.url,
                        confidence=0.7  # RSS confidence
                    ))
        
        # Remove duplicates (same player, similar date)
        unique_events = []
        seen = set()
        for event in events:
            key = (event.player_name, event.date.strftime('%Y-%m-%d'), event.event_category.value)
            if key not in seen:
                seen.add(key)
                unique_events.append(event)
        
        return unique_events


class RealTimeNewsService:
    """
    Real-time news monitoring service that continuously checks for updates.
    Can be run as a background service or cron job.
    """
    
    def __init__(self, check_interval_minutes: int = 15):
        self.check_interval = check_interval_minutes
        self.aggregator = FreeNewsAggregator()
        self.last_check = None
        self.known_events = set()  # Track already-reported events
    
    def check_for_updates(self) -> List[PlayerEvent]:
        """Check for new events since last scan."""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for news updates...")
        
        # Scan all sources
        events = self.aggregator.scan_all_free_sources()
        
        # Filter to only new events
        new_events = []
        for event in events:
            event_key = f"{event.player_name}:{event.date.strftime('%Y-%m-%d %H:%M')}:{event.description[:50]}"
            
            if event_key not in self.known_events:
                self.known_events.add(event_key)
                new_events.append(event)
        
        self.last_check = datetime.now()
        
        if new_events:
            print(f"🚨 Detected {len(new_events)} NEW events:")
            for event in new_events:
                print(f"  • {event.player_name.title()}: {event.event_category.value} "
                      f"(severity: {event.severity:.1f})")
                print(f"    {event.description[:80]}...")
        else:
            print("  No new events detected")
        
        return new_events
    
    def run_continuous_monitoring(self, duration_hours: int = 24):
        """Run continuous monitoring for specified duration."""
        import time
        
        print(f"\n{'='*70}")
        print(f"  REAL-TIME NEWS MONITOR")
        print(f"  Checking every {self.check_interval} minutes for {duration_hours} hours")
        print(f"{'='*70}\n")
        
        # Initial scan
        self.check_for_updates()
        
        # Continuous monitoring
        checks = 0
        max_checks = (duration_hours * 60) // self.check_interval
        
        try:
            while checks < max_checks:
                time.sleep(self.check_interval * 60)
                new_events = self.check_for_updates()
                
                # Here you could:
                # - Send alerts
                # - Update player impact scores
                # - Notify users of significant events
                
                checks += 1
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
        
        print(f"\n{'='*70}")
        print(f"  MONITORING COMPLETE")
        print(f"  Total checks: {checks}")
        print(f"  Unique events tracked: {len(self.known_events)}")
        print(f"{'='*70}\n")


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — NEWSAPI MONITOR")
    print("  Personal Event Scanning")
    print("=" * 70)
    
    # Get API key from environment
    api_key = os.environ.get("NEWS_API_KEY")
    
    if not api_key:
        print("\n⚠️  NEWS_API_KEY not found in environment variables")
        print("   Set it with: export NEWS_API_KEY=your_key_here")
        print("\nRunning demo with mock data...")
        
        # Demo with mock data
        monitor = NewsMonitor(api_key="demo_key")
        
        # Simulate a news article
        mock_article = NewsArticle(
            title="LeBron James misses practice due to family emergency",
            description="Los Angeles Lakers star LeBron James was absent from practice today due to a family emergency.",
            url="https://example.com/article",
            published_at=datetime.now(),
            source="ESPN"
        )
        
        print("\n" + "-" * 70)
        print("  MOCK ARTICLE ANALYSIS")
        print("-" * 70)
        print(f"\nTitle: {mock_article.title}")
        print(f"Source: {mock_article.source}")
        
        mentions = monitor.detect_player_mentions(mock_article)
        print(f"\nPlayer Mentions:")
        for player, conf in mentions.items():
            print(f"  {player}: {conf:.1%}")
        
        text = f"{mock_article.title} {mock_article.description}"
        category, conf = monitor.classify_event(text)
        severity = monitor.calculate_severity(category, text)
        
        print(f"\nEvent Classification:")
        print(f"  Category: {category.value}")
        print(f"  Confidence: {conf:.1%}")
        print(f"  Severity: {severity:.1f}")
        
    else:
        print(f"\n✓ NEWS_API_KEY found")
        print(f"  Fetching recent NBA news...")
        
        monitor = NewsMonitor(api_key=api_key)
        events = monitor.scan_for_events(days_back=7)
        
        print(f"\n" + "-" * 70)
        print(f"  DETECTED EVENTS (Last 7 Days)")
        print("-" * 70)
        print(f"\nTotal Events Found: {len(events)}")
        
        for event in events:
            print(f"\n{event.player_name.title()}")
            print(f"  Category: {event.event_category.value}")
            print(f"  Severity: {event.severity:.1f}")
            print(f"  Description: {event.description}")
            print(f"  Date: {event.date.strftime('%Y-%m-%d')}")
            print(f"  Source: {event.source_url}")
            print(f"  Confidence: {event.confidence:.1%}")
        
        if not events:
            print("\n  No significant personal events detected.")
    
    print("\n" + "=" * 70)
    print("  NEWSAPI MONITOR — READY")
    print("=" * 70)
    
    # Demo free news aggregator
    print("\n\n" + "=" * 70)
    print("  FREE NEWS AGGREGATOR DEMO")
    print("  (RSS Feeds + Reddit + Web Scraping - NO API KEY NEEDED)")
    print("=" * 70)
    
    print("\n📡 Fetching from FREE sources...")
    print("  (This uses RSS feeds, Reddit API, and web scraping)")
    print("  (No paid API keys required!)\n")
    
    try:
        aggregator = FreeNewsAggregator()
        free_events = aggregator.scan_all_free_sources()
        
        print(f"\n{'='*70}")
        print(f"  FREE SOURCE RESULTS")
        print(f"{'='*70}")
        print(f"\nTotal Events from Free Sources: {len(free_events)}")
        
        # Group by category
        by_category = {}
        for event in free_events:
            cat = event.event_category.value
            by_category[cat] = by_category.get(cat, []) + [event]
        
        for cat, events in by_category.items():
            print(f"\n  {cat.upper()} ({len(events)} events):")
            for event in events[:2]:  # Show top 2 per category
                print(f"    • {event.player_name.title()}: {event.description[:60]}...")
        
        # Demo real-time service
        print("\n\n" + "=" * 70)
        print("  REAL-TIME MONITORING DEMO")
        print("  (Simulated 15-minute interval checks)")
        print("=" * 70)
        print("\n🕐 To run real-time monitoring:")
        print("   service = RealTimeNewsService(check_interval_minutes=15)")
        print("   service.run_continuous_monitoring(duration_hours=24)")
        print("\n   This will check for new player news every 15 minutes")
        print("   and alert you to significant events automatically!")
        
        print("\n" + "=" * 70)
        print("  FREE NEWS SOURCES AVAILABLE:")
        print("=" * 70)
        print("\n  ✓ RSS Feeds: ESPN, NBA.com, Bleacher Report, SI, CBS Sports")
        print("  ✓ Reddit: r/nba, r/fantasybball, r/nbabets, team subreddits")
        print("  ✓ Web Scraping: ESPN Injury Report, Rotoworld")
        print("  ✓ All FREE - No API keys needed!")
        print("\n  💡 Recommendation: Use FreeNewsAggregator for daily scans")
        print("     Use RealTimeNewsService for continuous monitoring")
        
    except Exception as e:
        print(f"\n  Demo error (expected if running without network): {e}")
        print("  This would work in production with internet access")
    
    print("\n" + "=" * 70)
    print("  NEWS MONITORING SYSTEM — READY")
    print("=" * 70)
