import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPlayers } from "../api/players";
import type { Player, TradeResult } from "../types/player";
import { evaluateTrade } from "../api/players";
import PlayerSearch from "../components/PlayerSearch";

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

  function removeFromSideA(playerId: number) {
    setSideAPlayers(sideAPlayers.filter((p) => p.id !== playerId));
  }

  function removeFromSideB(playerId: number) {
    setSideBPlayers(sideBPlayers.filter((p) => p.id !== playerId));
  }

  async function handleEvaluate() {
    setLoading(true);
    try {
      const data = await evaluateTrade(
        sideAPlayers.map((p) => p.id),
        sideBPlayers.map((p) => p.id)
      );
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <nav>
        <Link to="/">Players</Link> | <Link to="/trade">Trade Calculator</Link>
      </nav>
      <h1>Trade Calculator</h1>

      <div style={{ display: "flex", gap: 24, justifyContent: "center" }}>
        <PlayerSearch
          label="Side A"
          allPlayers={allPlayers}
          selectedPlayers={sideAPlayers}
          onAdd={addToSideA}
          onRemove={removeFromSideA}
        />
        <PlayerSearch
          label="Side B"
          allPlayers={allPlayers}
          selectedPlayers={sideBPlayers}
          onAdd={addToSideB}
          onRemove={removeFromSideB}
        />
      </div>

      <button onClick={handleEvaluate} disabled={loading}>
        {loading ? "Evaluating..." : "Evaluate Trade"}
      </button>

      {result && (
        <div>
          <p>Side A total: {result.side_a_total}</p>
          <p>Side B total: {result.side_b_total}</p>
          <p>Verdict: {result.verdict}</p>
        </div>
      )}
    </div>
  );
}

export default TradeCalculator;