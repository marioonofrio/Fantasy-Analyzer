import nflreadpy as nfl

ids = nfl.load_ff_playerids()
print(ids.columns)
print(ids.head(3))

stats = nfl.load_player_stats([2025])
print(stats.columns)
print(stats.head(3))