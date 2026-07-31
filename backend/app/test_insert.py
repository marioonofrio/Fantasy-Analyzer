from database import get_session
from models import Player

"""with get_session() as session:
    player = Player(
        sleeper_id="6904",
        name="Josh Allen",
        position="QB",
        team="BUF",
        draft_year=2018,
        draft_round=1,
        draft_pick=7,
    )
    session.add(player)
    session.commit()
    session.refresh(player)
    print(player)
"""

with get_session() as session:
    from sqlmodel import select
    result = session.exec(select(Player).where(Player.sleeper_id == "6904")).first()
    print(result)