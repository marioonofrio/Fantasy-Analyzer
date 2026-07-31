from database import get_session
from models import PlayerValue

with get_session() as session:
    pv = PlayerValue(
        player_id=1,
        format="superflex",
        value=8500.0,
    )
    session.add(pv)
    session.commit()
    session.refresh(pv)
    print(pv)

with get_session() as session:
    try:
        bad_pv = PlayerValue(
            player_id=999,
            format="superflex",
            value=1000.0,
        )
        session.add(bad_pv)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)