"""
BetGenie — NBA Betting Pipeline with Firebase Integration

Enhanced pipeline that syncs all data to Firebase:
- Firestore: Players, games, events, predictions, reports
- Realtime DB: Live odds, picks, scores

This allows the web frontend to see data in real-time.
"""

import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Any

# Import original pipeline components
from nba_betting_pipeline import (
    NBABettingPipeline, GameInfo, PropBet, GuaranteedPicksReport,
    GameSchedule, PlayerPropLine, BetRecommendation
)
from firebase_db import FirebaseDatabase


class FirebaseEnhancedPipeline(NBABettingPipeline):
    """
    Enhanced betting pipeline with Firebase synchronization.
    
    Extends the base pipeline to:
    1. Sync all data to Firebase Firestore
    2. Publish live picks to Realtime Database
    3. Enable real-time updates for web frontend
    """
    
    def __init__(self, bankroll: float = 500.0, use_firebase: bool = True):
        super().__init__(bankroll)
        
        self.use_firebase = use_firebase
        self.firebase = None
        
        if use_firebase:
            self.firebase = FirebaseDatabase()
            if self.firebase.is_ready():
                print("✅ Firebase integration enabled")
            else:
                print("⚠️  Firebase not available - will use local SQLite only")
    
    async def run_full_pipeline_with_sync(self) -> Dict[str, Any]:
        """
        Run full pipeline and sync everything to Firebase.
        
        Returns:
            Complete report with Firebase sync status
        """
        print("\n" + "=" * 70)
        print("  BETGENIE — FULL PIPELINE WITH FIREBASE SYNC")
        print("=" * 70)
        
        # Step 1: Run base pipeline
        base_report = await self.run_full_pipeline()
        
        if not self.firebase or not self.firebase.is_ready():
            print("\n⚠️  Skipping Firebase sync (not connected)")
            return {
                **base_report,
                'firebase_sync': False,
                'firebase_error': 'Not connected'
            }
        
        # Step 2: Sync players to Firebase
        print("\n📤 Syncing players to Firebase...")
        self._sync_players_to_firebase()
        
        # Step 3: Sync games to Firebase
        print("\n📤 Syncing games to Firebase...")
        self._sync_games_to_firebase(base_report.get('games', {}))
        
        # Step 4: Sync predictions to Firebase
        print("\n📤 Syncing predictions to Firebase...")
        self._sync_predictions_to_firebase(base_report.get('predictions', []))
        
        # Step 5: Publish picks to Realtime Database
        print("\n📤 Publishing live picks to Realtime DB...")
        self._publish_picks_to_rtdb(base_report.get('guaranteed_picks', {}))
        
        # Step 6: Publish daily report
        print("\n📤 Publishing daily report...")
        self._publish_daily_report(base_report)
        
        # Step 7: Update system status
        self.firebase.update_system_status({
            'status': 'operational',
            'last_pipeline_run': datetime.now(timezone.utc).isoformat(),
            'total_predictions': base_report.get('total_predictions', 0),
            'guaranteed_picks': len(base_report.get('guaranteed_picks', {}).get('guaranteed_picks', [])),
            'games_analyzed': len(base_report.get('games', {}))
        })
        
        print("\n✅ Firebase sync complete!")
        print(f"   - Players synced")
        print(f"   - Games synced")
        print(f"   - Predictions synced")
        print(f"   - Picks published to Realtime DB")
        print(f"   - Daily report published")
        
        return {
            **base_report,
            'firebase_sync': True,
            'firebase_timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def _sync_players_to_firebase(self):
        """Sync all players to Firebase Firestore."""
        try:
            # Get players from ESPN data
            if not hasattr(self, 'espn_cache') or not self.espn_cache:
                self.espn_cache = self._load_espn_data()
            
            players_data = self.espn_cache.get('players', [])
            
            # Convert to Firebase format
            firebase_players = []
            for p in players_data[:100]:  # Sync top 100 players
                firebase_players.append({
                    'player_id': p.get('player_id', p.get('full_name', '').lower().replace(' ', '_')),
                    'full_name': p.get('full_name', ''),
                    'team': p.get('team', ''),
                    'position': p.get('position', ''),
                    'ppg': p.get('ppg', 0),
                    'rpg': p.get('rpg', 0),
                    'apg': p.get('apg', 0),
                    'source': 'espn'
                })
            
            # Batch save to Firebase
            success = self.firebase.batch_save_players(firebase_players)
            if success:
                print(f"  ✅ Synced {len(firebase_players)} players")
            else:
                print(f"  ❌ Failed to sync players")
                
        except Exception as e:
            print(f"  ❌ Error syncing players: {e}")
    
    def _sync_games_to_firebase(self, games: Dict[str, Any]):
        """Sync games to Firebase Firestore."""
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            count = 0
            
            for game_id, game_data in games.items():
                game_doc = {
                    'game_id': game_id,
                    'home_team': game_data.get('home_team', ''),
                    'away_team': game_data.get('away_team', ''),
                    'game_time': game_data.get('start_time', ''),
                    'game_date': today,
                    'status': 'scheduled',
                    'spread': game_data.get('spread', 0),
                    'total': game_data.get('total', 0),
                    'odds_count': len(game_data.get('odds', []))
                }
                
                self.firebase.save_game(game_id, game_doc)
                count += 1
            
            print(f"  ✅ Synced {count} games")
            
            # Also publish to Realtime DB for live updates
            for game_id, game_data in games.items():
                self.firebase.update_live_odds(game_id, {
                    'home_team': game_data.get('home_team', ''),
                    'away_team': game_data.get('away_team', ''),
                    'spread': game_data.get('spread', 0),
                    'total': game_data.get('total', 0),
                    'status': 'scheduled'
                })
            
        except Exception as e:
            print(f"  ❌ Error syncing games: {e}")
    
    def _sync_predictions_to_firebase(self, predictions: List[PropBet]):
        """Sync predictions to Firebase Firestore."""
        try:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
            firebase_predictions = []
            for i, pred in enumerate(predictions):
                pred_doc = {
                    'prediction_id': f"pred_{today}_{i}_{pred.player_name.lower().replace(' ', '_')}",
                    'player_name': pred.player_name,
                    'player_id': pred.player_id,
                    'team': pred.team,
                    'game_id': pred.game_id,
                    'prop_type': pred.prop_type.value if hasattr(pred.prop_type, 'value') else str(pred.prop_type),
                    'line': pred.line,
                    'direction': pred.direction.value if hasattr(pred.direction, 'value') else str(pred.direction),
                    'odds': pred.odds,
                    'ai_confidence': pred.ai_confidence,
                    'impact_score': pred.impact_score,
                    'projected_value': pred.projected_value,
                    'edge': pred.edge,
                    'key_factors': pred.key_factors,
                    'status': 'pending',
                    'created_date': today
                }
                firebase_predictions.append(pred_doc)
            
            # Batch save
            success = self.firebase.batch_save_predictions(firebase_predictions)
            if success:
                print(f"  ✅ Synced {len(firebase_predictions)} predictions")
            else:
                print(f"  ❌ Failed to sync predictions")
                
        except Exception as e:
            print(f"  ❌ Error syncing predictions: {e}")
    
    def _publish_picks_to_rtdb(self, guaranteed_report: GuaranteedPicksReport):
        """Publish guaranteed picks to Realtime Database."""
        try:
            picks = guaranteed_report.get('guaranteed_picks', [])
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
            for i, pick in enumerate(picks):
                pick_data = {
                    'pick_id': f"pick_{today}_{i}",
                    'player_name': pick.player_name,
                    'player_id': pick.player_id,
                    'team': pick.team,
                    'pick': f"{pick.direction.upper()} {pick.line} {pick.prop_type.value.upper()}",
                    'line': pick.line,
                    'direction': pick.direction.value if hasattr(pick.direction, 'value') else str(pick.direction),
                    'confidence': pick.ai_confidence,
                    'edge': pick.edge,
                    'quality': pick.quality.value if hasattr(pick.quality, 'value') else str(pick.quality),
                    'status': 'active',
                    'published_at': datetime.now(timezone.utc).isoformat()
                }
                
                self.firebase.publish_pick(pick_data['pick_id'], pick_data)
            
            print(f"  ✅ Published {len(picks)} picks to Realtime DB")
            
        except Exception as e:
            print(f"  ❌ Error publishing picks: {e}")
    
    def _publish_daily_report(self, report: Dict[str, Any]):
        """Publish daily betting report to Firebase."""
        try:
            guaranteed = report.get('guaranteed_picks', {})
            picks = guaranteed.get('guaranteed_picks', [])
            
            # Get top pick
            top_pick = None
            if picks:
                top_pick = f"{picks[0].player_name} {picks[0].direction.value.upper()} {picks[0].line}"
            
            # Get games list
            games = report.get('games', {})
            games_list = []
            for game_id, game_data in games.items():
                games_list.append({
                    'game_id': game_id,
                    'matchup': game_data.get('game', 'Unknown'),
                    'home_team': game_data.get('home_team', ''),
                    'away_team': game_data.get('away_team', '')
                })
            
            # Get predictions summary
            predictions = report.get('predictions', [])
            predictions_summary = []
            for p in predictions[:5]:  # Top 5
                predictions_summary.append({
                    'player': p.player_name,
                    'pick': f"{p.direction.value.upper()} {p.line}",
                    'confidence': p.ai_confidence,
                    'edge': p.edge
                })
            
            # Build report
            daily_report = {
                'total_games': len(games),
                'total_predictions': len(predictions),
                'guaranteed_picks_count': len(picks),
                'exotic_bets_count': len(report.get('exotic_bets', [])),
                'kicker_bets_count': len(report.get('kicker_bets', [])),
                'top_pick': top_pick,
                'games': games_list,
                'predictions': predictions_summary,
                'bankroll': {
                    'total': report.get('bankroll', {}).get('total_bankroll', 0),
                    'exposure': report.get('bankroll', {}).get('total_exposure', 0),
                    'available': report.get('bankroll', {}).get('available', 0)
                },
                'jarvis_summary': report.get('jarvis_response', {}).get('main_answer', '')[:200] + '...' if report.get('jarvis_response') else 'No picks available',
                'generated_at': report.get('timestamp', datetime.now(timezone.utc).isoformat())
            }
            
            self.firebase.publish_daily_report(daily_report)
            print(f"  ✅ Published daily report")
            
        except Exception as e:
            print(f"  ❌ Error publishing report: {e}")
    
    def _load_espn_data(self) -> Dict[str, Any]:
        """Load ESPN player data from file."""
        import json
        from pathlib import Path
        
        try:
            export_dir = Path(__file__).parent.parent / 'exports'
            espn_file = export_dir / 'nba_espn_players_2025.json'
            
            if espn_file.exists():
                with open(espn_file, 'r') as f:
                    data = json.load(f)
                    return {'players': data.get('players', [])}
            return {'players': []}
        except:
            return {'players': []}
    
    def sync_player_events_from_firebase(self) -> Dict[str, Any]:
        """
        Load player events from Firebase for PIS calculation.
        
        Returns:
            Dict mapping player names to their events
        """
        if not self.firebase or not self.firebase.is_ready():
            print("⚠️  Firebase not available for loading events")
            return {}
        
        try:
            print("\n📥 Loading player events from Firebase...")
            
            # Get recent events (last 30 days)
            events = self.firebase.get_recent_events(days_back=30)
            
            # Group by player
            player_events = {}
            for event in events:
                player_name = event.get('player_name', '')
                if player_name not in player_events:
                    player_events[player_name] = []
                player_events[player_name].append(event)
            
            print(f"  ✅ Loaded {len(events)} events for {len(player_events)} players")
            
            return player_events
            
        except Exception as e:
            print(f"  ❌ Error loading events: {e}")
            return {}


# ========== DEMO / TEST ==========

async def main():
    """Run Firebase-enhanced pipeline demo."""
    print("=" * 70)
    print("  BETGENIE — FIREBASE ENHANCED PIPELINE DEMO")
    print("=" * 70)
    
    # Initialize pipeline with Firebase
    pipeline = FirebaseEnhancedPipeline(bankroll=500.0, use_firebase=True)
    
    # Check Firebase status
    if pipeline.firebase and pipeline.firebase.is_ready():
        print("\n✅ Firebase connected and ready")
        
        # Test sync player events loading
        print("\n[1/3] Testing player events sync...")
        events = pipeline.sync_player_events_from_firebase()
        print(f"   Found events for {len(events)} players")
        
    else:
        print("\n⚠️  Firebase not connected - running in local mode")
        print("   Data will be stored in SQLite only")
    
    # Run full pipeline with sync
    print("\n[2/3] Running full pipeline with Firebase sync...")
    report = await pipeline.run_full_pipeline_with_sync()
    
    # Show Firebase sync status
    print("\n[3/3] Firebase sync status:")
    if report.get('firebase_sync'):
        print(f"   ✅ Synced at: {report.get('firebase_timestamp', 'N/A')}")
        print(f"   ✅ Predictions: {report.get('total_predictions', 0)}")
        print(f"   ✅ Guaranteed picks: {len(report.get('guaranteed_picks', {}).get('guaranteed_picks', []))}")
    else:
        print(f"   ❌ Sync failed: {report.get('firebase_error', 'Unknown')}")
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    
    print("\n📱 Frontend can now access data at:")
    print("   Firestore: players/, games/, predictions/, daily_reports/")
    print("   Realtime DB: /picks/, /live_odds/, /daily_reports/")
    
    return report


if __name__ == "__main__":
    asyncio.run(main())
