from pydantic import BaseModel
from typing import Optional


class PlayerOut(BaseModel):
    id: int
    name: str
    position: str
    team: Optional[str]
    age: Optional[int]
    value: Optional[float] = None

class TradeRequest(BaseModel):
    side_a_ids: list[int]
    side_b_ids: list[int]

class TradeResult(BaseModel):
    side_a_total: float
    side_b_total: float
    verdict: str

class LeagueImportRequest(BaseModel):
    sleeper_league_id: str

class LeagueOut(BaseModel):
    id: int
    name: str
    format: str
    team_count: int
    season: int

class PositionRank(BaseModel):
    value: float
    rank: int

class TeamRanking(BaseModel):
    team_id: int
    display_name: str
    total_value: float
    player_count: int
    avg_age: Optional[float] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    positions: dict[str, PositionRank]

class LeagueRankingsOut(BaseModel):
    league_id: int
    league_name: str
    format: str
    teams: list[TeamRanking]

class GoogleAuthRequest(BaseModel):
    credential: str

class AuthResponse(BaseModel):
    access_token: str
    user_id: int
    email: str
    name: str