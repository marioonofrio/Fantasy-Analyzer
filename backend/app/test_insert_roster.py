from database import get_session
from models import RosterSlot

with get_session() as session:
    slot = RosterSlot(team_id=3, player_id=1)
    session.add(slot)
    session.commit()
    session.refresh(slot)
    print(slot)

with get_session() as session:
    try:
        bad_slot = RosterSlot(team_id=3, player_id=999)
        session.add(bad_slot)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)

with get_session() as session:
    try:
        dup_slot = RosterSlot(team_id=3, player_id=1)
        session.add(dup_slot)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)