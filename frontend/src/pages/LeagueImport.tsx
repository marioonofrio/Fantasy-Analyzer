import { useState } from "react";
import { Link } from "react-router-dom";
import { importLeague, fetchLeagueRankings } from "../api/players";
import type { LeagueRankings } from "../types/player";
import LoadingSpinner from "../components/LoadingSpinner";

function LeagueImport() {
  const [leagueIdInput, setLeagueIdInput] = useState("");
  const [rankings, setRankings] = useState<LeagueRankings | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleImport() {
    setLoading(true);
    setError(null);
    try {
      const league = await importLeague(leagueIdInput.trim());
      const data = await fetchLeagueRankings(league.id);
      setRankings(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <nav>
        <Link to="/">Players</Link> | <Link to="/trade">Trade Calculator</Link> | <Link to="/league">Import League</Link>
      </nav>
      <h1>Import League</h1>

      <div>
        <input
          type="text"
          placeholder="Sleeper league ID"
          value={leagueIdInput}
          onChange={(e) => setLeagueIdInput(e.target.value)}
        />
        <button onClick={handleImport} disabled={loading || !leagueIdInput.trim()}>
          {loading ? "Importing..." : "Import"}
        </button>
      </div>

      {error && <p>{error}</p>}
      {loading && <LoadingSpinner />}

      {rankings && (
        <div>
          <h2>{rankings.league_name} — {rankings.format}</h2>
          <ol>
            {rankings.teams.map((t) => (
              <li key={t.team_id}>
                {t.display_name} — {t.total_value} ({t.player_count} players)
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default LeagueImport;