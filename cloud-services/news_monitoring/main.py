#!/usr/bin/env python3
"""
BetGenie Cloud Run Service: News Monitoring
Monitors news sources for NBA player events using RSS feeds.
"""

import os
import json
import feedparser
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud.logging import Client as LoggingClient
import logging

app = Flask(__name__)
db = firestore.Client()
logging_client = LoggingClient()
logging_client.setup_logging()

RSS_FEEDS = [
    "https://www.espn.com/espn/rss/nba/news",
    "https://www.nba.com/rss.xml",
    "https://bleacherreport.com/nba/feed",
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'news-monitoring'})

@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    try:
        data = request.get_json() or {}
        hours_back = data.get('hours_back', 24)
        
        since = datetime.now() - timedelta(hours=hours_back)
        articles = []
        
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    article_date = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
                    
                    if article_date > since:
                        articles.append({
                            'title': entry.get('title', ''),
                            'link': entry.get('link', ''),
                            'published': article_date.isoformat(),
                            'source': feed_url
                        })
            except Exception as e:
                logging.error(f"Error parsing feed {feed_url}: {e}")
        
        # Store in Firestore
        batch = db.batch()
        for article in articles:
            doc_ref = db.collection('news_events').document()
            doc_ref.set({
                'title': article['title'],
                'link': article['link'],
                'published': article['published'],
                'source': article['source'],
                'updated_at': datetime.now().isoformat()
            })
        
        batch.commit()
        
        return jsonify({
            'articles_count': len(articles),
            'message': f'Successfully fetched {len(articles)} articles'
        })
        
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['POST'])
def run_all():
    with app.test_client() as client:
        response = client.post('/fetch-news', json={'hours_back': 24})
    return response.get_json()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
