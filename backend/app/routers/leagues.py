import httpx
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import get_session
from models import League, Team, RosterSlot, Player
from schemas import LeagueImportRequest, LeagueOut, TeamRanking, LeagueRankingsOut
from routers.players import latest_value

router = APIRouter()

SLEEPER_BASE = "https://api.sleeper.app/v1"


def fetch_league(league_id: str):
    r = httpx.get(f"{SLEEPER_BASE}/league/{league_id}", timeout=15)
    r.raise_for_status()
    return r.json()


def fetch_rosters(league_id: str):
    r = httpx.get(f"{SLEEPER_BASE}/league/{league_id}/rosters", timeout=15)
    r.raise_for_status()
    return r.json()


def fetch_users(league_id: str):
    r = httpx.get(f"{SLEEPER_BASE}/league/{league_id}/users", timeout=15)
    r.raise_for_status()
    return r.json()


def detect_format(roster_positions: list) -> str:
    return "superflex" if "SUPER_FLEX" in roster_positions else "1qb"


@router.post("/leagues/import", response_model=LeagueOut)
def import_league(payload: LeagueImportRequest):
    try:
        league_data = fetch_league(payload.sleeper_league_id)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Sleeper league not found")

    if not league_data:
        raise HTTPException(status_code=404, detail="Sleeper league not found")

    rosters_data = fetch_rosters(payload.sleeper_league_id)
    users_data = fetch_users(payload.sleeper_league_id)
    user_names = {u["user_id"]: u.get("display_name", "Unknown") for u in users_data}

    fmt = detect_format(league_data.get("roster_positions", []))

    with get_session() as session:
        league = session.exec(
            select(League).where(League.sleeper_league_id == payload.sleeper_league_id)
        ).first()

        if not league:
            league = League(sleeper_league_id=payload.sleeper_league_id)

        league.name = league_data.get("name", "Unnamed League")
        league.format = fmt
        league.team_count = league_data.get("total_rosters", 0)
        league.season = int(league_data.get("season", 0))

        session.add(league)
        session.flush()

        for roster in rosters_data:
            owner_id = roster.get("owner_id") or f"unclaimed_{roster['roster_id']}"
            display_name = user_names.get(owner_id, "Unclaimed Team")

            team = session.exec(
                select(Team).where(
                    Team.league_id == league.id,
                    Team.sleeper_owner_id == owner_id,
                )
            ).first()

            if not team:
                team = Team(league_id=league.id, sleeper_owner_id=owner_id, display_name=display_name)
            else:
                team.display_name = display_name

            session.add(team)
            session.flush()

            old_slots = session.exec(
                select(RosterSlot).where(RosterSlot.team_id == team.id)
            ).all()
            for slot in old_slots:
                session.delete(slot)

            for sleeper_id in (roster.get("players") or []):
                player = session.exec(
                    select(Player).where(Player.sleeper_id == sleeper_id)
                ).first()
                if player:
                    session.add(RosterSlot(team_id=team.id, player_id=player.id))

        session.commit()
        session.refresh(league)
        return league


@router.get("/leagues/{league_id}/rankings", response_model=LeagueRankingsOut)
def get_league_rankings(league_id: int):
    with get_session() as session:
        league = session.get(League, league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")

        teams = session.exec(select(Team).where(Team.league_id == league_id)).all()

        rankings = []
        for team in teams:
            slots = session.exec(select(RosterSlot).where(RosterSlot.team_id == team.id)).all()
            total = sum(latest_value(session, s.player_id, league.format) or 0.0 for s in slots)
            rankings.append(TeamRanking(
                team_id=team.id,
                display_name=team.display_name,
                total_value=round(total),
                player_count=len(slots),
            ))

        rankings.sort(key=lambda t: -t.total_value)

        return LeagueRankingsOut(
            league_id=league.id,
            league_name=league.name,
            format=league.format,
            teams=rankings,
        )