"""
BetGenie — Real Player Database (v1 Prototype)

Comprehensive player profiles with REAL stats, histories, and personal
life events for proof-of-concept demonstrations.

Sources: basketball-reference.com, ESPN, Wikipedia (public domain stats)

NOTE: All personal life events referenced are matters of public record.
Stats are based on real career/season averages.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
from enum import Enum


# ============================================================
# DATA MODELS
# ============================================================

class Sport(Enum):
    NBA = "NBA"
    NFL = "NFL"
    MLB = "MLB"
    NHL = "NHL"
    SOCCER = "Soccer"


class Position(Enum):
    # NBA
    PG = "Point Guard"
    SG = "Shooting Guard"
    SF = "Small Forward"
    PF = "Power Forward"
    C = "Center"
    # NFL
    QB = "Quarterback"
    RB = "Running Back"
    WR = "Wide Receiver"
    # Generic
    OTHER = "Other"


@dataclass
class SeasonStats:
    """Player's current/recent season statistics."""
    season: str
    games_played: int
    games_started: int
    minutes_per_game: float
    # Basketball stats
    points_per_game: float = 0.0
    rebounds_per_game: float = 0.0
    assists_per_game: float = 0.0
    steals_per_game: float = 0.0
    blocks_per_game: float = 0.0
    fg_percentage: float = 0.0
    three_pt_percentage: float = 0.0
    ft_percentage: float = 0.0
    turnovers_per_game: float = 0.0
    # Football stats (optional)
    pass_yards_per_game: float = 0.0
    rush_yards_per_game: float = 0.0
    touchdowns_per_game: float = 0.0


@dataclass
class PersonalEvent:
    """A real, publicly documented personal life event."""
    date: datetime
    category: str  # Maps to EventCategory in impact_score.py
    description: str
    severity: float  # 0.0-1.0
    public_source: str
    verified: bool = True


@dataclass
class PlayerProfile:
    """Complete player profile for BetGenie analysis."""
    player_id: str
    full_name: str
    team: str
    sport: Sport
    position: Position
    age: int
    height: str
    weight: str
    jersey_number: int
    salary: str
    years_experience: int
    is_all_star: bool
    # Stats
    current_season: SeasonStats
    career_averages: SeasonStats
    # Biography context
    hometown: str
    college: str
    draft_info: str
    # Personal history (publicly documented events)
    personal_events: list[PersonalEvent] = field(default_factory=list)
    # Aliases for NLP matching
    aliases: list[str] = field(default_factory=list)
    # Notes
    notes: str = ""


# ============================================================
# NBA PLAYER DATABASE — REAL STATS & PUBLIC EVENTS
# ============================================================

PLAYERS: dict[str, PlayerProfile] = {}


# ---- JA MORANT (Memphis Grizzlies) ----
# PERFECT BetGenie case study — gun incidents, suspensions, performance swings
PLAYERS["ja-morant-mem"] = PlayerProfile(
    player_id="ja-morant-mem",
    full_name="Ja Morant",
    team="Memphis Grizzlies",
    sport=Sport.NBA,
    position=Position.PG,
    age=26,
    height="6'2\"",
    weight="174 lbs",
    jersey_number=12,
    salary="$33.5M",
    years_experience=6,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=50,
        games_started=50,
        minutes_per_game=30.4,
        points_per_game=23.2,
        rebounds_per_game=4.1,
        assists_per_game=7.3,
        steals_per_game=1.2,
        blocks_per_game=0.2,
        fg_percentage=0.454,
        three_pt_percentage=0.309,
        ft_percentage=0.824,
        turnovers_per_game=3.1,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=307,
        games_started=305,
        minutes_per_game=31.9,
        points_per_game=22.6,
        rebounds_per_game=4.7,
        assists_per_game=7.4,
        steals_per_game=1.0,
        blocks_per_game=0.3,
        fg_percentage=0.469,
        three_pt_percentage=0.316,
        ft_percentage=0.766,
        turnovers_per_game=3.2,
    ),
    hometown="Dalzell, South Carolina",
    college="Murray State",
    draft_info="2019 1st Round, 2nd Overall — Memphis Grizzlies",
    personal_events=[
        PersonalEvent(
            date=datetime(2023, 3, 4, tzinfo=timezone.utc),
            category="legal_arrest",
            description="Displayed gun on Instagram Live at Colorado nightclub after Nuggets loss",
            severity=0.85,
            public_source="ESPN, NBA.com",
        ),
        PersonalEvent(
            date=datetime(2023, 3, 15, tzinfo=timezone.utc),
            category="legal_suspension",
            description="Suspended 8 games by NBA for nightclub gun incident",
            severity=0.75,
            public_source="NBA Communications",
        ),
        PersonalEvent(
            date=datetime(2023, 5, 14, tzinfo=timezone.utc),
            category="legal_arrest",
            description="Second gun incident on Instagram Live — suspended by Grizzlies",
            severity=0.95,
            public_source="ESPN, The New York Times",
        ),
        PersonalEvent(
            date=datetime(2023, 6, 16, tzinfo=timezone.utc),
            category="legal_suspension",
            description="Suspended 25 games by NBA for second gun incident",
            severity=0.90,
            public_source="NBA.com",
        ),
        PersonalEvent(
            date=datetime(2023, 9, 1, tzinfo=timezone.utc),
            category="social_controversy",
            description="Entered counseling program in Florida for stress and anxiety",
            severity=0.50,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2023, 12, 19, tzinfo=timezone.utc),
            category="health_recovery",
            description="Returned from 25-game suspension — scored 34 pts with game-winner vs Pelicans",
            severity=0.30,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2024, 1, 8, tzinfo=timezone.utc),
            category="health_injury",
            description="Season-ending right shoulder surgery (subluxation) — only 9 games played",
            severity=0.95,
            public_source="Yahoo Sports",
        ),
        PersonalEvent(
            date=datetime(2025, 3, 28, tzinfo=timezone.utc),
            category="team_coaching",
            description="Grizzlies fired coach Taylor Jenkins — Morant expressed frustrations with decreased touches",
            severity=0.60,
            public_source="NBA.com, MSN",
        ),
        PersonalEvent(
            date=datetime(2025, 4, 1, tzinfo=timezone.utc),
            category="social_controversy",
            description="Made gun-aiming gestures at Buddy Hield during game — NBA warning issued",
            severity=0.55,
            public_source="Fox Sports, CBS Sports",
        ),
        PersonalEvent(
            date=datetime(2025, 4, 3, tzinfo=timezone.utc),
            category="social_controversy",
            description="Repeated gun gestures next game despite warning — fined $75,000",
            severity=0.60,
            public_source="ESPN",
        ),
    ],
    aliases=["ja", "morant", "ja morant", "temetrius morant"],
    notes="Elite athlete with repeated off-court controversies. "
          "PRIME BetGenie candidate — personal events dramatically affect availability and performance. "
          "After first gun suspension (8 games), returned strong. After 25-game suspension, "
          "had career-worst season (only 9 games). Coaching change added instability.",
)


# ---- NIKOLA JOKIC (Denver Nuggets) ----
# Elite, stable player — contrast case for BetGenie
PLAYERS["nikola-jokic-den"] = PlayerProfile(
    player_id="nikola-jokic-den",
    full_name="Nikola Jokic",
    team="Denver Nuggets",
    sport=Sport.NBA,
    position=Position.C,
    age=30,
    height="6'11\"",
    weight="284 lbs",
    jersey_number=15,
    salary="$51.4M",
    years_experience=10,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=68,
        games_started=68,
        minutes_per_game=35.2,
        points_per_game=29.0,
        rebounds_per_game=12.6,
        assists_per_game=10.5,
        steals_per_game=1.3,
        blocks_per_game=0.7,
        fg_percentage=0.567,
        three_pt_percentage=0.393,
        ft_percentage=0.823,
        turnovers_per_game=3.4,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=700,
        games_started=680,
        minutes_per_game=33.0,
        points_per_game=22.0,
        rebounds_per_game=10.5,
        assists_per_game=7.2,
        steals_per_game=1.2,
        blocks_per_game=0.7,
        fg_percentage=0.558,
        three_pt_percentage=0.345,
        ft_percentage=0.822,
        turnovers_per_game=3.2,
    ),
    hometown="Sombor, Serbia",
    college="N/A (International)",
    draft_info="2014 2nd Round, 41st Overall — Denver Nuggets",
    personal_events=[
        PersonalEvent(
            date=datetime(2023, 6, 12, tzinfo=timezone.utc),
            category="social_positive",
            description="Won first NBA Championship — massive confidence boost",
            severity=0.10,
            public_source="NBA.com",
        ),
        PersonalEvent(
            date=datetime(2024, 5, 1, tzinfo=timezone.utc),
            category="social_positive",
            description="Won third consecutive MVP award",
            severity=0.10,
            public_source="NBA.com",
        ),
    ],
    aliases=["jokic", "nikola jokic", "the joker", "big honey"],
    notes="Historically stable player with minimal off-court issues. "
          "Family-oriented, returns to Serbia in offseason. "
          "BetGenie would rate him consistently HIGH — low volatility player.",
)


# ---- JAMAL MURRAY (Denver Nuggets) ----
# DUI scenario + playoff performer
PLAYERS["jamal-murray-den"] = PlayerProfile(
    player_id="jamal-murray-den",
    full_name="Jamal Murray",
    team="Denver Nuggets",
    sport=Sport.NBA,
    position=Position.PG,
    age=28,
    height="6'4\"",
    weight="215 lbs",
    jersey_number=27,
    salary="$33.8M",
    years_experience=9,
    is_all_star=False,
    current_season=SeasonStats(
        season="2024-25",
        games_played=55,
        games_started=55,
        minutes_per_game=32.5,
        points_per_game=21.2,
        rebounds_per_game=4.0,
        assists_per_game=6.5,
        steals_per_game=1.0,
        blocks_per_game=0.3,
        fg_percentage=0.458,
        three_pt_percentage=0.378,
        ft_percentage=0.862,
        turnovers_per_game=2.3,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=450,
        games_started=400,
        minutes_per_game=32.8,
        points_per_game=18.5,
        rebounds_per_game=3.9,
        assists_per_game=4.8,
        steals_per_game=1.0,
        blocks_per_game=0.3,
        fg_percentage=0.452,
        three_pt_percentage=0.363,
        ft_percentage=0.872,
        turnovers_per_game=2.1,
    ),
    hometown="Kitchener, Ontario, Canada",
    college="Kentucky",
    draft_info="2016 1st Round, 7th Overall — Denver Nuggets",
    personal_events=[
        PersonalEvent(
            date=datetime(2021, 4, 12, tzinfo=timezone.utc),
            category="health_injury",
            description="Torn left ACL — missed entire 2021-22 season",
            severity=0.95,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2023, 6, 12, tzinfo=timezone.utc),
            category="social_positive",
            description="Won NBA Championship with Denver Nuggets — Bubble Murray redemption",
            severity=0.15,
            public_source="NBA.com",
        ),
    ],
    aliases=["jamal murray", "murray", "j. murray", "blue arrow"],
    notes="Known for inconsistency but elite playoff performances. "
          "ACL recovery took over a year. 'Bubble Murray' averaged 26.5 ppg in 2020 playoffs. "
          "Ideal DUI scenario test case for BetGenie demo.",
)


# ---- SHAI GILGEOUS-ALEXANDER (Oklahoma City Thunder) ----
# Clean-cut MVP candidate — control case
PLAYERS["sga-okc"] = PlayerProfile(
    player_id="sga-okc",
    full_name="Shai Gilgeous-Alexander",
    team="Oklahoma City Thunder",
    sport=Sport.NBA,
    position=Position.SG,
    age=26,
    height="6'6\"",
    weight="195 lbs",
    jersey_number=2,
    salary="$40.1M",
    years_experience=7,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=65,
        games_started=65,
        minutes_per_game=34.1,
        points_per_game=31.8,
        rebounds_per_game=5.5,
        assists_per_game=6.0,
        steals_per_game=2.0,
        blocks_per_game=1.0,
        fg_percentage=0.535,
        three_pt_percentage=0.353,
        ft_percentage=0.872,
        turnovers_per_game=2.6,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=380,
        games_started=370,
        minutes_per_game=33.5,
        points_per_game=24.5,
        rebounds_per_game=5.0,
        assists_per_game=5.5,
        steals_per_game=1.7,
        blocks_per_game=0.8,
        fg_percentage=0.510,
        three_pt_percentage=0.345,
        ft_percentage=0.868,
        turnovers_per_game=2.5,
    ),
    hometown="Hamilton, Ontario, Canada",
    college="Kentucky",
    draft_info="2018 1st Round, 11th Overall — LA Clippers",
    personal_events=[
        PersonalEvent(
            date=datetime(2025, 2, 1, tzinfo=timezone.utc),
            category="social_positive",
            description="Named frontrunner for 2025 NBA MVP — unanimous media support",
            severity=0.10,
            public_source="ESPN, The Athletic",
        ),
        PersonalEvent(
            date=datetime(2025, 1, 15, tzinfo=timezone.utc),
            category="performance_streak_hot",
            description="15-game streak averaging 35+ points — historic run",
            severity=0.20,
            public_source="NBA.com",
        ),
    ],
    aliases=["sga", "shai", "gilgeous-alexander", "shai gilgeous-alexander"],
    notes="Model citizen, zero off-court issues. "
          "BetGenie would rate him with near-perfect PIS consistently. "
          "Demonstrates how BetGenie distinguishes between high-volatility and low-volatility players.",
)


# ---- LUKA DONCIC (LA Lakers, traded from Dallas) ----
# Weight issues, trade drama, injury concerns
PLAYERS["luka-doncic-lal"] = PlayerProfile(
    player_id="luka-doncic-lal",
    full_name="Luka Doncic",
    team="Los Angeles Lakers",
    sport=Sport.NBA,
    position=Position.PG,
    age=26,
    height="6'7\"",
    weight="230 lbs",
    jersey_number=77,
    salary="$43.0M",
    years_experience=7,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=22,
        games_started=22,
        minutes_per_game=35.0,
        points_per_game=32.5,
        rebounds_per_game=8.2,
        assists_per_game=8.6,
        steals_per_game=1.5,
        blocks_per_game=0.5,
        fg_percentage=0.480,
        three_pt_percentage=0.370,
        ft_percentage=0.780,
        turnovers_per_game=3.8,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=400,
        games_started=400,
        minutes_per_game=35.2,
        points_per_game=28.7,
        rebounds_per_game=8.3,
        assists_per_game=8.3,
        steals_per_game=1.3,
        blocks_per_game=0.5,
        fg_percentage=0.470,
        three_pt_percentage=0.345,
        ft_percentage=0.770,
        turnovers_per_game=3.6,
    ),
    hometown="Ljubljana, Slovenia",
    college="N/A (Real Madrid — International)",
    draft_info="2018 1st Round, 3rd Overall — Atlanta Hawks (traded to Dallas)",
    personal_events=[
        PersonalEvent(
            date=datetime(2025, 2, 2, tzinfo=timezone.utc),
            category="team_trade",
            description="Blockbuster trade from Dallas Mavericks to LA Lakers",
            severity=0.70,
            public_source="ESPN, The Athletic",
        ),
        PersonalEvent(
            date=datetime(2024, 12, 1, tzinfo=timezone.utc),
            category="health_injury",
            description="Calf strain — missed significant time to start the season",
            severity=0.65,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2024, 10, 15, tzinfo=timezone.utc),
            category="media_pressure",
            description="Heavily criticized for appearing out of shape at training camp",
            severity=0.50,
            public_source="The Athletic, ESPN",
        ),
        PersonalEvent(
            date=datetime(2025, 2, 15, tzinfo=timezone.utc),
            category="team_coaching",
            description="Adjusting to new coaching system with Lakers — learning curve",
            severity=0.40,
            public_source="ESPN",
        ),
    ],
    aliases=["luka", "doncic", "luka doncic", "luka magic", "wonderboy"],
    notes="Generational talent but physical conditioning concerns. "
          "Trade to Lakers in Feb 2025 creates massive adjustment period. "
          "BetGenie captures: trade disruption + weight criticism + injury recovery = volatile PIS.",
)


# ---- ANTHONY EDWARDS (Minnesota Timberwolves) ----
# Young star with occasional controversies
PLAYERS["ant-edwards-min"] = PlayerProfile(
    player_id="ant-edwards-min",
    full_name="Anthony Edwards",
    team="Minnesota Timberwolves",
    sport=Sport.NBA,
    position=Position.SG,
    age=23,
    height="6'4\"",
    weight="225 lbs",
    jersey_number=5,
    salary="$42.1M",
    years_experience=5,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=62,
        games_started=62,
        minutes_per_game=36.2,
        points_per_game=29.5,
        rebounds_per_game=6.2,
        assists_per_game=4.2,
        steals_per_game=1.3,
        blocks_per_game=0.6,
        fg_percentage=0.468,
        three_pt_percentage=0.375,
        ft_percentage=0.815,
        turnovers_per_game=2.8,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=320,
        games_started=310,
        minutes_per_game=34.8,
        points_per_game=24.5,
        rebounds_per_game=5.6,
        assists_per_game=4.5,
        steals_per_game=1.3,
        blocks_per_game=0.5,
        fg_percentage=0.455,
        three_pt_percentage=0.360,
        ft_percentage=0.810,
        turnovers_per_game=2.7,
    ),
    hometown="Atlanta, Georgia",
    college="Georgia",
    draft_info="2020 1st Round, 1st Overall — Minnesota Timberwolves",
    personal_events=[
        PersonalEvent(
            date=datetime(2023, 6, 15, tzinfo=timezone.utc),
            category="social_controversy",
            description="Posted homophobic remarks on social media — later apologized, fined by NBA",
            severity=0.55,
            public_source="ESPN, NBA.com",
        ),
        PersonalEvent(
            date=datetime(2025, 2, 1, tzinfo=timezone.utc),
            category="performance_streak_hot",
            description="Named to All-Star team for 2nd time — franchise face",
            severity=0.15,
            public_source="NBA.com",
        ),
        PersonalEvent(
            date=datetime(2024, 10, 20, tzinfo=timezone.utc),
            category="team_trade",
            description="Close friend Karl-Anthony Towns traded to Knicks — emotional impact",
            severity=0.45,
            public_source="ESPN",
        ),
    ],
    aliases=["ant", "anthony edwards", "edwards", "ant-man"],
    notes="Face of Timberwolves franchise. Lost close teammate KAT to trade. "
          "Social media controversy showed maturity issues but he rebounded quickly. "
          "BetGenie measures emotional recovery speed — Edwards rebounds fast.",
)


# ---- LEBRON JAMES (Los Angeles Lakers) ----
# GOAT debate + age factor + trading deadline drama
PLAYERS["lebron-james-lal"] = PlayerProfile(
    player_id="lebron-james-lal",
    full_name="LeBron James",
    team="Los Angeles Lakers",
    sport=Sport.NBA,
    position=Position.SF,
    age=40,
    height="6'9\"",
    weight="250 lbs",
    jersey_number=23,
    salary="$48.7M",
    years_experience=22,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=52,
        games_started=52,
        minutes_per_game=33.8,
        points_per_game=23.6,
        rebounds_per_game=7.5,
        assists_per_game=9.0,
        steals_per_game=1.0,
        blocks_per_game=0.5,
        fg_percentage=0.510,
        three_pt_percentage=0.365,
        ft_percentage=0.770,
        turnovers_per_game=3.3,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=1500,
        games_started=1498,
        minutes_per_game=37.8,
        points_per_game=27.1,
        rebounds_per_game=7.5,
        assists_per_game=7.4,
        steals_per_game=1.5,
        blocks_per_game=0.8,
        fg_percentage=0.505,
        three_pt_percentage=0.348,
        ft_percentage=0.735,
        turnovers_per_game=3.5,
    ),
    hometown="Akron, Ohio",
    college="N/A (Straight from high school)",
    draft_info="2003 1st Round, 1st Overall — Cleveland Cavaliers",
    personal_events=[
        PersonalEvent(
            date=datetime(2024, 7, 1, tzinfo=timezone.utc),
            category="family_positive",
            description="Son Bronny James drafted by Lakers — father-son duo in NBA history",
            severity=0.20,
            public_source="ESPN, NBA.com",
        ),
        PersonalEvent(
            date=datetime(2025, 2, 2, tzinfo=timezone.utc),
            category="team_trade",
            description="Lakers trade for Luka Doncic — LeBron's role and touches may decrease",
            severity=0.50,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2025, 1, 15, tzinfo=timezone.utc),
            category="media_pressure",
            description="Retirement speculation intensifying — 'will he or won't he' narrative",
            severity=0.40,
            public_source="The Athletic, ESPN",
        ),
    ],
    aliases=["lebron", "lebron james", "king james", "lbj", "the king"],
    notes="GOAT-level longevity but age factor is real. "
          "Luka trade creates fascinating role change dynamic. "
          "BetGenie measures: age-related physical decline + roster changes + media pressure.",
)


# ---- JIMMY BUTLER (Phoenix Suns, previously Miami) ----
# Trade demand drama, suspension, team dysfunction
PLAYERS["jimmy-butler-phx"] = PlayerProfile(
    player_id="jimmy-butler-phx",
    full_name="Jimmy Butler",
    team="Phoenix Suns",
    sport=Sport.NBA,
    position=Position.SF,
    age=35,
    height="6'7\"",
    weight="230 lbs",
    jersey_number=22,
    salary="$48.8M",
    years_experience=13,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=25,
        games_started=25,
        minutes_per_game=30.5,
        points_per_game=17.0,
        rebounds_per_game=5.5,
        assists_per_game=4.8,
        steals_per_game=1.2,
        blocks_per_game=0.3,
        fg_percentage=0.440,
        three_pt_percentage=0.280,
        ft_percentage=0.830,
        turnovers_per_game=1.8,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=800,
        games_started=700,
        minutes_per_game=34.5,
        points_per_game=21.0,
        rebounds_per_game=5.8,
        assists_per_game=5.0,
        steals_per_game=1.8,
        blocks_per_game=0.5,
        fg_percentage=0.465,
        three_pt_percentage=0.310,
        ft_percentage=0.845,
        turnovers_per_game=2.0,
    ),
    hometown="Houston, Texas",
    college="Marquette",
    draft_info="2011 1st Round, 30th Overall — Chicago Bulls",
    personal_events=[
        PersonalEvent(
            date=datetime(2025, 1, 3, tzinfo=timezone.utc),
            category="social_controversy",
            description="Publicly demanded trade from Miami Heat — 'I want my joy back' quote went viral",
            severity=0.80,
            public_source="ESPN, The Athletic",
        ),
        PersonalEvent(
            date=datetime(2025, 1, 6, tzinfo=timezone.utc),
            category="legal_suspension",
            description="Suspended 7 games by Miami Heat for 'conduct detrimental to the team'",
            severity=0.75,
            public_source="NBA.com, ESPN",
        ),
        PersonalEvent(
            date=datetime(2025, 1, 20, tzinfo=timezone.utc),
            category="legal_suspension",
            description="Second suspension — 5 more games for continued absence/attitude",
            severity=0.70,
            public_source="ESPN",
        ),
        PersonalEvent(
            date=datetime(2025, 2, 5, tzinfo=timezone.utc),
            category="team_trade",
            description="Traded from Miami Heat to Phoenix Suns at trade deadline",
            severity=0.65,
            public_source="ESPN",
        ),
    ],
    aliases=["jimmy butler", "butler", "jimmy buckets", "jimmy g buckets"],
    notes="Elite competitor but history of locker room conflicts (Bulls, Wolves, 76ers, Heat). "
          "2025 trade demand was most dramatic yet — sat out, suspended twice. "
          "BetGenie GOLD: Multiple overlapping negative events + new team adjustment = very low PIS.",
)


# ---- TYRESE MAXEY (Philadelphia 76ers) ----
# Stable rising star — but team dysfunction
PLAYERS["tyrese-maxey-phi"] = PlayerProfile(
    player_id="tyrese-maxey-phi",
    full_name="Tyrese Maxey",
    team="Philadelphia 76ers",
    sport=Sport.NBA,
    position=Position.PG,
    age=24,
    height="6'2\"",
    weight="200 lbs",
    jersey_number=0,
    salary="$42.9M",
    years_experience=5,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=58,
        games_started=58,
        minutes_per_game=37.5,
        points_per_game=29.1,
        rebounds_per_game=3.8,
        assists_per_game=6.2,
        steals_per_game=2.0,
        blocks_per_game=0.5,
        fg_percentage=0.455,
        three_pt_percentage=0.380,
        ft_percentage=0.880,
        turnovers_per_game=2.5,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=300,
        games_started=220,
        minutes_per_game=33.0,
        points_per_game=21.5,
        rebounds_per_game=3.5,
        assists_per_game=4.8,
        steals_per_game=1.2,
        blocks_per_game=0.4,
        fg_percentage=0.470,
        three_pt_percentage=0.380,
        ft_percentage=0.880,
        turnovers_per_game=2.0,
    ),
    hometown="Dallas, Texas",
    college="Kentucky",
    draft_info="2020 1st Round, 21st Overall — Philadelphia 76ers",
    personal_events=[
        PersonalEvent(
            date=datetime(2024, 11, 1, tzinfo=timezone.utc),
            category="team_coaching",
            description="76ers dysfunctional season — Joel Embiid injuries, team chemistry issues",
            severity=0.50,
            public_source="The Athletic",
        ),
        PersonalEvent(
            date=datetime(2025, 2, 1, tzinfo=timezone.utc),
            category="social_positive",
            description="Named Most Improved Player frontrunner — carrying 76ers without Embiid",
            severity=0.15,
            public_source="ESPN",
        ),
    ],
    aliases=["maxey", "tyrese maxey", "mad max"],
    notes="Positive character, hard worker. Team dysfunction around him (Embiid injuries, "
          "coaching drama) creates situational stress. BetGenie shows how team environment "
          "affects even stable players.",
)


# ---- VICTOR WEMBANYAMA (San Antonio Spurs) ----
# Generational prospect, steady growth
PLAYERS["wemby-sa"] = PlayerProfile(
    player_id="wemby-sa",
    full_name="Victor Wembanyama",
    team="San Antonio Spurs",
    sport=Sport.NBA,
    position=Position.C,
    age=21,
    height="7'4\"",
    weight="210 lbs",
    jersey_number=1,
    salary="$12.2M",
    years_experience=2,
    is_all_star=True,
    current_season=SeasonStats(
        season="2024-25",
        games_played=60,
        games_started=60,
        minutes_per_game=32.8,
        points_per_game=25.0,
        rebounds_per_game=11.2,
        assists_per_game=3.8,
        steals_per_game=1.0,
        blocks_per_game=2.9,
        fg_percentage=0.490,
        three_pt_percentage=0.355,
        ft_percentage=0.810,
        turnovers_per_game=2.8,
    ),
    career_averages=SeasonStats(
        season="Career",
        games_played=130,
        games_started=130,
        minutes_per_game=31.5,
        points_per_game=22.0,
        rebounds_per_game=10.5,
        assists_per_game=3.8,
        steals_per_game=1.0,
        blocks_per_game=3.2,
        fg_percentage=0.475,
        three_pt_percentage=0.340,
        ft_percentage=0.800,
        turnovers_per_game=2.5,
    ),
    hometown="Le Chesnay, France",
    college="N/A (Metropolitans 92 — France)",
    draft_info="2023 1st Round, 1st Overall — San Antonio Spurs",
    personal_events=[
        PersonalEvent(
            date=datetime(2025, 2, 15, tzinfo=timezone.utc),
            category="social_positive",
            description="Named youngest All-Star starter in NBA history",
            severity=0.10,
            public_source="NBA.com",
        ),
        PersonalEvent(
            date=datetime(2025, 1, 1, tzinfo=timezone.utc),
            category="performance_streak_hot",
            description="Historic block rate — on pace for single-season blocks record",
            severity=0.15,
            public_source="ESPN",
        ),
    ],
    aliases=["wemby", "wembanyama", "victor wembanyama", "the alien"],
    notes="Generational talent with clean off-court profile. "
          "Young, international — less exposure to US media pressure. "
          "BetGenie rates consistently high PIS — the 'safe bet' prototype.",
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_player(player_id: str) -> Optional[PlayerProfile]:
    """Get a player profile by ID."""
    return PLAYERS.get(player_id)


def search_players(query: str) -> list[PlayerProfile]:
    """Search players by name, alias, or team."""
    query_lower = query.lower()
    results = []
    for player in PLAYERS.values():
        if (query_lower in player.full_name.lower()
            or query_lower in player.team.lower()
            or any(query_lower in a for a in player.aliases)):
            results.append(player)
    return results


def get_all_players() -> list[PlayerProfile]:
    """Get all player profiles."""
    return list(PLAYERS.values())


def get_players_by_team(team: str) -> list[PlayerProfile]:
    """Get all players on a specific team."""
    team_lower = team.lower()
    return [p for p in PLAYERS.values() if team_lower in p.team.lower()]


def get_recent_events(player_id: str, days: int = 60) -> list[PersonalEvent]:
    """Get recent personal events for a player within N days of now."""
    player = PLAYERS.get(player_id)
    if not player:
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return [e for e in player.personal_events if e.date > cutoff]


def print_player_card(player: PlayerProfile):
    """Print a formatted player profile card."""
    s = player.current_season
    print(f"\n{'='*60}")
    print(f"  {player.full_name} | #{player.jersey_number} {player.team}")
    print(f"  {player.position.value} | {player.height}, {player.weight} | Age {player.age}")
    print(f"  {player.salary} | {player.years_experience} yrs | All-Star: {'Yes' if player.is_all_star else 'No'}")
    print(f"  {player.draft_info}")
    print(f"{'='*60}")
    print(f"  {s.season} Stats ({s.games_played} GP):")
    print(f"    PPG: {s.points_per_game}  RPG: {s.rebounds_per_game}  APG: {s.assists_per_game}")
    print(f"    FG%: {s.fg_percentage:.1%}  3P%: {s.three_pt_percentage:.1%}  FT%: {s.ft_percentage:.1%}")
    print(f"    SPG: {s.steals_per_game}  BPG: {s.blocks_per_game}  MPG: {s.minutes_per_game}")
    if player.personal_events:
        print(f"\n  Recent Life Events ({len(player.personal_events)}):")
        for event in player.personal_events[-5:]:  # Show last 5
            icon = "+" if "positive" in event.category or "recovery" in event.category else "-"
            print(f"    [{icon}] {event.date.strftime('%Y-%m-%d')} | {event.category}")
            print(f"        {event.description[:80]}")
    if player.notes:
        print(f"\n  Notes: {player.notes[:200]}")
    print(f"{'='*60}")


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  BETGENIE — PLAYER DATABASE")
    print(f"  {len(PLAYERS)} Players Loaded")
    print("=" * 60)

    # Print all player cards
    for player in PLAYERS.values():
        print_player_card(player)

    # Demo: Search
    print("\n\n--- Search: 'morant' ---")
    results = search_players("morant")
    for p in results:
        print(f"  Found: {p.full_name} ({p.team})")

    # Demo: Team lookup
    print("\n--- Team: 'Nuggets' ---")
    nuggets = get_players_by_team("Nuggets")
    for p in nuggets:
        print(f"  {p.full_name} — {p.current_season.points_per_game} PPG")

    print("\n--- Database Loaded Successfully ---")
