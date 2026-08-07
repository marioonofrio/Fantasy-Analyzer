import { useState } from "react";
import type { Player } from "../types/player";

interface PlayerSearchProps {
  label: string;
  allPlayers: Player[];
  selectedPlayers: Player[];
  onAdd: (player: Player) => void;
  onRemove: (playerId: number) => void;
}

function PlayerSearch({ label, allPlayers, selectedPlayers, onAdd, onRemove }: PlayerSearchProps) {
  const [query, setQuery] = useState("");

  const selectedIds = new Set(selectedPlayers.map((p) => p.id));

  const matches =
    query.trim() === ""
      ? []
      : allPlayers
          .filter((p) => !selectedIds.has(p.id))
          .filter((p) => p.name.toLowerCase().includes(query.toLowerCase()))
          .slice(0, 8);

  const totalValue = selectedPlayers.reduce((sum, p) => sum + (p.value || 0), 0);

  function handleAdd(player: Player) {
    onAdd(player);
    setQuery("");
  }

  return (
    <div style={{ border: "1px solid #444", borderRadius: 8, padding: 16, width: 320 }}>
      <h3>{label}</h3>

      <input
        type="text"
        placeholder="Search for player"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "85%", padding: 8 }}
      />

      {matches.length > 0 && (
        <ul style={{ border: "1px solid #333", marginTop: 4, padding: 0, listStyle: "none" }}>
          {matches.map((p) => (
            <li key={p.id} onClick={() => handleAdd(p)} style={{ padding: 8, cursor: "pointer" }}>
              {p.name} — {p.position}
            </li>
          ))}
        </ul>
      )}

      <ul style={{ marginTop: 12, padding: 0, listStyle: "none" }}>
        {selectedPlayers.map((p) => (
          <li key={p.id} style={{ display: "flex", justifyContent: "space-between", padding: "4px 0" }}>
            <span>{p.name} — {p.position}</span>
            <button onClick={() => onRemove(p.id)}>Remove</button>
          </li>
        ))}
      </ul>

      <div style={{ borderTop: "1px solid #444", marginTop: 8, paddingTop: 8, display: "flex", justifyContent: "space-between" }}>
        <span>Total Value</span>
        <span>{totalValue}</span>
      </div>
    </div>
  );
}

export default PlayerSearch;