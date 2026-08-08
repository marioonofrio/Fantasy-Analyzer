import { useEffect, useState } from "react";
import { fetchPlayers } from "./api/players";
import type { Player } from "./types/player";
import LoadingSpinner from "./components/LoadingSpinner";
import Nav from "./components/Nav"

function App() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPlayers("superflex")
      .then(setPlayers)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <div>Error: {error}</div>;



  return (
    <div>
      <Nav />
      <h1>Players</h1>
      <ul>
        {players.map((p) => (
          <li key={p.id}>
            {p.name} — {p.position} — {p.value}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;