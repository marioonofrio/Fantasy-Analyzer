from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import date, datetime
from typing import Optional

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sleeper_id: str = Field(unique=True)
    name: str
    position: str
    team: Optional[str] = None
    age: Optional[int] = None
    draft_year: Optional[int] = None
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None

class PlayerSeason(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("player_id", "season"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    season: int
    points: float
    games_played: Optional[int] = None

class League(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sleeper_league_id: str = Field(unique=True)
    name: str
    format: str
    team_count: int
    season: int

class Team(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("league_id", "sleeper_owner_id"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="league.id")
    sleeper_owner_id: str
    display_name: str
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None

class RosterSlot(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("team_id", "player_id"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    player_id: int = Field(foreign_key="player.id")

class DraftPick(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("league_id", "season", "round", "original_team_id"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    league_id: int = Field(foreign_key="league.id")
    season: int
    round: int
    original_team_id: int = Field(foreign_key="team.id")
    current_team_id: int = Field(foreign_key="team.id")

class PlayerValue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    format: str
    value: float
    computed_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    google_id: str = Field(unique=True)
    email: str
    name: str

class UserLeague(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("user_id", "league_id"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    league_id: int = Field(foreign_key="league.id")