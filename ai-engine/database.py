"""
BetGenie — Database Layer

SQLite database for MVP (can migrate to PostgreSQL later).
Stores: players, games, events, picks, predictions, historical data
"""

import sqlite3
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "betgenie.db"


@dataclass
class PlayerDB:
    player_id: str
    full_name: str
    team: str
    position: str
    ppg: float
    rpg: float
    apg: float
    updated_at: str


@dataclass
class GameDB:
    game_id: str
    home_team: str
    away_team: str
    game_time: str
    home_score: Optional[int]
    away_score: Optional[int]
    status: str
    updated_at: str


@dataclass
class PersonalEventDB:
    event_id: str
    player_name: str
    category: str
    description: str
    severity: float
    date: str
    source_url: str
    verified: bool
    created_at: str


@dataclass
class PredictionDB:
    prediction_id: str
    player_name: str
    game_id: str
    prop_type: str
    line: float
    direction: str
    projected_value: float
    confidence: float
    edge: float
    result: Optional[str]  # 'win', 'loss', 'push', None
    actual_value: Optional[float]
    created_at: str
    resolved_at: Optional[str]


class BetGenieDatabase:
    """SQLite database manager for BetGenie."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(DATABASE_PATH)
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """Initialize all tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    team TEXT,
                    position TEXT,
                    ppg REAL DEFAULT 0,
                    rpg REAL DEFAULT 0,
                    apg REAL DEFAULT 0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Games table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    home_team TEXT NOT NULL,
                    away_team TEXT NOT NULL,
                    game_time TIMESTAMP NOT NULL,
                    home_score INTEGER,
                    away_score INTEGER,
                    status TEXT DEFAULT 'scheduled',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Personal events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personal_events (
                    event_id TEXT PRIMARY KEY,
                    player_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    severity REAL DEFAULT 0.5,
                    date TIMESTAMP,
                    source_url TEXT,
                    verified BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Predictions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    prediction_id TEXT PRIMARY KEY,
                    player_name TEXT NOT NULL,
                    game_id TEXT,
                    prop_type TEXT NOT NULL,
                    line REAL NOT NULL,
                    direction TEXT NOT NULL,
                    projected_value REAL,
                    confidence REAL,
                    edge REAL,
                    result TEXT,
                    actual_value REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP
                )
            """)
            
            # Historical performance table (for backtesting)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    game_date TEXT NOT NULL,
                    points REAL,
                    rebounds REAL,
                    assists REAL,
                    pis_score REAL,
                    events_count INTEGER,
                    opponent TEXT
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_player ON personal_events(player_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_player ON predictions(player_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_game ON predictions(game_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_historical_player ON historical_performance(player_name, game_date)")
            
            conn.commit()
            print(f"Database initialized at {self.db_path}")
    
    # ========== PLAYER OPERATIONS ==========
    
    def upsert_player(self, player: PlayerDB) -> bool:
        """Insert or update a player."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO players (player_id, full_name, team, position, ppg, rpg, apg, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(player_id) DO UPDATE SET
                        team = excluded.team,
                        position = excluded.position,
                        ppg = excluded.ppg,
                        rpg = excluded.rpg,
                        apg = excluded.apg,
                        updated_at = excluded.updated_at
                """, (player.player_id, player.full_name, player.team, player.position,
                      player.ppg, player.rpg, player.apg, player.updated_at))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error upserting player: {e}")
            return False
    
    def get_player(self, player_id: str) -> Optional[PlayerDB]:
        """Get player by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
            row = cursor.fetchone()
            if row:
                return PlayerDB(**dict(row))
            return None
    
    def get_all_players(self) -> List[PlayerDB]:
        """Get all players."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players ORDER BY full_name")
            return [PlayerDB(**dict(row)) for row in cursor.fetchall()]
    
    def get_players_by_team(self, team: str) -> List[PlayerDB]:
        """Get players for a specific team."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE team = ? ORDER BY ppg DESC", (team,))
            return [PlayerDB(**dict(row)) for row in cursor.fetchall()]
    
    # ========== GAME OPERATIONS ==========
    
    def upsert_game(self, game: GameDB) -> bool:
        """Insert or update a game."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO games (game_id, home_team, away_team, game_time, home_score, away_score, status, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(game_id) DO UPDATE SET
                        home_score = excluded.home_score,
                        away_score = excluded.away_score,
                        status = excluded.status,
                        updated_at = excluded.updated_at
                """, (game.game_id, game.home_team, game.away_team, game.game_time,
                      game.home_score, game.away_score, game.status, game.updated_at))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error upserting game: {e}")
            return False
    
    def get_todays_games(self) -> List[GameDB]:
        """Get games for today."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM games 
                WHERE date(game_time) = date('now')
                ORDER BY game_time
            """)
            return [GameDB(**dict(row)) for row in cursor.fetchall()]
    
    # ========== PERSONAL EVENTS OPERATIONS ==========
    
    def add_personal_event(self, event: PersonalEventDB) -> bool:
        """Add a personal event for a player."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO personal_events 
                    (event_id, player_name, category, description, severity, date, source_url, verified, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (event.event_id, event.player_name, event.category, event.description,
                      event.severity, event.date, event.source_url, event.verified, event.created_at))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding personal event: {e}")
            return False
    
    def get_player_events(self, player_name: str, days_back: int = 30) -> List[PersonalEventDB]:
        """Get personal events for a player."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM personal_events 
                WHERE player_name = ? 
                AND date >= datetime('now', '-' || ? || ' days')
                ORDER BY date DESC
            """, (player_name, days_back))
            return [PersonalEventDB(**dict(row)) for row in cursor.fetchall()]
    
    def get_all_recent_events(self, days_back: int = 7) -> List[PersonalEventDB]:
        """Get all recent personal events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM personal_events 
                WHERE date >= datetime('now', '-' || ? || ' days')
                ORDER BY date DESC
            """, (days_back,))
            return [PersonalEventDB(**dict(row)) for row in cursor.fetchall()]
    
    # ========== PREDICTIONS OPERATIONS ==========
    
    def save_prediction(self, prediction: PredictionDB) -> bool:
        """Save a prediction."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO predictions 
                    (prediction_id, player_name, game_id, prop_type, line, direction, 
                     projected_value, confidence, edge, result, actual_value, created_at, resolved_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (prediction.prediction_id, prediction.player_name, prediction.game_id,
                      prediction.prop_type, prediction.line, prediction.direction,
                      prediction.projected_value, prediction.confidence, prediction.edge,
                      prediction.result, prediction.actual_value, prediction.created_at,
                      prediction.resolved_at))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False
    
    def get_predictions_for_date(self, date: str) -> List[PredictionDB]:
        """Get all predictions for a specific date."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM predictions 
                WHERE date(created_at) = ?
                ORDER BY confidence DESC
            """, (date,))
            return [PredictionDB(**dict(row)) for row in cursor.fetchall()]
    
    def resolve_prediction(self, prediction_id: str, result: str, actual_value: float) -> bool:
        """Mark a prediction as resolved with the actual result."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE predictions 
                    SET result = ?, actual_value = ?, resolved_at = ?
                    WHERE prediction_id = ?
                """, (result, actual_value, datetime.now(timezone.utc).isoformat(), prediction_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error resolving prediction: {e}")
            return False
    
    def get_prediction_accuracy(self, days_back: int = 30) -> Dict[str, Any]:
        """Get prediction accuracy stats."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses,
                    SUM(CASE WHEN result = 'push' THEN 1 ELSE 0 END) as pushes,
                    AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as win_rate
                FROM predictions 
                WHERE created_at >= datetime('now', '-' || ? || ' days')
                AND result IS NOT NULL
            """, (days_back,))
            row = cursor.fetchone()
            if row:
                return {
                    "total": row[0],
                    "wins": row[1] or 0,
                    "losses": row[2] or 0,
                    "pushes": row[3] or 0,
                    "win_rate": row[4] or 0
                }
            return {"total": 0, "wins": 0, "losses": 0, "pushes": 0, "win_rate": 0}
    
    # ========== HISTORICAL PERFORMANCE (BACKTESTING) ==========
    
    def add_historical_performance(self, player_name: str, game_date: str, 
                                   points: float, rebounds: float, assists: float,
                                   pis_score: float, events_count: int, opponent: str) -> bool:
        """Add historical game performance for backtesting."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO historical_performance 
                    (player_name, game_date, points, rebounds, assists, pis_score, events_count, opponent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (player_name, game_date, points, rebounds, assists, pis_score, events_count, opponent))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding historical performance: {e}")
            return False
    
    def get_player_performance_with_pis(self, player_name: str) -> List[Dict]:
        """Get player performance data with PIS for correlation analysis."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM historical_performance 
                WHERE player_name = ?
                ORDER BY game_date DESC
            """, (player_name,))
            return [dict(row) for row in cursor.fetchall()]
    
    def clear_all_data(self):
        """Clear all data (use with caution)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players")
            cursor.execute("DELETE FROM games")
            cursor.execute("DELETE FROM personal_events")
            cursor.execute("DELETE FROM predictions")
            cursor.execute("DELETE FROM historical_performance")
            conn.commit()
            print("All database tables cleared")


# ========== DEMO / TEST ==========

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — DATABASE DEMO")
    print("=" * 70)
    
    # Initialize database
    db = BetGenieDatabase()
    
    # Test player operations
    print("\n[1/5] Testing player operations...")
    player = PlayerDB(
        player_id="test-001",
        full_name="Test Player",
        team="Test Team",
        position="PG",
        ppg=25.5,
        rpg=6.2,
        apg=7.1,
        updated_at=datetime.now(timezone.utc).isoformat()
    )
    db.upsert_player(player)
    print(f"  Added player: {player.full_name}")
    
    # Test event operations
    print("\n[2/5] Testing personal events...")
    event = PersonalEventDB(
        event_id="evt-001",
        player_name="Test Player",
        category="legal_arrest",
        description="DUI arrest",
        severity=0.8,
        date=datetime.now(timezone.utc).isoformat(),
        source_url="https://example.com",
        verified=True,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    db.add_personal_event(event)
    print(f"  Added event: {event.description}")
    
    events = db.get_player_events("Test Player")
    print(f"  Retrieved {len(events)} events for player")
    
    # Test prediction operations
    print("\n[3/5] Testing predictions...")
    prediction = PredictionDB(
        prediction_id="pred-001",
        player_name="Test Player",
        game_id="game-001",
        prop_type="points",
        line=22.5,
        direction="over",
        projected_value=26.0,
        confidence=75.0,
        edge=3.5,
        result=None,
        actual_value=None,
        created_at=datetime.now(timezone.utc).isoformat(),
        resolved_at=None
    )
    db.save_prediction(prediction)
    print(f"  Saved prediction: {prediction.player_name} {prediction.direction} {prediction.line}")
    
    # Test resolving prediction
    db.resolve_prediction("pred-001", "win", 28.0)
    print("  Resolved prediction as WIN")
    
    # Test accuracy stats
    accuracy = db.get_prediction_accuracy(30)
    print(f"\n[4/5] Prediction accuracy (last 30 days):")
    print(f"  Total: {accuracy['total']}, Wins: {accuracy['wins']}, Win Rate: {accuracy['win_rate']:.1%}")
    
    # Show all players
    print("\n[5/5] All players in database:")
    players = db.get_all_players()
    for p in players:
        print(f"  - {p.full_name} ({p.team}): {p.ppg} PPG")
    
    print("\n" + "=" * 70)
    print("  DATABASE DEMO COMPLETE")
    print("=" * 70)
