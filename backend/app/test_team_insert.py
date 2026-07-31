from database import get_session
from models import Team

with get_session() as session:
    try:
        bad_team = Team(
            league_id=999,
            sleeper_owner_id="abc123",
            display_name="Fake Team",
        )
        session.add(bad_team)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)