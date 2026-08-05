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