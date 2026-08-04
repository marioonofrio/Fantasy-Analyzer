import type { Player } from "../types/player";

const API_BASE = "http://127.0.0.1:8000";

export async function fetchPlayers(format: string = "superflex", position?: string, valuedOnly: boolean = true): Promise<Player[]> {
  const params = new URLSearchParams({ format, valued_only: String(valuedOnly) });
  if (position) params.append("position", position);

  const res = await fetch(`${API_BASE}/players?${params}`);
  if (!res.ok) throw new Error("Failed to fetch players");
  return res.json();
}