import httpx
from sqlmodel import select
from database import get_session
from models import Player

SLEEPER_URL = "https://api.sleeper.app/v1/players/nfl"
VALID_POSITIONS = {"QB", "RB", "WR", "TE"}


def fetch_players():
    response = httpx.get(SLEEPER_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def sync_players():
    data = fetch_players()
    created = 0
    updated = 0

    with get_session() as session:
        for sleeper_id, info in data.items():
            position = info.get("position")
            if position not in VALID_POSITIONS:
                continue

            first_name = info.get("first_name") or ""
            last_name = info.get("last_name") or ""
            name = f"{first_name} {last_name}".strip()
            if not name:
                continue

            existing = session.exec(
                select(Player).where(Player.sleeper_id == sleeper_id)
            ).first()

            if existing:
                existing.name = name
                existing.position = position
                existing.team = info.get("team")
                existing.age = info.get("age")
                session.add(existing)
                updated += 1
            else:
                player = Player(
                    sleeper_id=sleeper_id,
                    name=name,
                    position=position,
                    team=info.get("team"),
                    age=info.get("age"),
                )
                session.add(player)
                created += 1

        session.commit()

    print(f"created={created} updated={updated}")


if __name__ == "__main__":
    sync_players()