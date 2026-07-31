from pydantic import BaseModel
from typing import Optional


class PlayerOut(BaseModel):
    id: int
    name: str
    position: str
    team: Optional[str]
    age: Optional[int]
    value: Optional[float] = None