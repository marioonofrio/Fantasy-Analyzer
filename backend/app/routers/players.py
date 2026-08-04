from fastapi import APIRouter, Query
from sqlmodel import select
from typing import Optional
from database import get_session
from models import Player, PlayerValue
from schemas import PlayerOut, TradeRequest, TradeResult

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
    valued_only: bool = False,
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

        if valued_only:
            results = [p for p in results if p.value is not None]  
            
        results.sort(key=lambda p: (p.value is None, -(p.value or 0)))
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

FAIRNESS_THRESHOLD = 0.85


def sum_side(session, player_ids, fmt):
    total = 0.0
    for pid in player_ids:
        value = latest_value(session, pid, fmt)
        # TODO: decide — treat missing value as 0, or track/report it separately?
        total += value or 0.0
    return total


@router.post("/trade/evaluate", response_model=TradeResult)
def evaluate_trade(trade: TradeRequest, format: str = Query("superflex")):
    with get_session() as session:
        side_a_total = sum_side(session, trade.side_a_ids, format)
        side_b_total = sum_side(session, trade.side_b_ids, format)

        larger = max(side_a_total, side_b_total)
        smaller = min(side_a_total, side_b_total)
        ratio = smaller / larger if larger > 0 else 1.0

        if ratio >= FAIRNESS_THRESHOLD:
            verdict = "fair"
        elif side_a_total > side_b_total:
            verdict = "side_a_favored"
        else:
            verdict = "side_b_favored"

        return TradeResult(
            side_a_total=side_a_total,
            side_b_total=side_b_total,
            verdict=verdict,
        )