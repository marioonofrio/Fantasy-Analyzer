from fastapi import APIRouter, Query
from sqlmodel import select
from typing import Optional
from database import get_session
from models import Player, PlayerValue
from schemas import PlayerOut

router = APIRouter()


def latest_value(session, player_id, fmt):
    row = session.exec(
        select(PlayerValue)
        .where(PlayerValue.player_id == player_id, PlayerValue.format == fmt)
        .order_by(PlayerValue.computed_at.desc())
    ).first()
    return row.value if row else None


@router.get("/players", response_model=list[PlayerOut])
def list_players(
    format: str = Query("superflex"),
    position: Optional[str] = None,
):
    with get_session() as session:
        query = select(Player)
        if position:
            query = query.where(Player.position == position)
        players = session.exec(query).all()

        results = []
        for p in players:
            results.append(PlayerOut(
                id=p.id, name=p.name, position=p.position,
                team=p.team, age=p.age,
                value=latest_value(session, p.id, format),
            ))
        return results


@router.get("/players/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, format: str = Query("superflex")):
    with get_session() as session:
        p = session.get(Player, player_id)
        if not p:
            return {"error": "not found"}
        return PlayerOut(
            id=p.id, name=p.name, position=p.position,
            team=p.team, age=p.age,
            value=latest_value(session, p.id, format),
        )