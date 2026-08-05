import type { Player, TradeResult } from "../types/player";

const API_BASE = "http://127.0.0.1:8000";

export async function fetchPlayers(format: string = "superflex", position?: string, valuedOnly: boolean = true): Promise<Player[]> {
  const params = new URLSearchParams({ format, valued_only: String(valuedOnly) });
  if (position) params.append("position", position);

  const res = await fetch(`${API_BASE}/players?${params}`);
  if (!res.ok) throw new Error("Failed to fetch players");
  return res.json();
}

export async function evaluateTrade(sideAIds: number[], sideBIds: number[], format: string = "superflex"): Promise<TradeResult> {
  const res = await fetch(`${API_BASE}/trade/evaluate?format=${format}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ side_a_ids: sideAIds, side_b_ids: sideBIds }),
  });
  if (!res.ok) throw new Error("Failed to evaluate trade");
  return res.json();
}