from database import get_session
from models import League

with get_session() as session:
    league = League(
        sleeper_league_id="123456789",
        name="Dynasty Warfare",
        format="superflex",
        team_count=12,
        season=2025,
    )
    session.add(league)
    session.commit()
    session.refresh(league)
    print(league)

with get_session() as session:
    from sqlmodel import select
    result = session.exec(select(League).where(League.sleeper_league_id == "123456789")).first()
    print(result)