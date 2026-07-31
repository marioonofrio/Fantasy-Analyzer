from sqlmodel import select
from database import get_session
from models import Player, PlayerSeason, PlayerValue
from valuation import production, ageMult, scarcityCalc, totalValue, normalize

SEASON = 2025
FORMATS = ["1qb", "superflex"]


def build_player_dicts(session):
    season_rows = session.exec(
        select(PlayerSeason).where(PlayerSeason.season == SEASON)
    ).all()
    points_by_player = {row.player_id: row.points for row in season_rows}

    all_players = session.exec(select(Player)).all()

    dicts = []
    for p in all_players:
        if p.age is None:
            continue

        points = points_by_player.get(p.id, 0.0)

        if points > 0:
            rookiePick = None
        else:
            if p.draft_round is None or p.draft_pick is None:
                continue
            rookiePick = p.draft_round + round(p.draft_pick / 100, 2)

        dicts.append({
            "db_id": p.id,
            "name": p.name,
            "position": p.position,
            "age": p.age,
            "points": points,
            "rookiePick": rookiePick,
        })
    return dicts


def run_format(session, fmt):
    players = build_player_dicts(session)

    production(players, fmt)
    ageMult(players)
    scarcityCalc(players, fmt)
    totalValue(players)
    normalize(players)

    for item in players:
        session.add(PlayerValue(
            player_id=item["db_id"],
            format=fmt,
            value=item["value"],
        ))

    print(f"{fmt}: wrote {len(players)} PlayerValue rows")


def run_valuation():
    with get_session() as session:
        for fmt in FORMATS:
            run_format(session, fmt)
        session.commit()


if __name__ == "__main__":
    run_valuation()