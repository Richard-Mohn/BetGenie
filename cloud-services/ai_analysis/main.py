#!/usr/bin/env python3
"""
BetGenie Cloud Run Service: AI Analysis
Runs AI analysis on player data and generates picks.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud.logging import Client as LoggingClient
import logging

app = Flask(__name__)
db = firestore.Client()
logging_client = LoggingClient()
logging_client.setup_logging()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'ai-analysis'})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json() or {}
        game_id = data.get('game_id')
        
        if not game_id:
            return jsonify({'error': 'game_id is required'}), 400
        
        # Get game data from Firestore
        game_doc = db.collection('games').document(game_id).get()
        if not game_doc.exists:
            return jsonify({'error': 'Game not found'}), 404
        
        game = game_doc.to_dict()
        
        # Get odds for this game
        odds_query = db.collection('odds').where('game_id', '==', game_id).limit(1)
        odds_docs = odds_query.get()
        odds = next(odds_docs).to_dict() if odds_docs else None
        
        # Mock AI analysis (in production, this would call the Python AI engine)
        analysis = {
            'game_id': game_id,
            'home_team': game.get('home_team'),
            'away_team': game.get('away_team'),
            'predicted_winner': game.get('home_team'),
            'confidence': 0.72,
            'recommended_bets': [
                {
                    'type': 'spread',
                    'pick': f"{game.get('home_team')} -3.5",
                    'confidence': 0.68
                },
                {
                    'type': 'total',
                    'pick': f"OVER {game.get('home_team', 'Home')} total",
                    'confidence': 0.61
                }
            ],
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Store analysis
        doc_ref = db.collection('ai_analysis').document(game_id)
        doc_ref.set(analysis, merge=True)
        
        return jsonify(analysis)
        
    except Exception as e:
        logging.error(f"Error in analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-daily-report', methods=['POST'])
def generate_daily_report():
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get all games for today
        games_query = db.collection('games').where('date', '==', today)
        games = [doc.to_dict() for doc in games_query.stream()]
        
        # Get AI analysis for each game
        report = {
            'date': today,
            'games_count': len(games),
            'picks': [],
            'generated_at': datetime.now().isoformat()
        }
        
        for game in games:
            game_id = game.get('game_id')
            analysis_doc = db.collection('ai_analysis').document(game_id).get()
            if analysis_doc.exists:
                report['picks'].append(analysis_doc.to_dict())
        
        # Store report
        doc_ref = db.collection('daily_reports').document(today)
        doc_ref.set(report, merge=True)
        
        return jsonify(report)
        
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['POST'])
def run_all():
    with app.test_client() as client:
        response = client.post('/generate-daily-report')
    return response.get_json()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
