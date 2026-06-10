import { useNavigate } from "react-router-dom";

import { API_BASE_URL } from "../../api/client";
import { clearToken, isLoggedIn } from "../../auth/auth";
import StatusBadge from "../ui/StatusBadge";

export default function Header(): JSX.Element {
  const navigate = useNavigate();

  function handleLogout(): void {
    clearToken();
    navigate("/login");
  }

  return (
    <header className="top-header">
      <div>
        <h1>Research Lab Manager</h1>
        <p>Full-stack FastAPI + PostgreSQL admin dashboard</p>
      </div>
      <div className="header-status">
        <StatusBadge label="API health pending" tone="neutral" />
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
