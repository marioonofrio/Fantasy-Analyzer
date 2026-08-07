export interface Player {
  id: number;
  name: string;
  position: string;
  team: string | null;
  age: number | null;
  value: number | null;
}

export interface TradeResult {
  side_a_total: number;
  side_b_total: number;
  verdict: string;
}

export interface TeamRanking {
  team_id: number;
  display_name: string;
  total_value: number;
  player_count: number;
}

export interface LeagueRankings {
  league_id: number;
  league_name: string;
  format: string;
  teams: TeamRanking[];
}