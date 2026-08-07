import { useState } from "react";
import { Link } from "react-router-dom";
import { importLeague, fetchLeagueRankings } from "../api/players";
import type { LeagueRankings } from "../types/player";
import LoadingSpinner from "../components/LoadingSpinner";

const POSITIONS = ["QB", "RB", "WR", "TE"];

function rankColor(rank: number, totalTeams: number): string {
  if (rank <= totalTeams / 3) return "#2f9e44";
  if (rank <= (totalTeams * 2) / 3) return "#f08c00";
  return "#e03131";
}

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
          <table style={{ borderCollapse: "collapse", width: "100%", marginTop: 16 }}>
            <thead>
              <tr>
                <th>Team</th>
                <th>Total Value</th>
                <th>Record</th>
                <th>Avg Age</th>
                {POSITIONS.map((pos) => (
                  <th key={pos}>{pos}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rankings.teams.map((t, i) => (
                <tr key={t.team_id}>
                  <td>{i + 1}. {t.display_name}</td>
                  <td>{t.total_value}</td>
                  <td>
                    {t.wins ?? "-"}-{t.losses ?? "-"}{t.ties ? `-${t.ties}` : ""}
                  </td>
                  <td>{t.avg_age ?? "-"}</td>
                  {POSITIONS.map((pos) => (
                    <td key={pos}>
                      <span
                        style={{
                          background: rankColor(t.positions[pos].rank, rankings.teams.length),
                          borderRadius: 12,
                          padding: "2px 10px",
                          color: "#fff",
                        }}
                      >
                        {t.positions[pos].rank}
                      </span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default LeagueImport;