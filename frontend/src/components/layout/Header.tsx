import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { API_BASE_URL, apiRequest } from "../../api/client";
import { endpoints } from "../../api/endpoints";
import type { HealthResponse } from "../../api/types";
import { clearToken, isLoggedIn } from "../../auth/auth";
import StatusBadge from "../ui/StatusBadge";

export default function Header(): JSX.Element {
  const navigate = useNavigate();
  const healthQuery = useQuery({
    queryKey: ["health"],
    queryFn: () => apiRequest<HealthResponse>(endpoints.health),
    refetchInterval: 30000,
  });

  function handleLogout(): void {
    clearToken();
    navigate("/login");
  }

  const healthLabel = healthQuery.isLoading
    ? "Checking API"
    : healthQuery.data?.status === "ok"
      ? "API online"
      : "API offline";
  const healthTone =
    healthQuery.data?.status === "ok"
      ? "success"
      : healthQuery.isLoading
        ? "neutral"
        : "danger";

  return (
    <header className="top-header">
      <div>
        <h1>Research Lab Manager</h1>
        <p>Full-stack FastAPI + PostgreSQL admin dashboard</p>
      </div>
      <div className="header-status">
        <StatusBadge label={healthLabel} tone={healthTone} />
        <StatusBadge
          label={isLoggedIn() ? "Admin token saved" : "Read-only"}
          tone={isLoggedIn() ? "success" : "neutral"}
        />
        <span className="api-url">{API_BASE_URL}</span>
        <button className="header-button" onClick={handleLogout} type="button">
          Logout
        </button>
      </div>
    </header>
  );
}
