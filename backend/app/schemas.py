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