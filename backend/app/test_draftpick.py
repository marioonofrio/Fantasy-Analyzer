from database import get_session
from models import DraftPick

# valid insert
with get_session() as session:
    pick = DraftPick(
        league_id=1,
        season=2026,
        round=1,
        original_team_id=3,
        current_team_id=3,
    )
    session.add(pick)
    session.commit()
    session.refresh(pick)
    print(pick)

# invalid: current_team_id doesn't exist
with get_session() as session:
    try:
        bad_pick = DraftPick(
            league_id=1,
            season=2026,
            round=2,
            original_team_id=3,
            current_team_id=999,
        )
        session.add(bad_pick)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)

# invalid: duplicate of the valid insert above
with get_session() as session:
    try:
        dup_pick = DraftPick(
            league_id=1,
            season=2026,
            round=1,
            original_team_id=3,
            current_team_id=3,
        )
        session.add(dup_pick)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)