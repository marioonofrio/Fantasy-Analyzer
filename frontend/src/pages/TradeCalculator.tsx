import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPlayers } from "../api/players";
import type { Player, TradeResult } from "../types/player";
import { evaluateTrade } from "../api/players";
import PlayerSearch from "../components/PlayerSearch";
import LoadingSpinner from "../components/LoadingSpinner";

function TradeCalculator() {
  const [sideAPlayers, setSideAPlayers] = useState<Player[]>([]);
  const [sideBPlayers, setSideBPlayers] = useState<Player[]>([]);

  const [result, setResult] = useState<TradeResult | null>(null);
  const [loading, setLoading] = useState(false);

  const [format, setFormat] = useState("superflex");

  const [playersLoading, setPlayersLoading] = useState(true);

  const [allPlayers, setAllPlayers] = useState<Player[]>([]);
  useEffect(() => {
    setPlayersLoading(true);
    fetchPlayers(format)
      .then((data) => {
        setAllPlayers(data);
        setSideAPlayers((prev) => syncValues(prev, data));
        setSideBPlayers((prev) => syncValues(prev, data));
      })
      .catch((err) => console.error(err))
      .finally(() => setPlayersLoading(false));
  }, [format]);

  function syncValues(selected: Player[], fresh: Player[]) {
    return selected.map((p) => fresh.find((f) => f.id === p.id) ?? p);
  }

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
        sideBPlayers.map((p) => p.id),
        format
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
        <Link to="/">Players</Link> | <Link to="/trade">Trade Calculator</Link> | <Link to="/league">Import League</Link>
      </nav>
      <h1>Trade Calculator</h1>
      <div>
        <button onClick={() => setFormat("1qb")} disabled={format === "1qb"}>1QB</button>
        <button onClick={() => setFormat("superflex")} disabled={format === "superflex"}>Superflex</button>
      </div>

       {playersLoading ? (
        <LoadingSpinner />
      ) : (
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
      )}

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