#!/usr/bin/env python3
"""
BetGenie Cloud Run Service: Odds Aggregation
Aggregates odds from multiple sportsbooks and stores in Firestore.
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud.logging import Client as LoggingClient
import logging

app = Flask(__name__)
db = firestore.Client()
logging_client = LoggingClient()
logging_client.setup_logging()

ODDS_API_KEY = os.environ.get('ODDS_API_KEY', '')
ODDS_API_BASE = "https://api.the-odds-api.com/v4"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'odds-aggregation'})

@app.route('/fetch-odds', methods=['POST'])
def fetch_odds():
    try:
        data = request.get_json() or {}
        sport = data.get('sport', 'basketball_nba')
        
        headers = {'Authorization': ODDS_API_KEY} if ODDS_API_KEY else {}
        
        response = requests.get(
            f"{ODDS_API_BASE}/sports/{sport}/odds",
            headers=headers,
            params={'regions': 'us', 'markets': 'h2h,spreads,totals', 'oddsFormat': 'american'}
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch odds'}), 500
        
        odds_data = response.json()
        
        batch = db.batch()
        for game_odds in odds_data:
            game_id = str(game_odds.get('id', ''))
            doc_ref = db.collection('odds').document(game_id)
            doc_ref.set({
                'game_id': game_id,
                'sport': sport,
                'odds': game_odds,
                'updated_at': datetime.now().isoformat()
            }, merge=True)
        
        batch.commit()
        
        return jsonify({
            'games_count': len(odds_data),
            'message': f'Successfully stored odds for {len(odds_data)} games'
        })
        
    except Exception as e:
        logging.error(f"Error fetching odds: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['POST'])
def run_all():
    with app.test_client() as client:
        response = client.post('/fetch-odds', json={'sport': 'basketball_nba'})
    return response.get_json()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
