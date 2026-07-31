from database import get_session
from models import PlayerSeason


"""with get_session() as session:
    playerSeason = PlayerSeason(
        player_id = 1,
        season = 2024,
        points = 357.62,
        games_played = 17,
    )
    session.add(playerSeason)
    session.commit()
    session.refresh(playerSeason)
    print(playerSeason)
"""

with get_session() as session:
    try:
        badSeason = PlayerSeason(
            player_id = 999,
            season = 2025,
            points = 100.0,
            games_played = 10,
        )
        session.add(badSeason)
        session.commit()
        print("this should not print")
    except Exception as e:
        print("insert correctly rejected:", e)