"""
BetGenie — FastAPI REST API

Provides REST endpoints for:
- Players (list, get, search)
- Games (today's games, game details)
- Predictions (today's picks, historical accuracy)
- Personal Events (add, list)
- Backtesting (run, results)
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import asyncio

from database import BetGenieDatabase, PlayerDB, GameDB, PersonalEventDB, PredictionDB
from backtester import Backtester, BacktestSummary

# Initialize FastAPI app
app = FastAPI(
    title="BetGenie API",
    description="AI-powered NBA betting intelligence platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = BetGenieDatabase()


# ========== Pydantic Models ==========

class PlayerResponse(BaseModel):
    player_id: str
    full_name: str
    team: str
    position: str
    ppg: float
    rpg: float
    apg: float
    updated_at: str


class GameResponse(BaseModel):
    game_id: str
    home_team: str
    away_team: str
    game_time: str
    home_score: Optional[int]
    away_score: Optional[int]
    status: str


class PersonalEventCreate(BaseModel):
    player_name: str
    category: str
    description: str
    severity: float
    date: str
    source_url: str
    verified: bool = False


class PersonalEventResponse(BaseModel):
    event_id: str
    player_name: str
    category: str
    description: str
    severity: float
    date: str
    source_url: str
    verified: bool


class PredictionResponse(BaseModel):
    prediction_id: str
    player_name: str
    game_id: str
    prop_type: str
    line: float
    direction: str
    projected_value: float
    confidence: float
    edge: float
    result: Optional[str]
    created_at: str


class AccuracyStats(BaseModel):
    total: int
    wins: int
    losses: int
    pushes: int
    win_rate: float


class BacktestRequest(BaseModel):
    player_name: str
    events: List[Dict[str, Any]] = []


class BacktestResponse(BaseModel):
    player_name: str
    total_games: int
    mean_absolute_error: float
    correlation: float
    direction_accuracy: float
    high_pis_accuracy: float
    low_pis_accuracy: float


class HealthResponse(BaseModel):
    status: str
    version: str
    database_connected: bool
    timestamp: str


# ========== Dependency Injection ==========

def get_db():
    """Database dependency."""
    return db


# ========== API Endpoints ==========

@app.get("/", response_model=Dict[str, str])
async def root():
    """API root - welcome message."""
    return {
        "name": "BetGenie API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.get_all_players()
        db_connected = True
    except:
        db_connected = False
    
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        version="1.0.0",
        database_connected=db_connected,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


# ========== PLAYERS ==========

@app.get("/players", response_model=List[PlayerResponse])
async def list_players(
    team: Optional[str] = Query(None, description="Filter by team"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """List all players, optionally filtered by team."""
    if team:
        players = db.get_players_by_team(team)
    else:
        players = db.get_all_players()
    
    # Apply pagination
    players = players[offset:offset + limit]
    
    return [
        PlayerResponse(
            player_id=p.player_id,
            full_name=p.full_name,
            team=p.team,
            position=p.position,
            ppg=p.ppg,
            rpg=p.rpg,
            apg=p.apg,
            updated_at=p.updated_at
        ) for p in players
    ]


@app.get("/players/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    """Get a specific player by ID."""
    player = db.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return PlayerResponse(
        player_id=player.player_id,
        full_name=player.full_name,
        team=player.team,
        position=player.position,
        ppg=player.ppg,
        rpg=player.rpg,
        apg=player.apg,
        updated_at=player.updated_at
    )


@app.get("/players/search/{query}", response_model=List[PlayerResponse])
async def search_players(query: str):
    """Search players by name."""
    all_players = db.get_all_players()
    query_lower = query.lower()
    
    matching = [
        p for p in all_players 
        if query_lower in p.full_name.lower() or query_lower in p.player_id.lower()
    ]
    
    return [
        PlayerResponse(
            player_id=p.player_id,
            full_name=p.full_name,
            team=p.team,
            position=p.position,
            ppg=p.ppg,
            rpg=p.rpg,
            apg=p.apg,
            updated_at=p.updated_at
        ) for p in matching[:20]  # Limit to 20 results
    ]


# ========== GAMES ==========

@app.get("/games/today", response_model=List[GameResponse])
async def get_todays_games():
    """Get all NBA games scheduled for today."""
    games = db.get_todays_games()
    
    return [
        GameResponse(
            game_id=g.game_id,
            home_team=g.home_team,
            away_team=g.away_team,
            game_time=g.game_time,
            home_score=g.home_score,
            away_score=g.away_score,
            status=g.status
        ) for g in games
    ]


# ========== PREDICTIONS ==========

@app.get("/predictions/today", response_model=List[PredictionResponse])
async def get_todays_predictions():
    """Get all predictions for today."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    predictions = db.get_predictions_for_date(today)
    
    return [
        PredictionResponse(
            prediction_id=p.prediction_id,
            player_name=p.player_name,
            game_id=p.game_id,
            prop_type=p.prop_type,
            line=p.line,
            direction=p.direction,
            projected_value=p.projected_value,
            confidence=p.confidence,
            edge=p.edge,
            result=p.result,
            created_at=p.created_at
        ) for p in predictions
    ]


@app.get("/predictions/accuracy", response_model=AccuracyStats)
async def get_prediction_accuracy(days: int = Query(30, ge=1, le=365)):
    """Get prediction accuracy statistics."""
    stats = db.get_prediction_accuracy(days)
    
    return AccuracyStats(
        total=stats["total"],
        wins=stats["wins"],
        losses=stats["losses"],
        pushes=stats["pushes"],
        win_rate=stats["win_rate"]
    )


@app.get("/predictions/best", response_model=List[PredictionResponse])
async def get_best_predictions(min_confidence: float = Query(70.0, ge=0, le=100)):
    """Get best predictions with high confidence."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    predictions = db.get_predictions_for_date(today)
    
    # Filter by confidence
    best = [p for p in predictions if p.confidence >= min_confidence]
    best.sort(key=lambda x: x.confidence, reverse=True)
    
    return [
        PredictionResponse(
            prediction_id=p.prediction_id,
            player_name=p.player_name,
            game_id=p.game_id,
            prop_type=p.prop_type,
            line=p.line,
            direction=p.direction,
            projected_value=p.projected_value,
            confidence=p.confidence,
            edge=p.edge,
            result=p.result,
            created_at=p.created_at
        ) for p in best[:10]  # Top 10
    ]


# ========== PERSONAL EVENTS ==========

@app.post("/events", response_model=PersonalEventResponse)
async def add_personal_event(event: PersonalEventCreate):
    """Add a new personal event for a player."""
    event_id = f"evt-{event.player_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    event_db = PersonalEventDB(
        event_id=event_id,
        player_name=event.player_name,
        category=event.category,
        description=event.description,
        severity=event.severity,
        date=event.date,
        source_url=event.source_url,
        verified=event.verified,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    
    success = db.add_personal_event(event_db)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to add event")
    
    return PersonalEventResponse(
        event_id=event_id,
        player_name=event.player_name,
        category=event.category,
        description=event.description,
        severity=event.severity,
        date=event.date,
        source_url=event.source_url,
        verified=event.verified
    )


@app.get("/events/player/{player_name}", response_model=List[PersonalEventResponse])
async def get_player_events(
    player_name: str,
    days: int = Query(30, ge=1, le=365)
):
    """Get personal events for a specific player."""
    events = db.get_player_events(player_name, days)
    
    return [
        PersonalEventResponse(
            event_id=e.event_id,
            player_name=e.player_name,
            category=e.category,
            description=e.description,
            severity=e.severity,
            date=e.date,
            source_url=e.source_url,
            verified=e.verified
        ) for e in events
    ]


@app.get("/events/recent", response_model=List[PersonalEventResponse])
async def get_recent_events(days: int = Query(7, ge=1, le=30)):
    """Get all recent personal events."""
    events = db.get_all_recent_events(days)
    
    return [
        PersonalEventResponse(
            event_id=e.event_id,
            player_name=e.player_name,
            category=e.category,
            description=e.description,
            severity=e.severity,
            date=e.date,
            source_url=e.source_url,
            verified=e.verified
        ) for e in events
    ]


# ========== BACKTESTING ==========

@app.post("/backtest/player", response_model=BacktestResponse)
async def run_player_backtest(request: BacktestRequest):
    """Run backtest for a specific player."""
    backtester = Backtester(db)
    
    # Convert request events to backtest events
    events = []
    for event in request.events:
        events.append((
            event.get("type", "legal"),
            event.get("date", "2024-01-01"),
            event.get("description", ""),
            event.get("severity", 0.8)
        ))
    
    # Run backtest
    results = backtester.run_player_backtest(request.player_name, events)
    summary = backtester.calculate_summary(results)
    
    return BacktestResponse(
        player_name=request.player_name,
        total_games=summary.total_games,
        mean_absolute_error=summary.mean_absolute_error,
        correlation=summary.correlation,
        direction_accuracy=summary.direction_accuracy,
        high_pis_accuracy=summary.high_pis_accuracy,
        low_pis_accuracy=summary.low_pis_accuracy
    )


@app.get("/backtest/stats", response_model=Dict[str, Any])
async def get_backtest_stats():
    """Get overall backtesting statistics."""
    # This would aggregate all backtest results from database
    return {
        "total_players_backtested": 0,
        "total_games_analyzed": 0,
        "average_mae": 0.0,
        "average_correlation": 0.0,
        "message": "Run backtests to populate statistics"
    }


# ========== STATS & ANALYTICS ==========

@app.get("/stats/dashboard", response_model=Dict[str, Any])
async def get_dashboard_stats():
    """Get dashboard statistics."""
    players = db.get_all_players()
    games = db.get_todays_games()
    accuracy = db.get_prediction_accuracy(30)
    
    return {
        "total_players": len(players),
        "todays_games": len(games),
        "active_teams": len(set(p.team for p in players if p.team)),
        "prediction_accuracy_30d": {
            "total": accuracy["total"],
            "win_rate": round(accuracy["win_rate"], 3)
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/stats/player/{player_name}", response_model=Dict[str, Any])
async def get_player_stats(player_name: str):
    """Get comprehensive stats for a player."""
    # Get player from database
    all_players = db.get_all_players()
    player = next((p for p in all_players if p.full_name.lower() == player_name.lower()), None)
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Get events
    events = db.get_player_events(player_name, 30)
    
    # Get historical performance
    performance = db.get_player_performance_with_pis(player_name)
    
    return {
        "player": {
            "id": player.player_id,
            "name": player.full_name,
            "team": player.team,
            "position": player.position,
            "stats": {
                "ppg": player.ppg,
                "rpg": player.rpg,
                "apg": player.apg
            }
        },
        "recent_events": len(events),
        "events_list": [
            {
                "category": e.category,
                "description": e.description,
                "severity": e.severity,
                "date": e.date
            } for e in events[:5]
        ],
        "games_analyzed": len(performance),
        "last_updated": player.updated_at
    }


# ========== MAIN ==========

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("  BETGENIE API SERVER")
    print("=" * 70)
    print("\nStarting server...")
    print("API Documentation: http://localhost:8001/docs")
    print("Health Check: http://localhost:8001/health")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
