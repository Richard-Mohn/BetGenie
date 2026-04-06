"""
BetGenie — News & Sentiment Analysis Pipeline (v1 Prototype)

This module handles:
1. Fetching news articles about players
2. Extracting player mentions (entity extraction)
3. Classifying events by category
4. Scoring sentiment
5. Estimating performance impact

Production version will use fine-tuned BERT models and LangChain.
This prototype uses rule-based matching + OpenAI API.
"""

import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


@dataclass
class NewsArticle:
    """Raw news article from ingestion pipeline."""
    article_id: str
    title: str
    description: str
    content: str
    source: str
    url: str
    published_at: datetime
    image_url: Optional[str] = None


@dataclass
class PlayerMention:
    """An extracted mention of a player in a news article."""
    player_id: str
    player_name: str
    article_id: str
    context_snippet: str  # The sentence/paragraph containing the mention
    relevance_score: float  # 0-1, how relevant is this article to the player


@dataclass
class AnalyzedEvent:
    """The result of analyzing a news article for player impact."""
    player_id: str
    player_name: str
    event_category: str
    severity: float
    sentiment_score: float
    summary: str
    source_article: NewsArticle
    confidence: float


# ============================================================
# PLAYER NAME DATABASE (Prototype — hardcoded, will be DB-backed)
# ============================================================

# Maps canonical names to player IDs and known aliases
PLAYER_DATABASE = {
    "jamal murray": {
        "id": "jamal-murray-den",
        "team": "Denver Nuggets",
        "sport": "NBA",
        "aliases": ["j. murray", "murray"],
    },
    "nikola jokic": {
        "id": "nikola-jokic-den",
        "team": "Denver Nuggets",
        "sport": "NBA",
        "aliases": ["jokic", "the joker"],
    },
    "lebron james": {
        "id": "lebron-james-lal",
        "team": "Los Angeles Lakers",
        "sport": "NBA",
        "aliases": ["lebron", "king james", "lbj"],
    },
    "patrick mahomes": {
        "id": "patrick-mahomes-kc",
        "team": "Kansas City Chiefs",
        "sport": "NFL",
        "aliases": ["mahomes", "pat mahomes"],
    },
    "bobby portis": {
        "id": "bobby-portis-mil",
        "team": "Milwaukee Bucks",
        "sport": "NBA",
        "aliases": ["portis", "crazy eyes"],
    },
    "luka doncic": {
        "id": "luka-doncic-dal",
        "team": "Dallas Mavericks",
        "sport": "NBA",
        "aliases": ["luka", "luka magic", "doncic"],
    },
    # ... in production, this will be a database of 10,000+ athletes
}


# ============================================================
# EVENT CLASSIFICATION KEYWORDS (Prototype — rule-based)
# ============================================================

EVENT_KEYWORDS = {
    "legal_arrest": [
        "arrested", "arrest", "dui", "dwi", "charged with", "custody",
        "handcuffed", "booked", "mugshot", "police", "detained",
        "domestic violence", "assault charge", "felony", "misdemeanor",
    ],
    "legal_suspension": [
        "suspended", "suspension", "banned", "ped", "performance enhancing",
        "drug test", "failed test", "league discipline", "conduct policy",
    ],
    "legal_investigation": [
        "investigation", "under investigation", "lawsuit", "sued",
        "deposition", "court date", "hearing", "trial", "allegations",
    ],
    "family_positive": [
        "baby born", "newborn", "married", "wedding", "engagement",
        "graduated", "promoted", "family celebration", "daughter promoted",
        "son graduated", "family milestone",
    ],
    "family_negative": [
        "divorce", "separated", "family emergency", "family death",
        "mother passed", "father passed", "family illness", "custody battle",
        "car accident family", "restraining order",
    ],
    "health_injury": [
        "injury", "injured", "sprain", "strain", "torn", "fracture",
        "concussion", "surgery", "mri", "day-to-day", "out indefinitely",
        "questionable", "doubtful", "ruled out", "ankle", "knee", "hamstring",
    ],
    "health_recovery": [
        "cleared to play", "return from injury", "back in lineup",
        "full practice", "no restrictions", "healthy", "recovered",
    ],
    "financial_positive": [
        "contract extension", "new deal", "endorsement", "max contract",
        "sponsorship", "shoe deal", "brand deal",
    ],
    "financial_negative": [
        "fined", "fine", "contract dispute", "holdout", "pay cut",
        "financial trouble", "bankruptcy",
    ],
    "team_trade": [
        "traded", "trade", "waived", "released", "signed", "free agent",
        "trade deadline", "buyout",
    ],
    "team_coaching": [
        "coach fired", "new coach", "coaching change", "interim coach",
        "front office", "general manager",
    ],
    "social_controversy": [
        "controversy", "backlash", "criticized", "social media",
        "viral", "beef", "feud", "call out", "blasted",
    ],
    "social_positive": [
        "community service", "charity", "award", "honored",
        "all-star", "player of the week", "mvp candidate",
    ],
    "media_pressure": [
        "media frenzy", "press conference", "spotlight",
        "criticism", "hot seat", "under fire", "scrutiny",
    ],
}


def find_player_mentions(article: NewsArticle) -> list[PlayerMention]:
    """
    Extract player mentions from a news article.
    
    Prototype uses simple string matching.
    Production will use NER (Named Entity Recognition) models.
    """
    mentions = []
    text = f"{article.title} {article.description} {article.content}".lower()
    
    for name, info in PLAYER_DATABASE.items():
        # Check canonical name
        if name in text:
            # Extract context snippet (sentence containing the mention)
            sentences = re.split(r'[.!?]', text)
            context = next(
                (s.strip() for s in sentences if name in s),
                text[:200]
            )
            mentions.append(PlayerMention(
                player_id=info["id"],
                player_name=name.title(),
                article_id=article.article_id,
                context_snippet=context[:300],
                relevance_score=0.9,  # High confidence for exact name match
            ))
            continue
        
        # Check aliases
        for alias in info.get("aliases", []):
            if alias in text:
                sentences = re.split(r'[.!?]', text)
                context = next(
                    (s.strip() for s in sentences if alias in s),
                    text[:200]
                )
                mentions.append(PlayerMention(
                    player_id=info["id"],
                    player_name=name.title(),
                    article_id=article.article_id,
                    context_snippet=context[:300],
                    relevance_score=0.6,  # Lower confidence for alias match
                ))
                break
    
    return mentions


def classify_event(article: NewsArticle, player_mention: PlayerMention) -> Optional[str]:
    """
    Classify what type of event this article describes.
    
    Prototype uses keyword matching.
    Production will use a fine-tuned classifier model.
    """
    text = f"{article.title} {article.description} {article.content}".lower()
    
    scores = {}
    for category, keywords in EVENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[category] = score
    
    if not scores:
        return None
    
    # Return the category with the most keyword matches
    return max(scores, key=scores.get)


def score_sentiment(text: str) -> float:
    """
    Score the sentiment of text on a scale of -1.0 to 1.0.
    
    Prototype uses a simple keyword-based approach.
    Production will use a fine-tuned sentiment model (BERT/RoBERTa).
    """
    text_lower = text.lower()
    
    positive_words = [
        "great", "excellent", "amazing", "positive", "happy", "celebrate",
        "win", "victory", "success", "strong", "confident", "healthy",
        "cleared", "recovered", "promoted", "milestone", "honored",
    ]
    negative_words = [
        "arrested", "injury", "injured", "suspended", "controversy",
        "divorce", "death", "emergency", "trouble", "fired", "fined",
        "criticized", "struggling", "questionable", "doubtful", "out",
        "missed", "concern", "worry", "problem", "violation",
    ]
    
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    total = pos_count + neg_count
    if total == 0:
        return 0.0
    
    return (pos_count - neg_count) / total


def estimate_severity(event_category: str, text: str) -> float:
    """
    Estimate the severity of an event (0.0 to 1.0).
    
    Prototype uses simple heuristics.
    Production will use a trained regression model.
    """
    text_lower = text.lower()
    severity = 0.5  # Default moderate severity
    
    # High severity indicators
    high_severity = ["felony", "hospitalized", "season-ending", "indefinitely",
                     "death", "fatal", "domestic violence", "surgery"]
    if any(word in text_lower for word in high_severity):
        severity = 0.9
    
    # Low severity indicators
    low_severity = ["minor", "day-to-day", "precautionary", "routine", "mild"]
    if any(word in text_lower for word in low_severity):
        severity = 0.3
    
    return severity


def analyze_article(article: NewsArticle) -> list[AnalyzedEvent]:
    """
    Full analysis pipeline for a single article.
    
    1. Find player mentions
    2. For each mention, classify the event
    3. Score sentiment
    4. Estimate severity
    5. Return analyzed events
    """
    results = []
    
    # Step 1: Find player mentions
    mentions = find_player_mentions(article)
    
    for mention in mentions:
        # Step 2: Classify the event
        event_category = classify_event(article, mention)
        if event_category is None:
            continue
        
        # Step 3: Score sentiment
        sentiment = score_sentiment(
            f"{article.title} {article.description} {mention.context_snippet}"
        )
        
        # Step 4: Estimate severity
        severity = estimate_severity(
            event_category,
            f"{article.title} {article.description} {article.content}"
        )
        
        # Step 5: Build result
        results.append(AnalyzedEvent(
            player_id=mention.player_id,
            player_name=mention.player_name,
            event_category=event_category,
            severity=severity,
            sentiment_score=sentiment,
            summary=f"{mention.player_name}: {event_category.replace('_', ' ').title()} — {article.title[:100]}",
            source_article=article,
            confidence=mention.relevance_score * 0.8,  # Adjusted by pipeline confidence
        ))
    
    return results


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Demo: Analyze a sample article about Jamal Murray
    sample_article = NewsArticle(
        article_id="art-001",
        title="Jamal Murray Arrested for DUI in Denver",
        description="Denver Nuggets guard Jamal Murray was arrested early Saturday morning on suspicion of driving under the influence.",
        content="""
        Denver Nuggets point guard Jamal Murray was arrested on Saturday morning 
        in downtown Denver on suspicion of driving under the influence, according 
        to police reports. Murray, 28, was stopped by officers around 2:30 AM 
        after his vehicle was observed swerving between lanes. He was taken into 
        custody and later released on bond. The Nuggets organization released a 
        statement saying they are aware of the situation and gathering more 
        information. This comes at a critical time as the Nuggets push for 
        playoff positioning. Murray has been averaging 26.3 points per game 
        this season. His next court date is scheduled for March 15.
        """,
        source="ESPN",
        url="https://espn.com/example/murray-dui",
        published_at=datetime(2026, 2, 28, 8, 0, 0),
    )
    
    results = analyze_article(sample_article)
    
    print("=" * 60)
    print("  BETGENIE — NEWS ANALYSIS PIPELINE")
    print("=" * 60)
    for event in results:
        print(f"\n  Player: {event.player_name}")
        print(f"  Category: {event.event_category}")
        print(f"  Severity: {event.severity:.2f}")
        print(f"  Sentiment: {event.sentiment_score:+.2f}")
        print(f"  Confidence: {event.confidence:.2f}")
        print(f"  Summary: {event.summary}")
    print("\n" + "=" * 60)
