import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPlayers } from "../api/players";
import type { Player, TradeResult } from "../types/player";

function TradeCalculator() {
  const [sideAPlayers, setSideAPlayers] = useState<Player[]>([]);
  const [sideBPlayers, setSideBPlayers] = useState<Player[]>([]);

  const [result, setResult] = useState<TradeResult | null>(null);
  const [loading, setLoading] = useState(false);

  const [allPlayers, setAllPlayers] = useState<Player[]>([]);
  useEffect(() => {
    fetchPlayers("superflex")
      .then(setAllPlayers)
      .catch((err) => console.error(err));
  }, []);

  function addToSideA(player: Player) {
    setSideAPlayers([...sideAPlayers, player]);
  }

  function addToSideB(player: Player) {
    setSideBPlayers([...sideBPlayers, player]);
  }

  return (
    <div>
      <nav>
        <Link to="/">Players</Link> | <Link to="/trade">Trade Calculator</Link>
      </nav>
      <h1>Trade Calculator</h1>

      <h2>All Players</h2>
      <ul>
        {allPlayers.map((p) => (
          <li key={p.id}>
            {p.name} — {p.position}
            <button onClick={() => addToSideA(p)}>Add to A</button>
            <button onClick={() => addToSideB(p)}>Add to B</button>
          </li>
        ))}
      </ul>

      <h2>Side A</h2>
      <ul>
        {sideAPlayers.map((p) => (
          <li key={p.id}>{p.name} — {p.position}</li>
        ))}
      </ul>

      <h2>Side B</h2>
      <ul>
        {sideBPlayers.map((p) => (
          <li key={p.id}>{p.name} — {p.position}</li>
        ))}
      </ul>
    </div>
  );
}

export default TradeCalculator;