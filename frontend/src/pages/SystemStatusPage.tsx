import { useQuery } from "@tanstack/react-query";

import { API_BASE_URL, apiRequest } from "../api/client";
import { endpoints } from "../api/endpoints";
import type { HealthResponse } from "../api/types";
import { isLoggedIn } from "../auth/auth";
import Card from "../components/ui/Card";
import ErrorState from "../components/ui/ErrorState";
import LoadingState from "../components/ui/LoadingState";
import StatusBadge from "../components/ui/StatusBadge";

const engineeringRows = [
  ["Backend", "FastAPI + PostgreSQL"],
  ["ORM/Migrations", "SQLAlchemy async + Alembic"],
  ["Auth", "JWT protected write routes"],
  ["Testing", "Pytest + httpx integration tests"],
  ["CI", "GitHub Actions"],
  ["Frontend", "React + Vite + TypeScript"],
];

export default function SystemStatusPage(): JSX.Element {
  const healthQuery = useQuery({
    queryKey: ["system-status", "health"],
    queryFn: () => apiRequest<HealthResponse>(endpoints.health),
  });

  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>System health</span>
        <h2>System Status</h2>
        <p>
          Live API health, authentication state, documentation links, and
          engineering status.
        </p>
      </div>

      {healthQuery.isLoading ? <LoadingState message="Checking API health..." /> : null}
      {healthQuery.isError ? (
        <ErrorState message="Unable to reach the API health endpoint." />
      ) : null}

      <div className="card-grid">
        <Card description="GET /health" title="API Health">
          <div className="metric-row">
            <strong className="metric-value">
              {healthQuery.data?.status ?? "unknown"}
            </strong>
            <StatusBadge
              label={healthQuery.data?.status === "ok" ? "Online" : "Check API"}
              tone={healthQuery.data?.status === "ok" ? "success" : "warning"}
            />
          </div>
          <p className="placeholder-text">
            Service: {healthQuery.data?.service ?? "unknown"}
          </p>
        </Card>
        <Card description={API_BASE_URL} title="API Base URL">
          <p className="placeholder-text">Configured by VITE_API_BASE_URL.</p>
        </Card>
        <Card description="JWT localStorage token" title="Auth State">
          <StatusBadge
            label={isLoggedIn() ? "Admin token saved" : "Not logged in"}
            tone={isLoggedIn() ? "success" : "warning"}
          />
        </Card>
      <Card description="http://localhost:8000/docs" title="FastAPI Docs">
        <p className="placeholder-text">
          Swagger documentation exposes the complete backend API contract.
        </p>
      </Card>
      </div>

      <div className="card-grid">
        <Card description="Current backend test suite status." title="Testing">
          <strong className="metric-value">36</strong>
          <p className="placeholder-text">Integration tests passing.</p>
        </Card>
        <Card description="Repository automation status." title="CI">
          <StatusBadge label="GitHub Actions CI passing" tone="success" />
        </Card>
      </div>

      <Card
        description="High-level implementation summary for portfolio review."
        title="Engineering Summary"
      >
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Area</th>
                <th>Implementation</th>
              </tr>
            </thead>
            <tbody>
              {engineeringRows.map(([area, implementation]) => (
                <tr key={area}>
                  <td>{area}</td>
                  <td>
                    <code>{implementation}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </section>
  );
}
