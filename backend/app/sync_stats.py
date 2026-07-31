import polars as pl
import nflreadpy as nfl
from sqlmodel import select
from database import get_session
from models import Player, PlayerSeason

SEASON = 2025
VALID_POSITIONS = {"QB", "RB", "WR", "TE"}


def build_crosswalk():
    ids = nfl.load_ff_playerids()
    crosswalk = {}
    for row in ids.to_dicts():
        gsis_id = row.get("gsis_id")
        sleeper_id = row.get("sleeper_id")
        if gsis_id and sleeper_id is not None:
            row["sleeper_id"] = str(sleeper_id)
            crosswalk[gsis_id] = row
    return crosswalk


def aggregate_season_stats(season):
    stats = nfl.load_player_stats([season])
    stats = stats.filter(
        pl.col("position").is_in(list(VALID_POSITIONS)),
        pl.col("season_type") == "REG",
    )

    totals = {}
    for row in stats.to_dicts():
        pid = row["player_id"]
        pts = row.get("fantasy_points_ppr") or 0.0
        if pid not in totals:
            totals[pid] = {"points": 0.0, "games": 0}
        totals[pid]["points"] += pts
        totals[pid]["games"] += 1
    return totals


def sync_stats():
    crosswalk = build_crosswalk()
    season_totals = aggregate_season_stats(SEASON)

    created = updated = draft_backfilled = 0
    skipped_no_crosswalk = skipped_no_player = 0

    with get_session() as session:
        for gsis_id, totals in season_totals.items():
            row = crosswalk.get(gsis_id)
            if not row:
                skipped_no_crosswalk += 1
                continue

            player = session.exec(
                select(Player).where(Player.sleeper_id == row["sleeper_id"])
            ).first()
            if not player:
                skipped_no_player += 1
                continue

            if player.draft_year is None and row.get("draft_year"):
                player.draft_year = row.get("draft_year")
                player.draft_round = row.get("draft_round")
                player.draft_pick = row.get("draft_pick")
                session.add(player)
                draft_backfilled += 1

            existing = session.exec(
                select(PlayerSeason).where(
                    PlayerSeason.player_id == player.id,
                    PlayerSeason.season == SEASON,
                )
            ).first()

            if existing:
                existing.points = round(totals["points"], 2)
                existing.games_played = totals["games"]
                session.add(existing)
                updated += 1
            else:
                session.add(PlayerSeason(
                    player_id=player.id,
                    season=SEASON,
                    points=round(totals["points"], 2),
                    games_played=totals["games"],
                ))
                created += 1

        session.commit()

    print(f"created={created} updated={updated} draft_backfilled={draft_backfilled}")
    print(f"skipped_no_crosswalk={skipped_no_crosswalk} skipped_no_player={skipped_no_player}")


if __name__ == "__main__":
    sync_stats()