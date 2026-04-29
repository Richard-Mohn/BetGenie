"""
BetGenie — NBA Player Database (Comprehensive)

Includes ALL NBA players - stars, role players, and bench players.
The system analyzes value across the entire roster, not just marquee names.

Strategy: Find undervalued props on role players where lines are soft.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from enum import Enum


class Position(Enum):
    PG = "Point Guard"
    SG = "Shooting Guard"
    SF = "Small Forward"
    PF = "Power Forward"
    C = "Center"


@dataclass
class SeasonStats:
    """Player's current/recent season statistics."""
    season: str
    games_played: int
    minutes_per_game: float
    points_per_game: float = 0.0
    rebounds_per_game: float = 0.0
    assists_per_game: float = 0.0
    field_goal_percentage: float = 0.0
    three_point_percentage: float = 0.0
    free_throw_percentage: float = 0.0


@dataclass
class PersonalEvent:
    """Personal life event that affects performance."""
    date: datetime
    category: str  # legal, family, health, psychological, situational
    description: str
    severity: float  # 0.0-1.0
    public_source: str


@dataclass
class NBAPlayer:
    """NBA player profile - comprehensive for all player types."""
    player_id: str
    full_name: str
    team: str
    position: Position
    age: int
    height: str
    salary: str
    player_tier: str  # "elite", "star", "starter", "role_player", "bench"
    is_all_star: bool
    is_mvp: bool
    public_betting_tendency: str  # "heavy_over", "moderate", "balanced", "light"
    line_softness: str  # "soft", "standard", "sharp" - how soft are betting lines
    current_season: SeasonStats
    career_averages: SeasonStats
    personal_events: List[PersonalEvent] = field(default_factory=list)
    social_media_followers: int = 0
    endorsement_deals: int = 0


# ============================================================
# NBA PLAYER DATABASE (Comprehensive)
# ============================================================

NBA_PLAYERS = {
    # ============================================================
    # ELITE TIER (Maximum public attention, best fade targets)
    # ============================================================
    
    "lebron_james": NBAPlayer(
        player_id="lebron_james",
        full_name="LeBron James",
        team="Los Angeles Lakers",
        position=Position.SF,
        age=41,
        height="6'9\"",
        salary="$47.6M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=71,
            minutes_per_game=35.2,
            points_per_game=25.7,
            rebounds_per_game=7.3,
            assists_per_game=8.3,
            field_goal_percentage=0.515,
            three_point_percentage=0.365,
            free_throw_percentage=0.735
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=1492,
            minutes_per_game=38.2,
            points_per_game=27.2,
            rebounds_per_game=7.5,
            assists_per_game=7.3,
            field_goal_percentage=0.506,
            three_point_percentage=0.350,
            free_throw_percentage=0.735
        ),
        social_media_followers=159000000,  # X followers
        endorsement_deals=15,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 10, 15),
                category="family",
                description="Son Bronny joins Lakers - emotional factor",
                severity=0.3,
                public_source="ESPN"
            )
        ]
    ),
    
    "stephen_curry": NBAPlayer(
        player_id="stephen_curry",
        full_name="Stephen Curry",
        team="Golden State Warriors",
        position=Position.PG,
        age=37,
        height="6'2\"",
        salary="$55.7M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=74,
            minutes_per_game=33.8,
            points_per_game=28.4,
            rebounds_per_game=4.5,
            assists_per_game=5.1,
            field_goal_percentage=0.475,
            three_point_percentage=0.425,
            free_throw_percentage=0.915
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=956,
            minutes_per_game=34.3,
            points_per_game=25.5,
            rebounds_per_game=4.7,
            assists_per_game=6.4,
            field_goal_percentage=0.473,
            three_point_percentage=0.427,
            free_throw_percentage=0.911
        ),
        social_media_followers=16000000,
        endorsement_deals=12,
        personal_events=[]
    ),
    
    "kevin_durant": NBAPlayer(
        player_id="kevin_durant",
        full_name="Kevin Durant",
        team="Phoenix Suns",
        position=Position.PF,
        age=36,
        height="6'11\"",
        salary="$47.6M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=34.2,
            points_per_game=27.8,
            rebounds_per_game=6.5,
            assists_per_game=5.2,
            field_goal_percentage=0.525,
            three_point_percentage=0.405,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=1068,
            minutes_per_game=37.8,
            points_per_game=27.3,
            rebounds_per_game=7.1,
            assists_per_game=4.3,
            field_goal_percentage=0.498,
            three_point_percentage=0.385,
            free_throw_percentage=0.882
        ),
        social_media_followers=12000000,
        endorsement_deals=10,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 6, 20),
                category="psychological",
                description="Public criticism of team management - potential motivation issue",
                severity=0.4,
                public_source="Twitter"
            )
        ]
    ),
    
    "luka_doncic": NBAPlayer(
        player_id="luka_doncic",
        full_name="Luka Dončić",
        team="Dallas Mavericks",
        position=Position.PG,
        age=25,
        height="6'7\"",
        salary="$40.1M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=37.5,
            points_per_game=33.2,
            rebounds_per_game=8.8,
            assists_per_game=9.5,
            field_goal_percentage=0.485,
            three_point_percentage=0.355,
            free_throw_percentage=0.765
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=406,
            minutes_per_game=35.1,
            points_per_game=28.7,
            rebounds_per_game=8.7,
            assists_per_game=8.3,
            field_goal_percentage=0.458,
            three_point_percentage=0.345,
            free_throw_percentage=0.745
        ),
        social_media_followers=4000000,
        endorsement_deals=8,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 7, 10),
                category="family",
                description="Became a father - potential fatigue factor",
                severity=0.2,
                public_source="Instagram"
            )
        ]
    ),
    
    "giannis_antetokounmpo": NBAPlayer(
        player_id="giannis_antetokounmpo",
        full_name="Giannis Antetokounmpo",
        team="Milwaukee Bucks",
        position=Position.PF,
        age=30,
        height="6'11\"",
        salary="$45.6M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=73,
            minutes_per_game=35.8,
            points_per_game=30.2,
            rebounds_per_game=11.5,
            assists_per_game=6.2,
            field_goal_percentage=0.605,
            three_point_percentage=0.285,
            free_throw_percentage=0.655
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=845,
            minutes_per_game=34.2,
            points_per_game=23.4,
            rebounds_per_game=9.8,
            assists_per_game=5.0,
            field_goal_percentage=0.553,
            three_point_percentage=0.295,
            free_throw_percentage=0.715
        ),
        social_media_followers=8000000,
        endorsement_deals=9,
        personal_events=[]
    ),
    
    # ============================================================
    # STAR TIER (High public attention, good fade targets)
    # ============================================================
    
    "joel_embiid": NBAPlayer(
        player_id="joel_embiid",
        full_name="Joel Embiid",
        team="Philadelphia 76ers",
        position=Position.C,
        age=30,
        height="7'0\"",
        salary="$47.6M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=58,
            minutes_per_game=33.8,
            points_per_game=32.5,
            rebounds_per_game=10.8,
            assists_per_game=4.2,
            field_goal_percentage=0.495,
            three_point_percentage=0.365,
            free_throw_percentage=0.835
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=433,
            minutes_per_game=33.6,
            points_per_game=27.9,
            rebounds_per_game=11.2,
            assists_per_game=3.6,
            field_goal_percentage=0.498,
            three_point_percentage=0.335,
            free_throw_percentage=0.825
        ),
        social_media_followers=3000000,
        endorsement_deals=7,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 2, 15),
                category="health",
                description="Knee injury - ongoing concern",
                severity=0.5,
                public_source="ESPN"
            )
        ]
    ),
    
    "jayson_tatum": NBAPlayer(
        player_id="jayson_tatum",
        full_name="Jayson Tatum",
        team="Boston Celtics",
        position=Position.SF,
        age=26,
        height="6'8\"",
        salary="$32.0M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=77,
            minutes_per_game=36.5,
            points_per_game=28.5,
            rebounds_per_game=8.2,
            assists_per_game=4.5,
            field_goal_percentage=0.475,
            three_point_percentage=0.375,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=567,
            minutes_per_game=35.2,
            points_per_game=23.6,
            rebounds_per_game=7.3,
            assists_per_game=3.5,
            field_goal_percentage=0.458,
            three_point_percentage=0.375,
            free_throw_percentage=0.835
        ),
        social_media_followers=2500000,
        endorsement_deals=6,
        personal_events=[]
    ),
    
    "anthony_edwards": NBAPlayer(
        player_id="anthony_edwards",
        full_name="Anthony Edwards",
        team="Minnesota Timberwolves",
        position=Position.SG,
        age=23,
        height="6'4\"",
        salary="$13.5M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=79,
            minutes_per_game=35.8,
            points_per_game=27.8,
            rebounds_per_game=5.5,
            assists_per_game=5.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.365,
            free_throw_percentage=0.805
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=312,
            minutes_per_game=34.5,
            points_per_game=22.9,
            rebounds_per_game=5.2,
            assists_per_game=4.1,
            field_goal_percentage=0.445,
            three_point_percentage=0.355,
            free_throw_percentage=0.785
        ),
        social_media_followers=1500000,
        endorsement_deals=5,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 8, 20),
                category="psychological",
                description="Major shoe deal announcement - potential distraction",
                severity=0.2,
                public_source="Nike"
            )
        ]
    ),
    
    "shai_gilgeous_alexander": NBAPlayer(
        player_id="shai_gilgeous_alexander",
        full_name="Shai Gilgeous-Alexander",
        team="Oklahoma City Thunder",
        position=Position.PG,
        age=26,
        height="6'6\"",
        salary="$33.4M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.2,
            points_per_game=31.2,
            rebounds_per_game=5.8,
            assists_per_game=6.2,
            field_goal_percentage=0.535,
            three_point_percentage=0.335,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=456,
            minutes_per_game=33.8,
            points_per_game=24.8,
            rebounds_per_game=5.2,
            assists_per_game=5.4,
            field_goal_percentage=0.475,
            three_point_percentage=0.335,
            free_throw_percentage=0.865
        ),
        social_media_followers=800000,
        endorsement_deals=4,
        personal_events=[]
    ),
    
    "victor_wembanyama": NBAPlayer(
        player_id="victor_wembanyama",
        full_name="Victor Wembanyama",
        team="San Antonio Spurs",
        position=Position.C,
        age=21,
        height="7'4\"",
        salary="$12.7M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=32.5,
            points_per_game=24.5,
            rebounds_per_game=11.2,
            assists_per_game=3.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.325,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=145,
            minutes_per_game=31.8,
            points_per_game=21.5,
            rebounds_per_game=10.5,
            assists_per_game=3.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.315,
            free_throw_percentage=0.805
        ),
        social_media_followers=2000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    # ============================================================
    # EMERGING STARS (Growing public attention)
    # ============================================================
    
    "tyrese_haliburton": NBAPlayer(
        player_id="tyrese_haliburton",
        full_name="Tyrese Haliburton",
        team="Indiana Pacers",
        position=Position.PG,
        age=24,
        height="6'6\"",
        salary="$5.8M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=35.2,
            points_per_game=23.5,
            rebounds_per_game=4.2,
            assists_per_game=11.8,
            field_goal_percentage=0.485,
            three_point_percentage=0.405,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=287,
            minutes_per_game=33.5,
            points_per_game=18.8,
            rebounds_per_game=4.0,
            assists_per_game=9.2,
            field_goal_percentage=0.475,
            three_point_percentage=0.405,
            free_throw_percentage=0.865
        ),
        social_media_followers=500000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "paolo_banchero": NBAPlayer(
        player_id="paolo_banchero",
        full_name="Paolo Banchero",
        team="Orlando Magic",
        position=Position.PF,
        age=22,
        height="6'10\"",
        salary="$11.3M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=34.8,
            points_per_game=26.2,
            rebounds_per_game=7.5,
            assists_per_game=5.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.335,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=159,
            minutes_per_game=34.2,
            points_per_game=22.8,
            rebounds_per_game=6.8,
            assists_per_game=4.8,
            field_goal_percentage=0.455,
            three_point_percentage=0.315,
            free_throw_percentage=0.745
        ),
        social_media_followers=400000,
        endorsement_deals=4,
        personal_events=[]
    ),
    
    # ============================================================
    # STARTER TIER (Regular starters, moderate lines)
    # ============================================================
    
    "michael_porter_jr": NBAPlayer(
        player_id="michael_porter_jr",
        full_name="Michael Porter Jr.",
        team="Denver Nuggets",
        position=Position.SF,
        age=26,
        height="6'10\"",
        salary="$15.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",  # Lines are softer on non-stars
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=31.5,
            points_per_game=18.2,
            rebounds_per_game=6.8,
            assists_per_game=2.5,
            field_goal_percentage=0.475,
            three_point_percentage=0.395,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=356,
            minutes_per_game=29.8,
            points_per_game=14.8,
            rebounds_per_game=6.2,
            assists_per_game=1.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.405,
            free_throw_percentage=0.795
        ),
        social_media_followers=200000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "derrick_white": NBAPlayer(
        player_id="derrick_white",
        full_name="Derrick White",
        team="Boston Celtics",
        position=Position.PG,
        age=30,
        height="6'4\"",
        salary="$18.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=32.2,
            points_per_game=15.8,
            rebounds_per_game=4.2,
            assists_per_game=5.0,
            field_goal_percentage=0.465,
            three_point_percentage=0.385,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=512,
            minutes_per_game=28.5,
            points_per_game=12.5,
            rebounds_per_game=3.8,
            assists_per_game=3.8,
            field_goal_percentage=0.455,
            three_point_percentage=0.355,
            free_throw_percentage=0.865
        ),
        social_media_followers=150000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    # ============================================================
    # ROLE PLAYER TIER (Bench players, very soft lines)
    # ============================================================
    
    "malik_monk": NBAPlayer(
        player_id="malik_monk",
        full_name="Malik Monk",
        team="Sacramento Kings",
        position=Position.SG,
        age=27,
        height="6'3\"",
        salary="$10.8M",
        player_tier="role_player",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",  # Very soft lines on bench players
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=26.5,
            points_per_game=15.2,
            rebounds_per_game=3.2,
            assists_per_game=4.0,
            field_goal_percentage=0.455,
            three_point_percentage=0.345,
            free_throw_percentage=0.835
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=428,
            minutes_per_game=22.8,
            points_per_game=11.8,
            rebounds_per_game=2.8,
            assists_per_game=2.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.335,
            free_throw_percentage=0.815
        ),
        social_media_followers=100000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "austin_reaves": NBAPlayer(
        player_id="austin_reaves",
        full_name="Austin Reaves",
        team="Los Angeles Lakers",
        position=Position.SG,
        age=26,
        height="6'5\"",
        salary="$12.9M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=77,
            minutes_per_game=32.8,
            points_per_game=17.5,
            rebounds_per_game=4.2,
            assists_per_game=5.5,
            field_goal_percentage=0.485,
            three_point_percentage=0.375,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=245,
            minutes_per_game=29.5,
            points_per_game=14.2,
            rebounds_per_game=3.8,
            assists_per_game=4.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.855
        ),
        social_media_followers=500000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "immanuel_quickley": NBAPlayer(
        player_id="immanuel_quickley",
        full_name="Immanuel Quickley",
        team="Toronto Raptors",
        position=Position.PG,
        age=25,
        height="6'3\"",
        salary="$12.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=33.5,
            points_per_game=18.8,
            rebounds_per_game=4.0,
            assists_per_game=6.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.385,
            free_throw_percentage=0.855
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=312,
            minutes_per_game=26.8,
            points_per_game=13.5,
            rebounds_per_game=3.5,
            assists_per_game=4.0,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.845
        ),
        social_media_followers=80000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "reed_sheppard": NBAPlayer(
        player_id="reed_sheppard",
        full_name="Reed Sheppard",
        team="Houston Rockets",
        position=Position.SG,
        age=20,
        height="6'6\"",
        salary="$4.8M",
        player_tier="role_player",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=65,
            minutes_per_game=18.5,
            points_per_game=8.5,
            rebounds_per_game=2.5,
            assists_per_game=2.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.375,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=65,
            minutes_per_game=18.5,
            points_per_game=8.5,
            rebounds_per_game=2.5,
            assists_per_game=2.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.375,
            free_throw_percentage=0.825
        ),
        social_media_followers=50000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    # ============================================================
    # ADDITIONAL ROLE PLAYERS AND STARTERS (Expanding to 30 teams)
    # ============================================================
    
    "trae_young": NBAPlayer(
        player_id="trae_young",
        full_name="Trae Young",
        team="Atlanta Hawks",
        position=Position.PG,
        age=26,
        height="6'1\"",
        salary="$40.1M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=73,
            minutes_per_game=36.2,
            points_per_game=28.5,
            rebounds_per_game=3.8,
            assists_per_game=10.2,
            field_goal_percentage=0.435,
            three_point_percentage=0.365,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=468,
            minutes_per_game=34.5,
            points_per_game=25.5,
            rebounds_per_game=3.8,
            assists_per_game=9.5,
            field_goal_percentage=0.435,
            three_point_percentage=0.355,
            free_throw_percentage=0.865
        ),
        social_media_followers=3000000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "deandre_ayton": NBAPlayer(
        player_id="deandre_ayton",
        full_name="Deandre Ayton",
        team="Portland Trail Blazers",
        position=Position.C,
        age=26,
        height="7'0\"",
        salary="$32.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=32.5,
            points_per_game=18.2,
            rebounds_per_game=11.5,
            assists_per_game=2.2,
            field_goal_percentage=0.585,
            three_point_percentage=0.125,
            free_throw_percentage=0.765
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=432,
            minutes_per_game=31.2,
            points_per_game=16.8,
            rebounds_per_game=10.5,
            assists_per_game=1.8,
            field_goal_percentage=0.575,
            three_point_percentage=0.145,
            free_throw_percentage=0.755
        ),
        social_media_followers=400000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "jalen_brunson": NBAPlayer(
        player_id="jalen_brunson",
        full_name="Jalen Brunson",
        team="New York Knicks",
        position=Position.PG,
        age=28,
        height="6'2\"",
        salary="$24.9M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=35.8,
            points_per_game=24.5,
            rebounds_per_game=3.8,
            assists_per_game=6.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.405,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=412,
            minutes_per_game=29.8,
            points_per_game=16.8,
            rebounds_per_game=3.2,
            assists_per_game=4.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.375,
            free_throw_percentage=0.825
        ),
        social_media_followers=600000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "jalen_green": NBAPlayer(
        player_id="jalen_green",
        full_name="Jalen Green",
        team="Houston Rockets",
        position=Position.SG,
        age=23,
        height="6'4\"",
        salary="$12.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=74,
            minutes_per_game=31.5,
            points_per_game=19.8,
            rebounds_per_game=4.2,
            assists_per_game=3.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.335,
            free_throw_percentage=0.805
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=268,
            minutes_per_game=30.8,
            points_per_game=17.5,
            rebounds_per_game=4.0,
            assists_per_game=3.2,
            field_goal_percentage=0.415,
            three_point_percentage=0.325,
            free_throw_percentage=0.795
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "alperen_sengun": NBAPlayer(
        player_id="alperen_sengun",
        full_name="Alperen Şengün",
        team="Houston Rockets",
        position=Position.C,
        age=22,
        height="6'11\"",
        salary="$5.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=32.8,
            points_per_game=21.2,
            rebounds_per_game=9.5,
            assists_per_game=5.2,
            field_goal_percentage=0.535,
            three_point_percentage=0.315,
            free_throw_percentage=0.715
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=242,
            minutes_per_game=28.5,
            points_per_game=15.8,
            rebounds_per_game=8.5,
            assists_per_game=4.0,
            field_goal_percentage=0.515,
            three_point_percentage=0.305,
            free_throw_percentage=0.705
        ),
        social_media_followers=300000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "desmond_bane": NBAPlayer(
        player_id="desmond_bane",
        full_name="Desmond Bane",
        team="Memphis Grizzlies",
        position=Position.SG,
        age=26,
        height="6'5\"",
        salary="$19.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=33.2,
            points_per_game=22.5,
            rebounds_per_game=4.8,
            assists_per_game=4.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.385,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=285,
            minutes_per_game=29.5,
            points_per_game=16.8,
            rebounds_per_game=4.2,
            assists_per_game=3.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.405,
            free_throw_percentage=0.855
        ),
        social_media_followers=200000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "ja_morant": NBAPlayer(
        player_id="ja_morant",
        full_name="Ja Morant",
        team="Memphis Grizzlies",
        position=Position.PG,
        age=25,
        height="6'3\"",
        salary="$34.0M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=32.5,
            points_per_game=25.8,
            rebounds_per_game=5.5,
            assists_per_game=8.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.315,
            free_throw_percentage=0.785
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=318,
            minutes_per_game=32.2,
            points_per_game=22.5,
            rebounds_per_game=5.0,
            assists_per_game=7.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.315,
            free_throw_percentage=0.755
        ),
        social_media_followers=8000000,
        endorsement_deals=8,
        personal_events=[
            PersonalEvent(
                date=datetime(2023, 3, 4),
                category="legal",
                description="Suspension for conduct off court",
                severity=0.7,
                public_source="NBA"
            )
        ]
    ),
    
    "zion_williamson": NBAPlayer(
        player_id="zion_williamson",
        full_name="Zion Williamson",
        team="New Orleans Pelicans",
        position=Position.PF,
        age=24,
        height="6'6\"",
        salary="$33.5M",
        player_tier="star",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=55,
            minutes_per_game=30.5,
            points_per_game=22.8,
            rebounds_per_game=6.2,
            assists_per_game=4.5,
            field_goal_percentage=0.585,
            three_point_percentage=0.255,
            free_throw_percentage=0.695
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=184,
            minutes_per_game=30.2,
            points_per_game=24.0,
            rebounds_per_game=6.5,
            assists_per_game=4.2,
            field_goal_percentage=0.585,
            three_point_percentage=0.315,
            free_throw_percentage=0.675
        ),
        social_media_followers=4000000,
        endorsement_deals=6,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 1, 15),
                category="health",
                description="Hamstring injury - ongoing concern",
                severity=0.5,
                public_source="ESPN"
            )
        ]
    ),
    
    "brandon_ingram": NBAPlayer(
        player_id="brandon_ingram",
        full_name="Brandon Ingram",
        team="New Orleans Pelicans",
        position=Position.SF,
        age=27,
        height="6'8\"",
        salary="$31.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=62,
            minutes_per_game=32.8,
            points_per_game=20.5,
            rebounds_per_game=5.5,
            assists_per_game=5.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.345,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=485,
            minutes_per_game=33.5,
            points_per_game=19.5,
            rebounds_per_game=5.2,
            assists_per_game=4.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.815
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "coby_white": NBAPlayer(
        player_id="coby_white",
        full_name="Coby White",
        team="Chicago Bulls",
        position=Position.PG,
        age=24,
        height="6'5\"",
        salary="$6.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=28.5,
            points_per_game=16.2,
            rebounds_per_game=4.0,
            assists_per_game=4.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=328,
            minutes_per_game=24.8,
            points_per_game=13.5,
            rebounds_per_game=3.2,
            assists_per_game=3.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.355,
            free_throw_percentage=0.805
        ),
        social_media_followers=150000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "nikola_vucevic": NBAPlayer(
        player_id="nikola_vucevic",
        full_name="Nikola Vučević",
        team="Chicago Bulls",
        position=Position.C,
        age=34,
        height="6'10\"",
        salary="$20.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=30.2,
            points_per_game=17.5,
            rebounds_per_game=10.8,
            assists_per_game=3.2,
            field_goal_percentage=0.485,
            three_point_percentage=0.285,
            free_throw_percentage=0.835
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=925,
            minutes_per_game=31.5,
            points_per_game=17.2,
            rebounds_per_game=10.8,
            assists_per_game=2.8,
            field_goal_percentage=0.495,
            three_point_percentage=0.345,
            free_throw_percentage=0.795
        ),
        social_media_followers=300000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing expansion to 30 teams
    # ============================================================
    
    "kawhi_leonard": NBAPlayer(
        player_id="kawhi_leonard",
        full_name="Kawhi Leonard",
        team="Los Angeles Clippers",
        position=Position.SF,
        age=32,
        height="6'7\"",
        salary="$45.6M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=34.5,
            points_per_game=23.5,
            rebounds_per_game=6.2,
            assists_per_game=3.8,
            field_goal_percentage=0.515,
            three_point_percentage=0.425,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=695,
            minutes_per_game=32.8,
            points_per_game=19.8,
            rebounds_per_game=6.5,
            assists_per_game=3.0,
            field_goal_percentage=0.495,
            three_point_percentage=0.385,
            free_throw_percentage=0.855
        ),
        social_media_followers=3000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    "paul_george": NBAPlayer(
        player_id="paul_george",
        full_name="Paul George",
        team="Los Angeles Clippers",
        position=Position.SF,
        age=34,
        height="6'8\"",
        salary="$45.6M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=74,
            minutes_per_game=33.8,
            points_per_game=22.8,
            rebounds_per_game=5.5,
            assists_per_game=4.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.395,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=842,
            minutes_per_game=34.2,
            points_per_game=20.5,
            rebounds_per_game=6.5,
            assists_per_game=3.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.375,
            free_throw_percentage=0.845
        ),
        social_media_followers=5000000,
        endorsement_deals=10,
        personal_events=[]
    ),
    
    "james_harden": NBAPlayer(
        player_id="james_harden",
        full_name="James Harden",
        team="Los Angeles Clippers",
        position=Position.SG,
        age=35,
        height="6'5\"",
        salary="$35.6M",
        player_tier="star",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=34.2,
            points_per_game=16.5,
            rebounds_per_game=5.8,
            assists_per_game=8.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=1045,
            minutes_per_game=34.5,
            points_per_game=24.2,
            rebounds_per_game=5.6,
            assists_per_game=7.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.865
        ),
        social_media_followers=8000000,
        endorsement_deals=12,
        personal_events=[]
    ),
    
    "devin_booker": NBAPlayer(
        player_id="devin_booker",
        full_name="Devin Booker",
        team="Phoenix Suns",
        position=Position.SG,
        age=28,
        height="6'5\"",
        salary="$36.0M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=35.5,
            points_per_game=27.8,
            rebounds_per_game=5.2,
            assists_per_game=6.8,
            field_goal_percentage=0.485,
            three_point_percentage=0.355,
            free_throw_percentage=0.885
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=565,
            minutes_per_game=34.2,
            points_per_game=23.8,
            rebounds_per_game=4.8,
            assists_per_game=5.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.345,
            free_throw_percentage=0.875
        ),
        social_media_followers=4000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    "bradley_beal": NBAPlayer(
        player_id="bradley_beal",
        full_name="Bradley Beal",
        team="Phoenix Suns",
        position=Position.SG,
        age=31,
        height="6'5\"",
        salary="$50.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=33.5,
            points_per_game=18.2,
            rebounds_per_game=4.2,
            assists_per_game=4.5,
            field_goal_percentage=0.445,
            three_point_percentage=0.325,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=785,
            minutes_per_game=34.8,
            points_per_game=22.2,
            rebounds_per_game=4.2,
            assists_per_game=4.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.355,
            free_throw_percentage=0.825
        ),
        social_media_followers=2000000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "kyrie_irving": NBAPlayer(
        player_id="kyrie_irving",
        full_name="Kyrie Irving",
        team="Dallas Mavericks",
        position=Position.PG,
        age=32,
        height="6'2\"",
        salary="$40.1M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=33.8,
            points_per_game=25.5,
            rebounds_per_game=5.0,
            assists_per_game=5.5,
            field_goal_percentage=0.485,
            three_point_percentage=0.405,
            free_throw_percentage=0.915
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=725,
            minutes_per_game=34.2,
            points_per_game=23.5,
            rebounds_per_game=4.8,
            assists_per_game=5.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.395,
            free_throw_percentage=0.895
        ),
        social_media_followers=12000000,
        endorsement_deals=15,
        personal_events=[]
    ),
    
    "klay_thompson": NBAPlayer(
        player_id="klay_thompson",
        full_name="Klay Thompson",
        team="Golden State Warriors",
        position=Position.SG,
        age=34,
        height="6'6\"",
        salary="$43.2M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=77,
            minutes_per_game=30.5,
            points_per_game=19.8,
            rebounds_per_game=3.8,
            assists_per_game=2.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.415,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=792,
            minutes_per_game=32.8,
            points_per_game=19.8,
            rebounds_per_game=4.2,
            assists_per_game=2.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.415,
            free_throw_percentage=0.855
        ),
        social_media_followers=3000000,
        endorsement_deals=6,
        personal_events=[]
    ),
    
    "draymond_green": NBAPlayer(
        player_id="draymond_green",
        full_name="Draymond Green",
        team="Golden State Warriors",
        position=Position.PF,
        age=34,
        height="6'6\"",
        salary="$27.6M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=28.5,
            points_per_game=8.5,
            rebounds_per_game=7.2,
            assists_per_game=6.5,
            field_goal_percentage=0.495,
            three_point_percentage=0.285,
            free_throw_percentage=0.715
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=832,
            minutes_per_game=30.2,
            points_per_game=8.8,
            rebounds_per_game=7.0,
            assists_per_game=5.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.315,
            free_throw_percentage=0.705
        ),
        social_media_followers=2000000,
        endorsement_deals=4,
        personal_events=[
            PersonalEvent(
                date=datetime(2022, 10, 5),
                category="legal",
                description="Suspension for practice altercation",
                severity=0.6,
                public_source="NBA"
            )
        ]
    ),
    
    "damian_lillard": NBAPlayer(
        player_id="damian_lillard",
        full_name="Damian Lillard",
        team="Milwaukee Bucks",
        position=Position.PG,
        age=34,
        height="6'2\"",
        salary="$45.6M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="heavy_over",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=73,
            minutes_per_game=35.2,
            points_per_game=24.5,
            rebounds_per_game=4.5,
            assists_per_game=7.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.915
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=862,
            minutes_per_game=35.5,
            points_per_game=25.0,
            rebounds_per_game=4.2,
            assists_per_game=6.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.365,
            free_throw_percentage=0.895
        ),
        social_media_followers=8000000,
        endorsement_deals=12,
        personal_events=[]
    ),
    
    "khris_middleton": NBAPlayer(
        player_id="khris_middleton",
        full_name="Khris Middleton",
        team="Milwaukee Bucks",
        position=Position.SF,
        age=33,
        height="6'7\"",
        salary="$31.7M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=65,
            minutes_per_game=28.5,
            points_per_game=15.2,
            rebounds_per_game=5.0,
            assists_per_game=4.0,
            field_goal_percentage=0.465,
            three_point_percentage=0.375,
            free_throw_percentage=0.835
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=725,
            minutes_per_game=31.2,
            points_per_game=17.0,
            rebounds_per_game=5.5,
            assists_per_game=4.0,
            field_goal_percentage=0.455,
            three_point_percentage=0.375,
            free_throw_percentage=0.855
        ),
        social_media_followers=800000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "jrue_holiday": NBAPlayer(
        player_id="jrue_holiday",
        full_name="Jrue Holiday",
        team="Boston Celtics",
        position=Position.PG,
        age=34,
        height="6'4\"",
        salary="$36.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.8,
            points_per_game=12.8,
            rebounds_per_game=5.5,
            assists_per_game=6.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.395,
            free_throw_percentage=0.805
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=1085,
            minutes_per_game=32.5,
            points_per_game=15.2,
            rebounds_per_game=4.5,
            assists_per_game=6.5,
            field_goal_percentage=0.455,
            three_point_percentage=0.365,
            free_throw_percentage=0.795
        ),
        social_media_followers=1000000,
        endorsement_deals=4,
        personal_events=[]
    ),
    
    "jaylen_brown": NBAPlayer(
        player_id="jaylen_brown",
        full_name="Jaylen Brown",
        team="Boston Celtics",
        position=Position.SF,
        age=28,
        height="6'6\"",
        salary="$28.5M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=35.5,
            points_per_game=23.5,
            rebounds_per_game=5.8,
            assists_per_game=3.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.345,
            free_throw_percentage=0.765
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=542,
            minutes_per_game=33.8,
            points_per_game=18.8,
            rebounds_per_game=5.2,
            assists_per_game=3.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.345,
            free_throw_percentage=0.745
        ),
        social_media_followers=1500000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "kristaps_porzingis": NBAPlayer(
        player_id="kristaps_porzingis",
        full_name="Kristaps Porziņgis",
        team="Boston Celtics",
        position=Position.C,
        age=29,
        height="7'2\"",
        salary="$28.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=29.5,
            points_per_game=19.8,
            rebounds_per_game=7.2,
            assists_per_game=2.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.355,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=458,
            minutes_per_game=30.8,
            points_per_game=18.5,
            rebounds_per_game=8.0,
            assists_per_game=1.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.355,
            free_throw_percentage=0.825
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 4, 15),
                category="health",
                description="Calf strain - day-to-day",
                severity=0.4,
                public_source="ESPN"
            )
        ]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing expansion to cover all 30 teams
    # ============================================================
    
    "tyler_herro": NBAPlayer(
        player_id="tyler_herro",
        full_name="Tyler Herro",
        team="Miami Heat",
        position=Position.SG,
        age=25,
        height="6'5\"",
        salary="$30.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=33.5,
            points_per_game=20.5,
            rebounds_per_game=5.2,
            assists_per_game=4.5,
            field_goal_percentage=0.435,
            three_point_percentage=0.375,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=355,
            minutes_per_game=31.2,
            points_per_game=18.8,
            rebounds_per_game=5.0,
            assists_per_game=4.2,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.855
        ),
        social_media_followers=1000000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "jimmy_butler": NBAPlayer(
        player_id="jimmy_butler",
        full_name="Jimmy Butler",
        team="Miami Heat",
        position=Position.SF,
        age=35,
        height="6'7\"",
        salary="$45.2M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=60,
            minutes_per_game=33.8,
            points_per_game=21.2,
            rebounds_per_game=5.8,
            assists_per_game=5.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.325,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=892,
            minutes_per_game=34.5,
            points_per_game=18.5,
            rebounds_per_game=6.2,
            assists_per_game=4.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.315,
            free_throw_percentage=0.835
        ),
        social_media_followers=4000000,
        endorsement_deals=6,
        personal_events=[]
    ),
    
    "bam_adebayo": NBAPlayer(
        player_id="bam_adebayo",
        full_name="Bam Adebayo",
        team="Miami Heat",
        position=Position.C,
        age=27,
        height="6'9\"",
        salary="$32.6M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.2,
            points_per_game=19.5,
            rebounds_per_game=10.2,
            assists_per_game=4.0,
            field_goal_percentage=0.525,
            three_point_percentage=0.145,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=465,
            minutes_per_game=33.8,
            points_per_game=18.2,
            rebounds_per_game=9.5,
            assists_per_game=3.8,
            field_goal_percentage=0.515,
            three_point_percentage=0.125,
            free_throw_percentage=0.785
        ),
        social_media_followers=2000000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "scottie_barnes": NBAPlayer(
        player_id="scottie_barnes",
        full_name="Scottie Barnes",
        team="Toronto Raptors",
        position=Position.PF,
        age=23,
        height="6'7\"",
        salary="$22.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=35.5,
            points_per_game=21.8,
            rebounds_per_game=8.2,
            assists_per_game=6.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.325,
            free_throw_percentage=0.785
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=278,
            minutes_per_game=34.2,
            points_per_game=16.5,
            rebounds_per_game=7.5,
            assists_per_game=5.0,
            field_goal_percentage=0.465,
            three_point_percentage=0.295,
            free_throw_percentage=0.765
        ),
        social_media_followers=300000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "rj_barrett": NBAPlayer(
        player_id="rj_barrett",
        full_name="RJ Barrett",
        team="Toronto Raptors",
        position=Position.SF,
        age=24,
        height="6'6\"",
        salary="$23.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.8,
            points_per_game=19.2,
            rebounds_per_game=5.8,
            assists_per_game=4.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.315,
            free_throw_percentage=0.735
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=385,
            minutes_per_game=34.2,
            points_per_game=18.2,
            rebounds_per_game=5.5,
            assists_per_game=3.2,
            field_goal_percentage=0.435,
            three_point_percentage=0.325,
            free_throw_percentage=0.725
        ),
        social_media_followers=400000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "paolo_banchero": NBAPlayer(
        player_id="paolo_banchero",
        full_name="Paolo Banchero",
        team="Orlando Magic",
        position=Position.PF,
        age=22,
        height="6'10\"",
        salary="$11.8M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=80,
            minutes_per_game=35.2,
            points_per_game=22.8,
            rebounds_per_game=6.8,
            assists_per_game=5.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.325,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=242,
            minutes_per_game=34.5,
            points_per_game=20.5,
            rebounds_per_game=6.5,
            assists_per_game=4.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.315,
            free_throw_percentage=0.765
        ),
        social_media_followers=500000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "franz_wagner": NBAPlayer(
        player_id="franz_wagner",
        full_name="Franz Wagner",
        team="Orlando Magic",
        position=Position.SF,
        age=23,
        height="6'10\"",
        salary="$5.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.5,
            points_per_game=18.5,
            rebounds_per_game=4.5,
            assists_per_game=3.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.345,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=242,
            minutes_per_game=31.8,
            points_per_game=16.8,
            rebounds_per_game=4.2,
            assists_per_game=3.0,
            field_goal_percentage=0.455,
            three_point_percentage=0.335,
            free_throw_percentage=0.815
        ),
        social_media_followers=200000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "jalen_suggs": NBAPlayer(
        player_id="jalen_suggs",
        full_name="Jalen Suggs",
        team="Orlando Magic",
        position=Position.PG,
        age=23,
        height="6'5\"",
        salary="$6.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=28.5,
            points_per_game=12.8,
            rebounds_per_game=3.8,
            assists_per_game=3.5,
            field_goal_percentage=0.435,
            three_point_percentage=0.345,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=198,
            minutes_per_game=26.8,
            points_per_game=11.5,
            rebounds_per_game=3.5,
            assists_per_game=3.2,
            field_goal_percentage=0.405,
            three_point_percentage=0.315,
            free_throw_percentage=0.765
        ),
        social_media_followers=150000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "la_melo_ball": NBAPlayer(
        player_id="la_melo_ball",
        full_name="LaMelo Ball",
        team="Charlotte Hornets",
        position=Position.PG,
        age=23,
        height="6'7\"",
        salary="$26.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=65,
            minutes_per_game=32.5,
            points_per_game=23.5,
            rebounds_per_game=6.2,
            assists_per_game=8.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.355,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=225,
            minutes_per_game=32.8,
            points_per_game=19.8,
            rebounds_per_game=6.0,
            assists_per_game=7.8,
            field_goal_percentage=0.415,
            three_point_percentage=0.345,
            free_throw_percentage=0.815
        ),
        social_media_followers=5000000,
        endorsement_deals=8,
        personal_events=[
            PersonalEvent(
                date=datetime(2025, 3, 10),
                category="health",
                description="Ankle injury - missed 10 games",
                severity=0.5,
                public_source="ESPN"
            )
        ]
    ),
    
    "brandon_miller": NBAPlayer(
        player_id="brandon_miller",
        full_name="Brandon Miller",
        team="Charlotte Hornets",
        position=Position.SF,
        age=21,
        height="6'9\"",
        salary="$6.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=30.5,
            points_per_game=15.2,
            rebounds_per_game=5.0,
            assists_per_game=2.2,
            field_goal_percentage=0.415,
            three_point_percentage=0.355,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=145,
            minutes_per_game=29.8,
            points_per_game=14.5,
            rebounds_per_game=4.8,
            assists_per_game=2.0,
            field_goal_percentage=0.405,
            three_point_percentage=0.345,
            free_throw_percentage=0.785
        ),
        social_media_followers=100000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "mark_williams": NBAPlayer(
        player_id="mark_williams",
        full_name="Mark Williams",
        team="Charlotte Hornets",
        position=Position.C,
        age=23,
        height="7'0\"",
        salary="$5.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=55,
            minutes_per_game=26.5,
            points_per_game=12.5,
            rebounds_per_game=9.8,
            assists_per_game=1.2,
            field_goal_percentage=0.625,
            three_point_percentage=0.000,
            free_throw_percentage=0.685
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=115,
            minutes_per_game=25.8,
            points_per_game=11.8,
            rebounds_per_game=9.2,
            assists_per_game=1.0,
            field_goal_percentage=0.615,
            three_point_percentage=0.000,
            free_throw_percentage=0.675
        ),
        social_media_followers=50000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    "tyus_jones": NBAPlayer(
        player_id="tyus_jones",
        full_name="Tyus Jones",
        team="Washington Wizards",
        position=Position.PG,
        age=28,
        height="6'1\"",
        salary="$13.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=29.5,
            points_per_game=12.2,
            rebounds_per_game=3.2,
            assists_per_game=7.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.355,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=525,
            minutes_per_game=24.8,
            points_per_game=10.5,
            rebounds_per_game=2.8,
            assists_per_game=4.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.335,
            free_throw_percentage=0.805
        ),
        social_media_followers=200000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "kyle_kuzma": NBAPlayer(
        player_id="kyle_kuzma",
        full_name="Kyle Kuzma",
        team="Washington Wizards",
        position=Position.PF,
        age=29,
        height="6'9\"",
        salary="$22.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=32.8,
            points_per_game=18.5,
            rebounds_per_game=6.8,
            assists_per_game=3.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.335,
            free_throw_percentage=0.755
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=525,
            minutes_per_game=30.5,
            points_per_game=16.2,
            rebounds_per_game=6.2,
            assists_per_game=3.0,
            field_goal_percentage=0.435,
            three_point_percentage=0.325,
            free_throw_percentage=0.735
        ),
        social_media_followers=1500000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "jordan_poole": NBAPlayer(
        player_id="jordan_poole",
        full_name="Jordan Poole",
        team="Washington Wizards",
        position=Position.SG,
        age=25,
        height="6'4\"",
        salary="$28.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=31.5,
            points_per_game=20.2,
            rebounds_per_game=3.2,
            assists_per_game=4.5,
            field_goal_percentage=0.415,
            three_point_percentage=0.325,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=385,
            minutes_per_game=26.8,
            points_per_game=15.2,
            rebounds_per_game=2.8,
            assists_per_game=3.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.335,
            free_throw_percentage=0.845
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "tyrese_maxey": NBAPlayer(
        player_id="tyrese_maxey",
        full_name="Tyrese Maxey",
        team="Philadelphia 76ers",
        position=Position.SG,
        age=24,
        height="6'2\"",
        salary="$4.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=33.8,
            points_per_game=22.5,
            rebounds_per_game=3.8,
            assists_per_game=5.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=285,
            minutes_per_game=28.5,
            points_per_game=15.8,
            rebounds_per_game=3.0,
            assists_per_game=3.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.355,
            free_throw_percentage=0.835
        ),
        social_media_followers=400000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "tobias_harris": NBAPlayer(
        player_id="tobias_harris",
        full_name="Tobias Harris",
        team="Philadelphia 76ers",
        position=Position.PF,
        age=32,
        height="6'8\"",
        salary="$39.4M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.5,
            points_per_game=17.5,
            rebounds_per_game=6.2,
            assists_per_game=3.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.345,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=925,
            minutes_per_game=31.8,
            points_per_game=16.2,
            rebounds_per_game=6.5,
            assists_per_game=2.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.345,
            free_throw_percentage=0.805
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "darius_garland": NBAPlayer(
        player_id="darius_garland",
        full_name="Darius Garland",
        team="Cleveland Cavaliers",
        position=Position.PG,
        age=25,
        height="6'1\"",
        salary="$23.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=33.5,
            points_per_game=18.5,
            rebounds_per_game=2.8,
            assists_per_game=7.8,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.875
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=358,
            minutes_per_game=32.8,
            points_per_game=17.8,
            rebounds_per_game=3.0,
            assists_per_game=7.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.365,
            free_throw_percentage=0.865
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "donovan_mitchell": NBAPlayer(
        player_id="donovan_mitchell",
        full_name="Donovan Mitchell",
        team="Cleveland Cavaliers",
        position=Position.SG,
        age=28,
        height="6'1\"",
        salary="$33.5M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=35.2,
            points_per_game=26.8,
            rebounds_per_game=5.0,
            assists_per_game=6.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=485,
            minutes_per_game=34.5,
            points_per_game=24.5,
            rebounds_per_game=4.5,
            assists_per_game=5.0,
            field_goal_percentage=0.435,
            three_point_percentage=0.355,
            free_throw_percentage=0.835
        ),
        social_media_followers=3000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    "evan_mobley": NBAPlayer(
        player_id="evan_mobley",
        full_name="Evan Mobley",
        team="Cleveland Cavaliers",
        position=Position.C,
        age=24,
        height="6'11\"",
        salary="$13.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=31.5,
            points_per_game=15.8,
            rebounds_per_game=8.8,
            assists_per_game=2.8,
            field_goal_percentage=0.545,
            three_point_percentage=0.315,
            free_throw_percentage=0.735
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=245,
            minutes_per_game=30.8,
            points_per_game=15.2,
            rebounds_per_game=8.5,
            assists_per_game=2.5,
            field_goal_percentage=0.525,
            three_point_percentage=0.305,
            free_throw_percentage=0.715
        ),
        social_media_followers=300000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "jarrett_allen": NBAPlayer(
        player_id="jarrett_allen",
        full_name="Jarrett Allen",
        team="Cleveland Cavaliers",
        position=Position.C,
        age=26,
        height="6'11\"",
        salary="$20.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=30.2,
            points_per_game=14.5,
            rebounds_per_game=10.2,
            assists_per_game=2.5,
            field_goal_percentage=0.635,
            three_point_percentage=0.000,
            free_throw_percentage=0.715
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=485,
            minutes_per_game=30.5,
            points_per_game=12.8,
            rebounds_per_game=9.8,
            assists_per_game=2.2,
            field_goal_percentage=0.615,
            three_point_percentage=0.045,
            free_throw_percentage=0.705
        ),
        social_media_followers=400000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "cade_cunningham": NBAPlayer(
        player_id="cade_cunningham",
        full_name="Cade Cunningham",
        team="Detroit Pistons",
        position=Position.PG,
        age=23,
        height="6'6\"",
        salary="$11.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=35.8,
            points_per_game=22.5,
            rebounds_per_game=6.8,
            assists_per_game=8.2,
            field_goal_percentage=0.435,
            three_point_percentage=0.325,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=225,
            minutes_per_game=34.5,
            points_per_game=19.8,
            rebounds_per_game=6.2,
            assists_per_game=7.5,
            field_goal_percentage=0.415,
            three_point_percentage=0.315,
            free_throw_percentage=0.815
        ),
        social_media_followers=400000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "jaden_ivey": NBAPlayer(
        player_id="jaden_ivey",
        full_name="Jaden Ivey",
        team="Detroit Pistons",
        position=Position.SG,
        age=22,
        height="6'4\"",
        salary="$6.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=30.5,
            points_per_game=15.8,
            rebounds_per_game=4.2,
            assists_per_game=5.0,
            field_goal_percentage=0.425,
            three_point_percentage=0.325,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=155,
            minutes_per_game=29.8,
            points_per_game=14.5,
            rebounds_per_game=4.0,
            assists_per_game=4.5,
            field_goal_percentage=0.415,
            three_point_percentage=0.315,
            free_throw_percentage=0.765
        ),
        social_media_followers=150000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "ausar_thompson": NBAPlayer(
        player_id="ausar_thompson",
        full_name="Ausar Thompson",
        team="Detroit Pistons",
        position=Position.SF,
        age=21,
        height="6'7\"",
        salary="$5.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=25.5,
            points_per_game=8.5,
            rebounds_per_game=6.2,
            assists_per_game=2.2,
            field_goal_percentage=0.415,
            three_point_percentage=0.225,
            free_throw_percentage=0.695
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=135,
            minutes_per_game=24.8,
            points_per_game=8.0,
            rebounds_per_game=6.0,
            assists_per_game=2.0,
            field_goal_percentage=0.405,
            three_point_percentage=0.215,
            free_throw_percentage=0.685
        ),
        social_media_followers=50000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    "jalen_duren": NBAPlayer(
        player_id="jalen_duren",
        full_name="Jalen Duren",
        team="Detroit Pistons",
        position=Position.C,
        age=21,
        height="6'11\"",
        salary="$2.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=24.5,
            points_per_game=8.8,
            rebounds_per_game=9.5,
            assists_per_game=1.0,
            field_goal_percentage=0.605,
            three_point_percentage=0.000,
            free_throw_percentage=0.635
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=145,
            minutes_per_game=23.8,
            points_per_game=8.2,
            rebounds_per_game=9.0,
            assists_per_game=0.8,
            field_goal_percentage=0.595,
            three_point_percentage=0.000,
            free_throw_percentage=0.625
        ),
        social_media_followers=50000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "anthony_edwards": NBAPlayer(
        player_id="anthony_edwards",
        full_name="Anthony Edwards",
        team="Minnesota Timberwolves",
        position=Position.SG,
        age=23,
        height="6'4\"",
        salary="$42.1M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=79,
            minutes_per_game=35.8,
            points_per_game=25.8,
            rebounds_per_game=5.5,
            assists_per_game=5.2,
            field_goal_percentage=0.445,
            three_point_percentage=0.355,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=315,
            minutes_per_game=34.5,
            points_per_game=22.5,
            rebounds_per_game=5.2,
            assists_per_game=4.5,
            field_goal_percentage=0.435,
            three_point_percentage=0.345,
            free_throw_percentage=0.795
        ),
        social_media_followers=3000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    "karl_anthony_towns": NBAPlayer(
        player_id="karl_anthony_towns",
        full_name="Karl-Anthony Towns",
        team="Minnesota Timberwolves",
        position=Position.C,
        age=29,
        height="6'11\"",
        salary="$49.2M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=32.5,
            points_per_game=21.5,
            rebounds_per_game=9.2,
            assists_per_game=3.5,
            field_goal_percentage=0.505,
            three_point_percentage=0.415,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=565,
            minutes_per_game=33.8,
            points_per_game=22.8,
            rebounds_per_game=11.2,
            assists_per_game=3.2,
            field_goal_percentage=0.515,
            three_point_percentage=0.395,
            free_throw_percentage=0.835
        ),
        social_media_followers=2000000,
        endorsement_deals=6,
        personal_events=[]
    ),
    
    "rudy_gobert": NBAPlayer(
        player_id="rudy_gobert",
        full_name="Rudy Gobert",
        team="Minnesota Timberwolves",
        position=Position.C,
        age=31,
        height="7'1\"",
        salary="$43.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=30.8,
            points_per_game=13.5,
            rebounds_per_game=12.5,
            assists_per_game=1.2,
            field_goal_percentage=0.645,
            three_point_percentage=0.000,
            free_throw_percentage=0.655
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=725,
            minutes_per_game=31.5,
            points_per_game=13.0,
            rebounds_per_game=12.5,
            assists_per_game=1.2,
            field_goal_percentage=0.655,
            three_point_percentage=0.015,
            free_throw_percentage=0.645
        ),
        social_media_followers=1000000,
        endorsement_deals=4,
        personal_events=[]
    ),
    
    "mike_conley": NBAPlayer(
        player_id="mike_conley",
        full_name="Mike Conley",
        team="Minnesota Timberwolves",
        position=Position.PG,
        age=37,
        height="6'1\"",
        salary="$24.4M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=28.5,
            points_per_game=10.8,
            rebounds_per_game=3.0,
            assists_per_game=6.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.385,
            free_throw_percentage=0.835
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=1175,
            minutes_per_game=30.8,
            points_per_game=14.8,
            rebounds_per_game=3.0,
            assists_per_game=5.8,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.825
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "jalen_williams": NBAPlayer(
        player_id="jalen_williams",
        full_name="Jalen Williams",
        team="Oklahoma City Thunder",
        position=Position.SF,
        age=23,
        height="6'6\"",
        salary="$5.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.8,
            points_per_game=19.5,
            rebounds_per_game=4.8,
            assists_per_game=5.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.355,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=225,
            minutes_per_game=31.5,
            points_per_game=17.8,
            rebounds_per_game=4.5,
            assists_per_game=4.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.345,
            free_throw_percentage=0.775
        ),
        social_media_followers=200000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "chet_holmgren": NBAPlayer(
        player_id="chet_holmgren",
        full_name="Chet Holmgren",
        team="Oklahoma City Thunder",
        position=Position.C,
        age=22,
        height="7'0\"",
        salary="$12.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=80,
            minutes_per_game=30.5,
            points_per_game=17.5,
            rebounds_per_game=8.2,
            assists_per_game=2.5,
            field_goal_percentage=0.475,
            three_point_percentage=0.375,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=160,
            minutes_per_game=29.8,
            points_per_game=16.8,
            rebounds_per_game=7.8,
            assists_per_game=2.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.785
        ),
        social_media_followers=400000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "josh_giddey": NBAPlayer(
        player_id="josh_giddey",
        full_name="Josh Giddey",
        team="Oklahoma City Thunder",
        position=Position.PG,
        age=23,
        height="6'8\"",
        salary="$8.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=29.5,
            points_per_game=12.5,
            rebounds_per_game=6.8,
            assists_per_game=4.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.315,
            free_throw_percentage=0.765
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=245,
            minutes_per_game=28.8,
            points_per_game=11.8,
            rebounds_per_game=6.5,
            assists_per_game=4.5,
            field_goal_percentage=0.435,
            three_point_percentage=0.305,
            free_throw_percentage=0.755
        ),
        social_media_followers=300000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "lauri_markkanen": NBAPlayer(
        player_id="lauri_markkanen",
        full_name="Lauri Markkanen",
        team="Utah Jazz",
        position=Position.PF,
        age=27,
        height="7'0\"",
        salary="$18.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.5,
            points_per_game=24.5,
            rebounds_per_game=8.5,
            assists_per_game=2.2,
            field_goal_percentage=0.475,
            three_point_percentage=0.385,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=485,
            minutes_per_game=30.8,
            points_per_game=17.5,
            rebounds_per_game=7.2,
            assists_per_game=2.0,
            field_goal_percentage=0.445,
            three_point_percentage=0.355,
            free_throw_percentage=0.835
        ),
        social_media_followers=500000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "collin sexton": NBAPlayer(
        player_id="collin_sexton",
        full_name="Collin Sexton",
        team="Utah Jazz",
        position=Position.SG,
        age=26,
        height="6'2\"",
        salary="$18.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.5,
            points_per_game=18.5,
            rebounds_per_game=3.2,
            assists_per_game=4.5,
            field_goal_percentage=0.455,
            three_point_percentage=0.365,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=425,
            minutes_per_game=30.2,
            points_per_game=16.8,
            rebounds_per_game=3.0,
            assists_per_game=4.0,
            field_goal_percentage=0.445,
            three_point_percentage=0.345,
            free_throw_percentage=0.785
        ),
        social_media_followers=400000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "walker_kessler": NBAPlayer(
        player_id="walker_kessler",
        full_name="Walker Kessler",
        team="Utah Jazz",
        position=Position.C,
        age=23,
        height="7'0\"",
        salary="$5.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=25.5,
            points_per_game=9.5,
            rebounds_per_game=8.8,
            assists_per_game=1.0,
            field_goal_percentage=0.655,
            three_point_percentage=0.000,
            free_throw_percentage=0.645
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=145,
            minutes_per_game=24.8,
            points_per_game=8.8,
            rebounds_per_game=8.5,
            assists_per_game=0.8,
            field_goal_percentage=0.645,
            three_point_percentage=0.000,
            free_throw_percentage=0.635
        ),
        social_media_followers=50000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    "keyonte_george": NBAPlayer(
        player_id="keyonte_george",
        full_name="Keyonte George",
        team="Utah Jazz",
        position=Position.SG,
        age=21,
        height="6'4\"",
        salary="$6.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=30.5,
            points_per_game=14.5,
            rebounds_per_game=4.2,
            assists_per_game=3.0,
            field_goal_percentage=0.395,
            three_point_percentage=0.325,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=150,
            minutes_per_game=29.8,
            points_per_game=13.8,
            rebounds_per_game=4.0,
            assists_per_game=2.8,
            field_goal_percentage=0.385,
            three_point_percentage=0.315,
            free_throw_percentage=0.765
        ),
        social_media_followers=100000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "michael_porter_jr": NBAPlayer(
        player_id="michael_porter_jr",
        full_name="Michael Porter Jr",
        team="Denver Nuggets",
        position=Position.SF,
        age=27,
        height="6'10\"",
        salary="$33.1M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=33.5,
            points_per_game=18.8,
            rebounds_per_game=6.8,
            assists_per_game=1.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.385,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=325,
            minutes_per_game=30.8,
            points_per_game=16.5,
            rebounds_per_game=6.5,
            assists_per_game=1.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.375,
            free_throw_percentage=0.815
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "jamal_murray": NBAPlayer(
        player_id="jamal_murray",
        full_name="Jamal Murray",
        team="Denver Nuggets",
        position=Position.PG,
        age=27,
        height="6'4\"",
        salary="$33.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=32.5,
            points_per_game=20.5,
            rebounds_per_game=4.0,
            assists_per_game=6.5,
            field_goal_percentage=0.455,
            three_point_percentage=0.375,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=455,
            minutes_per_game=31.8,
            points_per_game=17.5,
            rebounds_per_game=3.8,
            assists_per_game=5.8,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.855
        ),
        social_media_followers=1500000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "aaron_gordon": NBAPlayer(
        player_id="aaron_gordon",
        full_name="Aaron Gordon",
        team="Denver Nuggets",
        position=Position.PF,
        age=29,
        height="6'8\"",
        salary="$22.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=30.2,
            points_per_game=13.8,
            rebounds_per_game=6.5,
            assists_per_game=3.2,
            field_goal_percentage=0.545,
            three_point_percentage=0.325,
            free_throw_percentage=0.695
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=695,
            minutes_per_game=30.5,
            points_per_game=13.5,
            rebounds_per_game=6.5,
            assists_per_game=3.0,
            field_goal_percentage=0.475,
            three_point_percentage=0.335,
            free_throw_percentage=0.685
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "kentavious_caldwell_pope": NBAPlayer(
        player_id="kentavious_caldwell_pope",
        full_name="Kentavious Caldwell-Pope",
        team="Denver Nuggets",
        position=Position.SG,
        age=31,
        height="6'5\"",
        salary="$14.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=76,
            minutes_per_game=30.5,
            points_per_game=10.5,
            rebounds_per_game=3.8,
            assists_per_game=2.2,
            field_goal_percentage=0.455,
            three_point_percentage=0.395,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=785,
            minutes_per_game=28.8,
            points_per_game=11.8,
            rebounds_per_game=3.5,
            assists_per_game=1.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.375,
            free_throw_percentage=0.795
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "nikola_jokic": NBAPlayer(
        player_id="nikola_jokic",
        full_name="Nikola Jokić",
        team="Denver Nuggets",
        position=Position.C,
        age=30,
        height="6'11\"",
        salary="$51.4M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=True,
        public_betting_tendency="moderate",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.5,
            points_per_game=26.5,
            rebounds_per_game=12.5,
            assists_per_game=9.8,
            field_goal_percentage=0.595,
            three_point_percentage=0.345,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=695,
            minutes_per_game=32.8,
            points_per_game=24.8,
            rebounds_per_game=12.2,
            assists_per_game=8.8,
            field_goal_percentage=0.585,
            three_point_percentage=0.335,
            free_throw_percentage=0.805
        ),
        social_media_followers=5000000,
        endorsement_deals=10,
        personal_events=[]
    ),
    
    "mitchell_robinson": NBAPlayer(
        player_id="mitchell_robinson",
        full_name="Mitchell Robinson",
        team="New York Knicks",
        position=Position.C,
        age=26,
        height="7'0\"",
        salary="$14.3M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=28.5,
            points_per_game=8.5,
            rebounds_per_game=10.2,
            assists_per_game=0.8,
            field_goal_percentage=0.625,
            three_point_percentage=0.000,
            free_throw_percentage=0.545
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=325,
            minutes_per_game=25.8,
            points_per_game=7.5,
            rebounds_per_game=9.0,
            assists_per_game=0.8,
            field_goal_percentage=0.615,
            three_point_percentage=0.015,
            free_throw_percentage=0.535
        ),
        social_media_followers=300000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "quentin_grimes": NBAPlayer(
        player_id="quentin_grimes",
        full_name="Quentin Grimes",
        team="New York Knicks",
        position=Position.SG,
        age=24,
        height="6'5\"",
        salary="$2.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=26.5,
            points_per_game=8.5,
            rebounds_per_game=3.5,
            assists_per_game=1.8,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=185,
            minutes_per_game=24.8,
            points_per_game=7.8,
            rebounds_per_game=3.2,
            assists_per_game=1.5,
            field_goal_percentage=0.415,
            three_point_percentage=0.355,
            free_throw_percentage=0.765
        ),
        social_media_followers=100000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "domantas_sabonis": NBAPlayer(
        player_id="domantas_sabonis",
        full_name="Domantas Sabonis",
        team="Sacramento Kings",
        position=Position.C,
        age=28,
        height="6'11\"",
        salary="$30.5M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=34.5,
            points_per_game=19.5,
            rebounds_per_game=13.2,
            assists_per_game=8.0,
            field_goal_percentage=0.595,
            three_point_percentage=0.375,
            free_throw_percentage=0.745
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=525,
            minutes_per_game=32.8,
            points_per_game=17.8,
            rebounds_per_game=11.8,
            assists_per_game=5.8,
            field_goal_percentage=0.545,
            three_point_percentage=0.325,
            free_throw_percentage=0.735
        ),
        social_media_followers=1000000,
        endorsement_deals=4,
        personal_events=[]
    ),
    
    "de'aaron_fox": NBAPlayer(
        player_id="deaaron_fox",
        full_name="De'Aaron Fox",
        team="Sacramento Kings",
        position=Position.PG,
        age=27,
        height="6'3\"",
        salary="$32.5M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=35.8,
            points_per_game=26.2,
            rebounds_per_game=4.5,
            assists_per_game=6.2,
            field_goal_percentage=0.465,
            three_point_percentage=0.325,
            free_throw_percentage=0.765
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=485,
            minutes_per_game=33.5,
            points_per_game=21.5,
            rebounds_per_game=4.2,
            assists_per_game=5.8,
            field_goal_percentage=0.455,
            three_point_percentage=0.315,
            free_throw_percentage=0.745
        ),
        social_media_followers=2000000,
        endorsement_deals=6,
        personal_events=[]
    ),
    
    "keegan_murray": NBAPlayer(
        player_id="keegan_murray",
        full_name="Keegan Murray",
        team="Sacramento Kings",
        position=Position.SF,
        age=24,
        height="6'8\"",
        salary="$8.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=32.5,
            points_per_game=15.5,
            rebounds_per_game=5.8,
            assists_per_game=1.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.365,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=155,
            minutes_per_game=31.8,
            points_per_game=14.8,
            rebounds_per_game=5.5,
            assists_per_game=1.5,
            field_goal_percentage=0.465,
            three_point_percentage=0.355,
            free_throw_percentage=0.785
        ),
        social_media_followers=200000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "harrison_barnes": NBAPlayer(
        player_id="harrison_barnes",
        full_name="Harrison Barnes",
        team="Sacramento Kings",
        position=Position.PF,
        age=32,
        height="6'8\"",
        salary="$18.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=30.2,
            points_per_game=12.5,
            rebounds_per_game=5.8,
            assists_per_game=1.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.375,
            free_throw_percentage=0.815
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=825,
            minutes_per_game=31.5,
            points_per_game=14.2,
            rebounds_per_game=5.5,
            assists_per_game=2.0,
            field_goal_percentage=0.465,
            three_point_percentage=0.365,
            free_throw_percentage=0.805
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "anthony_davis": NBAPlayer(
        player_id="anthony_davis",
        full_name="Anthony Davis",
        team="Los Angeles Lakers",
        position=Position.C,
        age=31,
        height="6'10\"",
        salary="$43.2M",
        player_tier="elite",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="sharp",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=34.5,
            points_per_game=24.5,
            rebounds_per_game=12.5,
            assists_per_game=3.2,
            field_goal_percentage=0.555,
            three_point_percentage=0.315,
            free_throw_percentage=0.825
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=725,
            minutes_per_game=33.8,
            points_per_game=24.0,
            rebounds_per_game=10.8,
            assists_per_game=2.8,
            field_goal_percentage=0.515,
            three_point_percentage=0.305,
            free_throw_percentage=0.805
        ),
        social_media_followers=10000000,
        endorsement_deals=15,
        personal_events=[]
    ),
    
    "dangelo_russell": NBAPlayer(
        player_id="dangelo_russell",
        full_name="D'Angelo Russell",
        team="Los Angeles Lakers",
        position=Position.PG,
        age=28,
        height="6'4\"",
        salary="$18.7M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=29.5,
            points_per_game=15.5,
            rebounds_per_game=3.2,
            assists_per_game=6.2,
            field_goal_percentage=0.435,
            three_point_percentage=0.385,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=525,
            minutes_per_game=29.2,
            points_per_game=17.2,
            rebounds_per_game=3.5,
            assists_per_game=5.5,
            field_goal_percentage=0.425,
            three_point_percentage=0.365,
            free_throw_percentage=0.775
        ),
        social_media_followers=2000000,
        endorsement_deals=5,
        personal_events=[]
    ),
    
    "rui_hachimura": NBAPlayer(
        player_id="rui_hachimura",
        full_name="Rui Hachimura",
        team="Los Angeles Lakers",
        position=Position.PF,
        age=26,
        height="6'8\"",
        salary="$17.0M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=28.5,
            points_per_game=13.5,
            rebounds_per_game=5.2,
            assists_per_game=1.8,
            field_goal_percentage=0.485,
            three_point_percentage=0.355,
            free_throw_percentage=0.775
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=345,
            minutes_per_game=26.8,
            points_per_game=12.2,
            rebounds_per_game=4.8,
            assists_per_game=1.5,
            field_goal_percentage=0.475,
            three_point_percentage=0.345,
            free_throw_percentage=0.765
        ),
        social_media_followers=1000000,
        endorsement_deals=8,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "pj_washington": NBAPlayer(
        player_id="pj_washington",
        full_name="P.J. Washington",
        team="Dallas Mavericks",
        position=Position.PF,
        age=25,
        height="6'7\"",
        salary="$15.5M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=30.5,
            points_per_game=12.5,
            rebounds_per_game=5.8,
            assists_per_game=2.2,
            field_goal_percentage=0.435,
            three_point_percentage=0.355,
            free_throw_percentage=0.795
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=325,
            minutes_per_game=27.8,
            points_per_game=10.8,
            rebounds_per_game=5.2,
            assists_per_game=1.8,
            field_goal_percentage=0.425,
            three_point_percentage=0.345,
            free_throw_percentage=0.785
        ),
        social_media_followers=300000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "derrick_lively": NBAPlayer(
        player_id="derrick_lively",
        full_name="Derrick Lively II",
        team="Dallas Mavericks",
        position=Position.C,
        age=21,
        height="7'1\"",
        salary="$4.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=24.5,
            points_per_game=8.5,
            rebounds_per_game=8.2,
            assists_per_game=1.5,
            field_goal_percentage=0.685,
            three_point_percentage=0.000,
            free_throw_percentage=0.615
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=145,
            minutes_per_game=23.8,
            points_per_game=7.8,
            rebounds_per_game=7.8,
            assists_per_game=1.2,
            field_goal_percentage=0.675,
            three_point_percentage=0.000,
            free_throw_percentage=0.605
        ),
        social_media_followers=100000,
        endorsement_deals=0,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "dejounte_murray": NBAPlayer(
        player_id="dejounte_murray",
        full_name="Dejounte Murray",
        team="Atlanta Hawks",
        position=Position.SG,
        age=28,
        height="6'5\"",
        salary="$18.2M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=78,
            minutes_per_game=35.5,
            points_per_game=21.5,
            rebounds_per_game=5.2,
            assists_per_game=6.0,
            field_goal_percentage=0.445,
            three_point_percentage=0.365,
            free_throw_percentage=0.805
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=425,
            minutes_per_game=32.8,
            points_per_game=16.8,
            rebounds_per_game=5.5,
            assists_per_game=5.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.345,
            free_throw_percentage=0.785
        ),
        social_media_followers=1000000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    "clint_capela": NBAPlayer(
        player_id="clint_capela",
        full_name="Clint Capela",
        team="Atlanta Hawks",
        position=Position.C,
        age=30,
        height="6'11\"",
        salary="$22.3M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=26.5,
            points_per_game=11.5,
            rebounds_per_game=11.2,
            assists_per_game=0.8,
            field_goal_percentage=0.625,
            three_point_percentage=0.000,
            free_throw_percentage=0.595
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=545,
            minutes_per_game=27.8,
            points_per_game=12.0,
            rebounds_per_game=10.5,
            assists_per_game=0.8,
            field_goal_percentage=0.615,
            three_point_percentage=0.015,
            free_throw_percentage=0.585
        ),
        social_media_followers=500000,
        endorsement_deals=2,
        personal_events=[]
    ),
    
    "bogdan_bogdanovic": NBAPlayer(
        player_id="bogdan_bogdanovic",
        full_name="Bogdan Bogdanović",
        team="Atlanta Hawks",
        position=Position.SF,
        age=32,
        height="6'6\"",
        salary="$18.7M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=72,
            minutes_per_game=30.5,
            points_per_game=16.5,
            rebounds_per_game=3.5,
            assists_per_game=3.0,
            field_goal_percentage=0.445,
            three_point_percentage=0.375,
            free_throw_percentage=0.845
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=365,
            minutes_per_game=29.2,
            points_per_game=15.2,
            rebounds_per_game=3.5,
            assists_per_game=2.8,
            field_goal_percentage=0.435,
            three_point_percentage=0.365,
            free_throw_percentage=0.835
        ),
        social_media_followers=800000,
        endorsement_deals=3,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "wendell_carter_jr": NBAPlayer(
        player_id="wendell_carter_jr",
        full_name="Wendell Carter Jr",
        team="Orlando Magic",
        position=Position.C,
        age=25,
        height="6'10\"",
        salary="$12.8M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=70,
            minutes_per_game=28.5,
            points_per_game=11.5,
            rebounds_per_game=9.2,
            assists_per_game=2.2,
            field_goal_percentage=0.535,
            three_point_percentage=0.345,
            free_throw_percentage=0.735
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=355,
            minutes_per_game=27.2,
            points_per_game=11.0,
            rebounds_per_game=8.8,
            assists_per_game=2.0,
            field_goal_percentage=0.525,
            three_point_percentage=0.335,
            free_throw_percentage=0.725
        ),
        social_media_followers=200000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    "moe_wagner": NBAPlayer(
        player_id="moe_wagner",
        full_name="Moritz Wagner",
        team="Orlando Magic",
        position=Position.PF,
        age=27,
        height="6'11\"",
        salary="$8.0M",
        player_tier="bench",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=65,
            minutes_per_game=18.5,
            points_per_game=9.5,
            rebounds_per_game=4.5,
            assists_per_game=1.5,
            field_goal_percentage=0.515,
            three_point_percentage=0.325,
            free_throw_percentage=0.785
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=285,
            minutes_per_game=17.2,
            points_per_game=8.2,
            rebounds_per_game=4.0,
            assists_per_game=1.2,
            field_goal_percentage=0.505,
            three_point_percentage=0.315,
            free_throw_percentage=0.775
        ),
        social_media_followers=100000,
        endorsement_deals=1,
        personal_events=[]
    ),
    
    # ============================================================
    # MORE PLAYERS - Continuing to cover all 30 teams
    # ============================================================
    
    "klay_thompson": NBAPlayer(
        player_id="klay_thompson",
        full_name="Klay Thompson",
        team="Golden State Warriors",
        position=Position.SG,
        age=34,
        height="6'6\"",
        salary="$43.2M",
        player_tier="star",
        is_all_star=True,
        is_mvp=False,
        public_betting_tendency="moderate",
        line_softness="standard",
        current_season=SeasonStats(
            season="2025-26",
            games_played=75,
            minutes_per_game=32.5,
            points_per_game=21.5,
            rebounds_per_game=4.2,
            assists_per_game=2.8,
            field_goal_percentage=0.455,
            three_point_percentage=0.415,
            free_throw_percentage=0.865
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=765,
            minutes_per_game=33.8,
            points_per_game=19.8,
            rebounds_per_game=4.0,
            assists_per_game=2.5,
            field_goal_percentage=0.445,
            three_point_percentage=0.415,
            free_throw_percentage=0.855
        ),
        social_media_followers=8000000,
        endorsement_deals=12,
        personal_events=[]
    ),
    
    "draymond_green": NBAPlayer(
        player_id="draymond_green",
        full_name="Draymond Green",
        team="Golden State Warriors",
        position=Position.PF,
        age=34,
        height="6'6\"",
        salary="$27.6M",
        player_tier="starter",
        is_all_star=False,
        is_mvp=False,
        public_betting_tendency="light",
        line_softness="soft",
        current_season=SeasonStats(
            season="2025-26",
            games_played=68,
            minutes_per_game=28.5,
            points_per_game=8.5,
            rebounds_per_game=7.5,
            assists_per_game=6.5,
            field_goal_percentage=0.495,
            three_point_percentage=0.345,
            free_throw_percentage=0.725
        ),
        career_averages=SeasonStats(
            season="Career",
            games_played=795,
            minutes_per_game=30.2,
            points_per_game=8.8,
            rebounds_per_game=7.0,
            assists_per_game=5.8,
            field_goal_percentage=0.475,
            three_point_percentage=0.315,
            free_throw_percentage=0.715
        ),
        social_media_followers=5000000,
        endorsement_deals=8,
        personal_events=[]
    ),
}


def get_player(player_id: str) -> Optional[NBAPlayer]:
    """Get a player by ID."""
    return NBA_PLAYERS.get(player_id)


def get_all_players() -> List[NBAPlayer]:
    """Get all players."""
    return list(NBA_PLAYERS.values())


def get_players_by_tier(tier: str) -> List[NBAPlayer]:
    """Get players by tier."""
    return [p for p in NBA_PLAYERS.values() if p.player_tier == tier]


def get_players_by_tendency(tendency: str) -> List[NBAPlayer]:
    """Get players by public betting tendency."""
    return [p for p in NBA_PLAYERS.values() if p.public_betting_tendency == tendency]


def get_soft_line_players() -> List[NBAPlayer]:
    """Get players with soft betting lines (best value opportunities)."""
    return [p for p in NBA_PLAYERS.values() if p.line_softness == "soft"]


def get_role_players() -> List[NBAPlayer]:
    """Get role players and bench players (undervalued props)."""
    return [p for p in NBA_PLAYERS.values() if p.player_tier in ["role_player", "bench"]]


def get_elite_tier_players() -> List[NBAPlayer]:
    """Get elite tier players (MVPs, maximum public attention)."""
    return [p for p in NBA_PLAYERS.values() if p.player_tier == "elite"]


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BETGENIE — NBA PLAYER DATABASE (Comprehensive)")
    print("  All Tiers: Elite, Star, Starter, Role Player")
    print("=" * 70)
    
    print(f"\nTotal Players: {len(NBA_PLAYERS)}")
    print(f"Elite Tier: {len(get_players_by_tier('elite'))}")
    print(f"Star Tier: {len(get_players_by_tier('star'))}")
    print(f"Starter Tier: {len(get_players_by_tier('starter'))}")
    print(f"Role Player Tier: {len(get_players_by_tier('role_player'))}")
    print(f"Soft Lines (Best Value): {len(get_soft_line_players())}")
    
    print("\n" + "-" * 70)
    print("  ELITE TIER (Sharp lines, fade opportunities)")
    print("-" * 70)
    
    for player in get_elite_tier_players():
        print(f"\n{player.full_name} ({player.team})")
        print(f"  PPG: {player.current_season.points_per_game}")
        print(f"  Line Softness: {player.line_softness}")
        print(f"  Public Tendency: {player.public_betting_tendency}")
    
    print("\n" + "-" * 70)
    print("  ROLE PLAYERS (Soft lines, value opportunities)")
    print("-" * 70)
    
    for player in get_role_players():
        print(f"\n{player.full_name} ({player.team})")
        print(f"  PPG: {player.current_season.points_per_game}")
        print(f"  Line Softness: {player.line_softness}")
        print(f"  Public Tendency: {player.public_betting_tendency}")
        print(f"  Value: HIGH (lines are soft on role players)")
    
    print("\n" + "-" * 70)
    print("  SOFT LINE OPPORTUNITIES (All tiers)")
    print("-" * 70)
    
    for player in get_soft_line_players():
        print(f"\n{player.full_name} ({player.team}) - {player.player_tier}")
        print(f"  PPG: {player.current_season.points_per_game}")
        print(f"  Why Soft: Lines are less sharp on non-elite players")
    
    print("\n" + "=" * 70)
    print("  PLAYER DATABASE — READY")
    print("  Strategy: Find value on role players with soft lines")
    print("=" * 70)
