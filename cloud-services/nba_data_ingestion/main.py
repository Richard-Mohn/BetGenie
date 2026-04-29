#!/usr/bin/env python3
"""
BetGenie Cloud Run Service: NBA Data Ingestion
Fetches NBA game data, player stats, and injury reports.
Stores data in Firestore for real-time access.
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud.logging import Client as LoggingClient
import logging

# Initialize Flask app
app = Flask(__name__)

# Initialize Google Cloud clients
db = firestore.Client()
logging_client = LoggingClient()
logging_client.setup_logging()

# Config
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'betgenie-ai')
BALLDONTLIE_API_KEY = os.environ.get('BALLEDONTLIE_API_KEY', '')
NBA_API_BASE = "https://api.balldontlie.io/v1"


class NBAGame:
    """NBA Game data structure."""
    def __init__(self, game_data: dict):
        self.game_id = str(game_data.get('id', ''))
        self.home_team = game_data.get('home_team', {}).get('name', '')
        self.away_team = game_data.get('visitor_team', {}).get('name', '')
        self.home_team_id = game_data.get('home_team', {}).get('id', '')
        self.away_team_id = game_data.get('visitor_team', {}).get('id', '')
        self.start_time = game_data.get('date', '')
        self.status = game_data.get('status', '')
        self.season = game_data.get('season', '')
        self.home_score = game_data.get('home_team_score', 0)
        self.away_score = game_data.get('visitor_team_score', 0)
        
    def to_dict(self) -> dict:
        return {
            'game_id': self.game_id,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'start_time': self.start_time,
            'status': self.status,
            'season': self.season,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'date': self.start_time.split('T')[0] if 'T' in self.start_time else self.start_time[:10],
            'updated_at': datetime.now().isoformat()
        }


class Player:
    """NBA Player data structure."""
    def __init__(self, player_data: dict):
        self.player_id = str(player_data.get('id', ''))
        self.first_name = player_data.get('first_name', '')
        self.last_name = player_data.get('last_name', '')
        self.name = f"{self.first_name} {self.last_name}"
        self.team = player_data.get('team', {}).get('name', '')
        self.team_id = player_data.get('team', {}).get('id', '')
        self.position = player_data.get('position', '')
        self.height = player_data.get('height', '')
        self.weight = player_data.get('weight', '')
        self.jersey_number = player_data.get('jersey_number', '')
        
    def to_dict(self) -> dict:
        return {
            'player_id': self.player_id,
            'name': self.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'team': self.team,
            'team_id': self.team_id,
            'position': self.position,
            'height': self.height,
            'weight': self.weight,
            'jersey_number': self.jersey_number,
            'updated_at': datetime.now().isoformat()
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'nba-data-ingestion',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/fetch-games', methods=['POST'])
def fetch_games():
    """Fetch today's NBA games."""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Fetch from BallDontLie API
        headers = {'Authorization': BALLDONTLIE_API_KEY} if BALLDONTLIE_API_KEY else {}
        
        response = requests.get(
            f"{NBA_API_BASE}/games",
            headers=headers,
            params={'dates[]': today, 'per_page': 100}
        )
        
        if response.status_code != 200:
            logging.error(f"API error: {response.status_code} - {response.text}")
            return jsonify({'error': 'Failed to fetch games from API'}), 500
        
        data = response.json()
        games_data = data.get('data', [])
        
        # Process and store games
        games = []
        batch = db.batch()
        
        for game_data in games_data:
            game = NBAGame(game_data)
            games.append(game.to_dict())
            
            # Store in Firestore
            doc_ref = db.collection('games').document(game.game_id)
            batch.set(doc_ref, game.to_dict(), merge=True)
        
        batch.commit()
        
        logging.info(f"Fetched and stored {len(games)} games for {today}")
        
        return jsonify({
            'date': today,
            'games_count': len(games),
            'games': games
        })
        
    except Exception as e:
        logging.error(f"Error fetching games: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-players', methods=['POST'])
def fetch_players():
    """Fetch all NBA players."""
    try:
        headers = {'Authorization': BALLDONTLIE_API_KEY} if BALLDONTLIE_API_KEY else {}
        
        # Fetch players (paginated)
        all_players = []
        cursor = 0
        per_page = 100
        
        while True:
            response = requests.get(
                f"{NBA_API_BASE}/players",
                headers=headers,
                params={'per_page': per_page, 'cursor': cursor}
            )
            
            if response.status_code != 200:
                break
            
            data = response.json()
            players_data = data.get('data', [])
            
            if not players_data:
                break
            
            all_players.extend(players_data)
            cursor += per_page
            
            # Limit to avoid timeout
            if cursor >= 500:
                break
        
        # Store in Firestore
        batch = db.batch()
        for player_data in all_players:
            player = Player(player_data)
            doc_ref = db.collection('players').document(player.player_id)
            batch.set(doc_ref, player.to_dict(), merge=True)
        
        batch.commit()
        
        logging.info(f"Fetched and stored {len(all_players)} players")
        
        return jsonify({
            'players_count': len(all_players),
            'message': f'Successfully stored {len(all_players)} players'
        })
        
    except Exception as e:
        logging.error(f"Error fetching players: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-player-stats', methods=['POST'])
def fetch_player_stats():
    """Fetch recent player stats."""
    try:
        data = request.get_json() or {}
        player_id = data.get('player_id')
        
        if not player_id:
            return jsonify({'error': 'player_id is required'}), 400
        
        headers = {'Authorization': BALLDONTLIE_API_KEY} if BALLDONTLIE_API_KEY else {}
        
        # Fetch last 10 games stats
        response = requests.get(
            f"{NBA_API_BASE}/stats",
            headers=headers,
            params={
                'player_ids[]': player_id,
                'per_page': 10,
                'sort': 'date',
                'direction': 'desc'
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch stats'}), 500
        
        stats_data = response.json().get('data', [])
        
        # Store in Firestore
        for stat in stats_data:
            stat_id = f"{player_id}_{stat.get('game', {}).get('id', '')}"
            doc_ref = db.collection('player_stats').document(stat_id)
            doc_ref.set({
                'player_id': player_id,
                'game_id': str(stat.get('game', {}).get('id', '')),
                'points': stat.get('pts', 0),
                'rebounds': stat.get('reb', 0),
                'assists': stat.get('ast', 0),
                'threes': stat.get('fg3m', 0),
                'steals': stat.get('stl', 0),
                'blocks': stat.get('blk', 0),
                'minutes': stat.get('min', ''),
                'fg_pct': stat.get('fg_pct', 0),
                'fg3_pct': stat.get('fg3_pct', 0),
                'ft_pct': stat.get('ft_pct', 0),
                'date': stat.get('game', {}).get('date', ''),
                'updated_at': datetime.now().isoformat()
            }, merge=True)
        
        return jsonify({
            'player_id': player_id,
            'stats_count': len(stats_data),
            'stats': stats_data
        })
        
    except Exception as e:
        logging.error(f"Error fetching player stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/fetch-injuries', methods=['POST'])
def fetch_injuries():
    """Fetch injury reports (mock implementation - real would scrape ESPN)."""
    try:
        # In production, this would scrape ESPN or use an injury API
        # For now, return mock data structure
        
        injuries = [
            {
                'player_name': 'Example Player',
                'team': 'LAL',
                'status': 'Out',
                'injury': 'Ankle',
                'date': datetime.now().isoformat()
            }
        ]
        
        return jsonify({
            'injuries_count': len(injuries),
            'injuries': injuries,
            'note': 'This is a mock endpoint - real implementation would scrape injury data'
        })
        
    except Exception as e:
        logging.error(f"Error fetching injuries: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['POST'])
def run_all():
    """Main endpoint - runs all data ingestion tasks."""
    try:
        results = {}
        
        # Fetch games
        with app.test_client() as client:
            games_response = client.post('/fetch-games')
            results['games'] = games_response.get_json()
        
        # Fetch player stats for key players
        # In production, this would iterate through all active players
        key_players = ['237', '115', '140']  # LeBron, Steph, KD (example IDs)
        results['player_stats'] = []
        
        for player_id in key_players:
            with app.test_client() as client:
                stats_response = client.post('/fetch-player-stats',
                    json={'player_id': player_id})
                results['player_stats'].append(stats_response.get_json())
        
        logging.info("NBA data ingestion completed successfully")
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'results': results
        })
        
    except Exception as e:
        logging.error(f"Error in data ingestion: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
