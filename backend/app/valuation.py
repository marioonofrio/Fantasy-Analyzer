POSITION_CONFIG = {
    "QB": {"max_points": 357.62, "peak_start": 26, "peak_end": 33, "decay": 0.035},
    "RB": {"max_points": 363.60, "peak_start": 23, "peak_end": 27, "decay": 0.13},
    "WR": {"max_points": 309.50, "peak_start": 24, "peak_end": 28, "decay": 0.07},
    "TE": {"max_points": 260.00, "peak_start": 25, "peak_end": 30, "decay": 0.05},
}

FORMAT_CONFIG = {
    "1qb": {
        "QB": {"scarcity": 0.60, "baseline": 250},
        "RB": {"scarcity": 1.10, "baseline": 180},
        "WR": {"scarcity": 1.10, "baseline": 170},
        "TE": {"scarcity": 0.85, "baseline": 120},
    },
    "superflex": {
        "QB": {"scarcity": 1.50, "baseline": 200},
        "RB": {"scarcity": 1.00, "baseline": 190},
        "WR": {"scarcity": 1.00, "baseline": 180},
        "TE": {"scarcity": 0.80, "baseline": 120},
    },
}

PICK_VALUE = {
    1: {"early": 0.72, "mid": 0.55, "late": 0.42},
    2: {"early": 0.32, "mid": 0.25, "late": 0.19},
    3: {"early": 0.14, "mid": 0.11, "late": 0.08},
}
LATE_ROUND_VALUE = 0.05
PROD_FLOOR = 0.05



fmt = "superflex"

def production(players, fmt):
    for item in players:
        cfg = POSITION_CONFIG[item["position"]]
        baseline = FORMAT_CONFIG[fmt][item["position"]]["baseline"]
        if item["points"] > 0:
            score = (item["points"] - baseline) / (cfg["max_points"] - baseline)
            item["prod"] = max(score, PROD_FLOOR)
        else:
            item["prod"] = pick_score(item["rookiePick"])   

def ageMult(players):
    for item in players:
        cfg = POSITION_CONFIG[item["position"]]
        if item["age"] < cfg["peak_start"]:
            mult = min(1.0 + (cfg["peak_start"] - item["age"]) * 0.04, 1.30)
        elif item["age"] <= cfg["peak_end"]:
            mult = 1.0
        else:
            mult = max(1.0 -(item["age"] - cfg["peak_end"]) * cfg["decay"], 0.15)
        item["ageMult"] = mult

def scarcityCalc(players, fmt):
    for item in players:
        item["scarcity"] = FORMAT_CONFIG[fmt][item["position"]]["scarcity"]

def totalValue(players):
    for item in players:
        item["value"] = item["prod"] * item["ageMult"] * item["scarcity"] * 10000
    
def normalize(players):
    max_value = max(item["value"] for item in players)
    if max_value == 0:
        return
    for item in players:
        item["value"] = round(item["value"] / max_value * 10000)

def pick_score(pick):
    rnd = int(pick)
    slot = round((pick - rnd) * 100)
    if rnd not in PICK_VALUE:
        return LATE_ROUND_VALUE
    if slot <= 4:
        tier = "early"
    elif slot <= 8:
        tier = "mid"
    else:
        tier = "late"
    return PICK_VALUE[rnd][tier]

if __name__ == "__main__":
    players = [
        {"name": "Puka Nacua", "position": "WR", "age": 25, "points": 309.5, "rookiePick": 2.01},
        {"name": "Jaxon Smith-Njigba", "position": "WR", "age": 24, "points": 297.4, "rookiePick": 3.07},
        {"name": "Caleb Williams", "position": "QB", "age": 24, "points": 309.18, "rookiePick": 7.02},
        {"name": "Christian McCaffrey", "position": "RB", "age": 30, "points": 363.6, "rookiePick": 4.08},
        {"name": "Josh Allen", "position": "QB", "age": 30, "points": 357.62, "rookiePick": 1.01},
        {"name": "Jeremiyah Love", "position": "RB", "age": 21, "points": 0, "rookiePick": 1.01},
        {"name": "DJ Moore", "position": "WR", "age": 29, "points": 144.18, "rookiePick": 8.01},
        {"name": "Devon Achane", "position": "RB", "age": 24.8, "points": 288.3, "rookiePick": 2.05},
    ]

    fmt = "superflex"

    production(players, fmt)
    ageMult(players)
    scarcityCalc(players, fmt)
    totalValue(players)
    normalize(players)

    for item in players:
        print(f"{item['name']:<20} prod={item['prod']:.3f}  age={item['ageMult']:.2f}  scar={item['scarcity']:.2f}  value={item['value']}")