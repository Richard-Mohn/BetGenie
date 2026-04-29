"""
BetGenie — Firebase Integration for Python AI Engine

Integrates with Firebase Firestore and Realtime Database.
- Firestore: Persistent data (players, games, events, predictions)
- Realtime DB: Live updates (odds, picks, scores)

Requires Firebase Admin SDK credentials.
"""

import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("WARNING: Firebase Admin SDK not installed. Run: pip install firebase-admin")


# ========== Configuration ==========

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "betgenie-ai")
SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./firebase-service-account.json")


class FirebaseDatabase:
    """
    Firebase Database Manager for BetGenie AI Engine.
    
    Provides:
    - Firestore: Players, games, events, predictions (structured data)
    - Realtime DB: Live odds, current picks, game scores (real-time updates)
    """
    
    def __init__(self):
        self.firestore = None
        self.rtdb = None
        self.app = None
        self._initialized = False
        
        if not FIREBASE_AVAILABLE:
            print("❌ Firebase Admin SDK not available")
            return
        
        self._init_firebase()
    
    def _init_firebase(self):
        """Initialize Firebase Admin SDK."""
        try:
            # Check if already initialized
            if firebase_admin._apps:
                self.app = firebase_admin.get_app()
                print("✅ Using existing Firebase app")
            else:
                # Try to load service account
                if os.path.exists(SERVICE_ACCOUNT_PATH):
                    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
                    self.app = firebase_admin.initialize_app(cred, {
                        'databaseURL': f'https://{FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com'
                    })
                    print(f"✅ Firebase initialized with service account")
                else:
                    # Try application default credentials (for Cloud Run, etc.)
                    try:
                        cred = credentials.ApplicationDefault()
                        self.app = firebase_admin.initialize_app(cred, {
                            'databaseURL': f'https://{FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com',
                            'projectId': FIREBASE_PROJECT_ID
                        })
                        print(f"✅ Firebase initialized with application default credentials")
                    except:
                        print(f"❌ No Firebase credentials found")
                        print(f"   Expected: {SERVICE_ACCOUNT_PATH}")
                        print(f"   Download from: https://console.firebase.google.com/project/{FIREBASE_PROJECT_ID}/settings/serviceaccounts/adminsdk")
                        return
            
            # Initialize Firestore
            self.firestore = firestore.client()
            
            # Initialize Realtime Database
            self.rtdb = db.reference('/', app=self.app)
            
            self._initialized = True
            print("✅ Firebase Database ready")
            
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            self._initialized = False
    
    # ========== FIRESTORE OPERATIONS ==========
    
    def is_ready(self) -> bool:
        """Check if Firebase is initialized and ready."""
        return self._initialized and self.firestore is not None
    
    # ----- Players Collection -----
    
    def save_player(self, player_id: str, player_data: Dict[str, Any]) -> bool:
        """Save player to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            player_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            self.firestore.collection('players').document(player_id).set(player_data)
            return True
        except Exception as e:
            print(f"Error saving player: {e}")
            return False
    
    def get_player(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player from Firestore."""
        if not self.is_ready():
            return None
        
        try:
            doc = self.firestore.collection('players').document(player_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting player: {e}")
            return None
    
    def get_all_players(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get all players from Firestore."""
        if not self.is_ready():
            return []
        
        try:
            docs = self.firestore.collection('players').limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting players: {e}")
            return []
    
    def get_players_by_team(self, team: str) -> List[Dict[str, Any]]:
        """Get players by team."""
        if not self.is_ready():
            return []
        
        try:
            docs = self.firestore.collection('players').where('team', '==', team).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting players by team: {e}")
            return []
    
    # ----- Games Collection -----
    
    def save_game(self, game_id: str, game_data: Dict[str, Any]) -> bool:
        """Save game to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            game_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            self.firestore.collection('games').document(game_id).set(game_data)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get game from Firestore."""
        if not self.is_ready():
            return None
        
        try:
            doc = self.firestore.collection('games').document(game_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting game: {e}")
            return None
    
    def get_todays_games(self) -> List[Dict[str, Any]]:
        """Get today's games from Firestore."""
        if not self.is_ready():
            return []
        
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            docs = self.firestore.collection('games').where('game_date', '==', today).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting today's games: {e}")
            return []
    
    # ----- Personal Events Collection -----
    
    def save_personal_event(self, event_id: str, event_data: Dict[str, Any]) -> bool:
        """Save personal event to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            event_data['created_at'] = datetime.now(timezone.utc).isoformat()
            self.firestore.collection('personal_events').document(event_id).set(event_data)
            
            # Also update player's events subcollection
            player_name = event_data.get('player_name', '')
            if player_name:
                self.firestore.collection('players').document(player_name.lower().replace(' ', '_')).collection('events').document(event_id).set(event_data)
            
            return True
        except Exception as e:
            print(f"Error saving event: {e}")
            return False
    
    def get_player_events(self, player_name: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """Get personal events for a player."""
        if not self.is_ready():
            return []
        
        try:
            cutoff_date = (datetime.now(timezone.utc) - __import__('datetime').timedelta(days=days_back)).isoformat()
            docs = self.firestore.collection('personal_events').where('player_name', '==', player_name).where('date', '>=', cutoff_date).order_by('date', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting player events: {e}")
            return []
    
    def get_recent_events(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get all recent personal events."""
        if not self.is_ready():
            return []
        
        try:
            cutoff_date = (datetime.now(timezone.utc) - __import__('datetime').timedelta(days=days_back)).isoformat()
            docs = self.firestore.collection('personal_events').where('date', '>=', cutoff_date).order_by('date', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting recent events: {e}")
            return []
    
    # ----- Predictions Collection -----
    
    def save_prediction(self, prediction_id: str, prediction_data: Dict[str, Any]) -> bool:
        """Save prediction to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            prediction_data['created_at'] = datetime.now(timezone.utc).isoformat()
            self.firestore.collection('predictions').document(prediction_id).set(prediction_data)
            return True
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False
    
    def get_prediction(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        """Get prediction from Firestore."""
        if not self.is_ready():
            return None
        
        try:
            doc = self.firestore.collection('predictions').document(prediction_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting prediction: {e}")
            return None
    
    def get_todays_predictions(self) -> List[Dict[str, Any]]:
        """Get today's predictions."""
        if not self.is_ready():
            return []
        
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            docs = self.firestore.collection('predictions').where('created_date', '==', today).order_by('confidence', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting today's predictions: {e}")
            return []
    
    def resolve_prediction(self, prediction_id: str, result: str, actual_value: float) -> bool:
        """Mark prediction as resolved with actual result."""
        if not self.is_ready():
            return False
        
        try:
            self.firestore.collection('predictions').document(prediction_id).update({
                'result': result,
                'actual_value': actual_value,
                'resolved_at': datetime.now(timezone.utc).isoformat(),
                'status': 'resolved'
            })
            return True
        except Exception as e:
            print(f"Error resolving prediction: {e}")
            return False
    
    def get_prediction_accuracy(self, days: int = 30) -> Dict[str, Any]:
        """Get prediction accuracy stats."""
        if not self.is_ready():
            return {'total': 0, 'wins': 0, 'losses': 0, 'win_rate': 0}
        
        try:
            cutoff_date = (datetime.now(timezone.utc) - __import__('datetime').timedelta(days=days)).isoformat()
            docs = self.firestore.collection('predictions').where('created_at', '>=', cutoff_date).where('status', '==', 'resolved').stream()
            
            predictions = [doc.to_dict() for doc in docs]
            
            wins = sum(1 for p in predictions if p.get('result') == 'win')
            losses = sum(1 for p in predictions if p.get('result') == 'loss')
            pushes = sum(1 for p in predictions if p.get('result') == 'push')
            total = wins + losses + pushes
            
            return {
                'total': total,
                'wins': wins,
                'losses': losses,
                'pushes': pushes,
                'win_rate': wins / total if total > 0 else 0
            }
        except Exception as e:
            print(f"Error getting accuracy: {e}")
            return {'total': 0, 'wins': 0, 'losses': 0, 'win_rate': 0}
    
    # ----- Historical Performance (Backtesting) -----
    
    def save_historical_performance(self, player_name: str, game_date: str, 
                                    performance_data: Dict[str, Any]) -> bool:
        """Save historical performance for backtesting."""
        if not self.is_ready():
            return False
        
        try:
            doc_id = f"{player_name.lower().replace(' ', '_')}_{game_date}"
            performance_data['player_name'] = player_name
            performance_data['game_date'] = game_date
            self.firestore.collection('historical_performance').document(doc_id).set(performance_data)
            return True
        except Exception as e:
            print(f"Error saving historical performance: {e}")
            return False
    
    def get_player_historical_performance(self, player_name: str) -> List[Dict[str, Any]]:
        """Get player's historical performance."""
        if not self.is_ready():
            return []
        
        try:
            docs = self.firestore.collection('historical_performance').where('player_name', '==', player_name).order_by('game_date', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error getting historical performance: {e}")
            return []
    
    # ========== REALTIME DATABASE OPERATIONS ==========
    
    def rtdb_is_ready(self) -> bool:
        """Check if Realtime Database is available."""
        return self._initialized and self.rtdb is not None
    
    # ----- Live Odds -----
    
    def update_live_odds(self, game_id: str, odds_data: Dict[str, Any]) -> bool:
        """Update live odds in Realtime Database."""
        if not self.rtdb_is_ready():
            return False
        
        try:
            odds_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            self.rtdb.child(f'live_odds/{game_id}').set(odds_data)
            return True
        except Exception as e:
            print(f"Error updating live odds: {e}")
            return False
    
    def get_live_odds(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get live odds from Realtime Database."""
        if not self.rtdb_is_ready():
            return None
        
        try:
            return self.rtdb.child(f'live_odds/{game_id}').get()
        except Exception as e:
            print(f"Error getting live odds: {e}")
            return None
    
    # ----- Live Picks -----
    
    def publish_pick(self, pick_id: str, pick_data: Dict[str, Any]) -> bool:
        """Publish a pick to Realtime Database for live updates."""
        if not self.rtdb_is_ready():
            return False
        
        try:
            pick_data['published_at'] = datetime.now(timezone.utc).isoformat()
            self.rtdb.child(f'picks/{pick_id}').set(pick_data)
            return True
        except Exception as e:
            print(f"Error publishing pick: {e}")
            return False
    
    def get_live_picks(self, date: Optional[str] = None) -> Dict[str, Any]:
        """Get all live picks for a date."""
        if not self.rtdb_is_ready():
            return {}
        
        try:
            if date is None:
                date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            return self.rtdb.child(f'picks').get() or {}
        except Exception as e:
            print(f"Error getting live picks: {e}")
            return {}
    
    # ----- Live Scores -----
    
    def update_live_score(self, game_id: str, score_data: Dict[str, Any]) -> bool:
        """Update live game scores."""
        if not self.rtdb_is_ready():
            return False
        
        try:
            score_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            self.rtdb.child(f'scores/{game_id}').set(score_data)
            return True
        except Exception as e:
            print(f"Error updating live score: {e}")
            return False
    
    def get_live_score(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get live game scores."""
        if not self.rtdb_is_ready():
            return None
        
        try:
            return self.rtdb.child(f'scores/{game_id}').get()
        except Exception as e:
            print(f"Error getting live score: {e}")
            return None
    
    # ----- System Status -----
    
    def update_system_status(self, status_data: Dict[str, Any]) -> bool:
        """Update system status in Realtime Database."""
        if not self.rtdb_is_ready():
            return False
        
        try:
            status_data['last_updated'] = datetime.now(timezone.utc).isoformat()
            self.rtdb.child('system/status').set(status_data)
            return True
        except Exception as e:
            print(f"Error updating system status: {e}")
            return False
    
    def get_system_status(self) -> Optional[Dict[str, Any]]:
        """Get system status."""
        if not self.rtdb_is_ready():
            return None
        
        try:
            return self.rtdb.child('system/status').get()
        except Exception as e:
            print(f"Error getting system status: {e}")
            return None
    
    # ========== BATCH OPERATIONS ==========
    
    def batch_save_players(self, players: List[Dict[str, Any]]) -> bool:
        """Batch save players to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            batch = self.firestore.batch()
            
            for player in players:
                player_id = player.get('player_id', player.get('full_name', '').lower().replace(' ', '_'))
                player['updated_at'] = datetime.now(timezone.utc).isoformat()
                ref = self.firestore.collection('players').document(player_id)
                batch.set(ref, player, merge=True)
            
            batch.commit()
            print(f"✅ Batch saved {len(players)} players")
            return True
        except Exception as e:
            print(f"Error batch saving players: {e}")
            return False
    
    def batch_save_predictions(self, predictions: List[Dict[str, Any]]) -> bool:
        """Batch save predictions to Firestore."""
        if not self.is_ready():
            return False
        
        try:
            batch = self.firestore.batch()
            
            for pred in predictions:
                pred_id = pred.get('prediction_id', f"pred_{datetime.now(timezone.utc).timestamp()}")
                pred['created_at'] = datetime.now(timezone.utc).isoformat()
                pred['created_date'] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                ref = self.firestore.collection('predictions').document(pred_id)
                batch.set(ref, pred, merge=True)
            
            batch.commit()
            print(f"✅ Batch saved {len(predictions)} predictions")
            return True
        except Exception as e:
            print(f"Error batch saving predictions: {e}")
            return False
    
    def publish_daily_report(self, report_data: Dict[str, Any]) -> bool:
        """Publish daily betting report to both Firestore and Realtime DB."""
        if not self.is_ready():
            return False
        
        try:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            report_id = f"daily_report_{date}"
            
            # Save to Firestore for persistence
            report_data['date'] = date
            report_data['published_at'] = datetime.now(timezone.utc).isoformat()
            self.firestore.collection('daily_reports').document(report_id).set(report_data)
            
            # Publish to Realtime DB for live access
            if self.rtdb_is_ready():
                self.rtdb.child(f'daily_reports/{date}').set(report_data)
            
            print(f"✅ Published daily report for {date}")
            return True
        except Exception as e:
            print(f"Error publishing daily report: {e}")
            return False


# ========== DEMO / TEST ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — FIREBASE DATABASE DEMO")
    print("=" * 70)
    
    # Initialize Firebase
    fb = FirebaseDatabase()
    
    if not fb.is_ready():
        print("\n⚠️  Firebase not initialized - demo mode only")
        print("\nTo enable Firebase:")
        print("  1. Download service account key from Firebase Console")
        print("  2. Save as: firebase-service-account.json")
        print("  3. Set: GOOGLE_APPLICATION_CREDENTIALS=./firebase-service-account.json")
        print(f"  4. Project ID: {FIREBASE_PROJECT_ID}")
        
        print("\n📋 Firestore Collections Structure:")
        print("  players/             - NBA player data")
        print("  games/                 - Game schedules and results")
        print("  personal_events/       - Player personal events")
        print("  predictions/           - AI predictions")
        print("  historical_performance/ - Backtesting data")
        print("  daily_reports/         - Generated reports")
        
        print("\n📋 Realtime Database Structure:")
        print("  /live_odds/{game_id}   - Real-time odds updates")
        print("  /picks/{pick_id}       - Live picks")
        print("  /scores/{game_id}      - Live game scores")
        print("  /system/status         - System health")
        print("  /daily_reports/{date}  - Today's report")
    else:
        print("\n✅ Firebase connected!")
        
        # Test Firestore operations
        print("\n[1/4] Testing Firestore player operations...")
        test_player = {
            'player_id': 'test_jokic',
            'full_name': 'Nikola Jokic',
            'team': 'Denver Nuggets',
            'position': 'C',
            'ppg': 29.4,
            'rpg': 12.8,
            'apg': 10.2
        }
        fb.save_player('test_jokic', test_player)
        print(f"  Saved player: {test_player['full_name']}")
        
        retrieved = fb.get_player('test_jokic')
        if retrieved:
            print(f"  Retrieved: {retrieved['full_name']} - {retrieved['ppg']} PPG")
        
        # Test prediction
        print("\n[2/4] Testing Firestore prediction operations...")
        test_prediction = {
            'prediction_id': 'pred_test_001',
            'player_name': 'Nikola Jokic',
            'game_id': 'game_001',
            'prop_type': 'points',
            'line': 28.5,
            'direction': 'over',
            'projected_value': 31.2,
            'confidence': 78.0,
            'edge': 2.7,
            'status': 'pending'
        }
        fb.save_prediction('pred_test_001', test_prediction)
        print(f"  Saved prediction: {test_prediction['player_name']} {test_prediction['direction']} {test_prediction['line']}")
        
        # Test Realtime DB
        if fb.rtdb_is_ready():
            print("\n[3/4] Testing Realtime Database...")
            fb.publish_pick('pick_test_001', {
                'player_name': 'Nikola Jokic',
                'pick': 'OVER 28.5 points',
                'confidence': 78,
                'status': 'active'
            })
            print("  Published pick to Realtime DB")
            
            fb.update_live_odds('game_001', {
                'home_team': 'Denver Nuggets',
                'away_team': 'Los Angeles Lakers',
                'spread': -5.5,
                'total': 225.5
            })
            print("  Updated live odds")
        
        # Test batch operations
        print("\n[4/4] Testing batch operations...")
        test_players = [
            {'player_id': 'test_murray', 'full_name': 'Jamal Murray', 'team': 'Denver Nuggets', 'ppg': 21.2},
            {'player_id': 'test_porter', 'full_name': 'Michael Porter Jr.', 'team': 'Denver Nuggets', 'ppg': 17.8}
        ]
        fb.batch_save_players(test_players)
        
        # Publish daily report
        print("\n[Bonus] Publishing daily report...")
        fb.publish_daily_report({
            'date': datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            'total_games': 10,
            'total_predictions': 5,
            'guaranteed_picks': 2,
            'best_pick': 'Nikola Jokic OVER 28.5'
        })
    
    print("\n" + "=" * 70)
    print("  FIREBASE DEMO COMPLETE")
    print("=" * 70)
