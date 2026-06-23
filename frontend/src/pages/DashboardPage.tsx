import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { apiRequest } from "../api/client";
import { endpoints } from "../api/endpoints";
import type { CountableRecord, HealthResponse } from "../api/types";
import { isLoggedIn } from "../auth/auth";
import Card from "../components/ui/Card";
import ErrorState from "../components/ui/ErrorState";
import LoadingState from "../components/ui/LoadingState";
import StatusBadge from "../components/ui/StatusBadge";

type CountCardProps = {
  label: string;
  value: number | string;
  note: string;
};

const quickLinks = [
  ["/members", "Members"],
  ["/projects", "Projects"],
  ["/equipment", "Equipment"],
  ["/usage", "Usage"],
  ["/reports", "Reports"],
  ["/system-status", "System Status"],
];

function CountCard({ label, note, value }: CountCardProps): JSX.Element {
  return (
    <Card description={note} title={label}>
      <strong className="metric-value">{value}</strong>
    </Card>
  );
}

export default function DashboardPage(): JSX.Element {
  const navigate = useNavigate();

  const healthQuery = useQuery({
    queryKey: ["dashboard", "health"],
    queryFn: () => apiRequest<HealthResponse>(endpoints.health),
  });
  const membersQuery = useQuery({
    queryKey: ["dashboard", "members"],
    queryFn: () => apiRequest<CountableRecord[]>(endpoints.members.list()),
  });
  const projectsQuery = useQuery({
    queryKey: ["dashboard", "projects"],
    queryFn: () => apiRequest<CountableRecord[]>(endpoints.projects.list),
  });
  const equipmentQuery = useQuery({
    queryKey: ["dashboard", "equipment"],
    queryFn: () => apiRequest<CountableRecord[]>(endpoints.equipment.list),
  });
  const devicesQuery = useQuery({
    queryKey: ["dashboard", "devices"],
    queryFn: () => apiRequest<CountableRecord[]>(endpoints.devices.list),
  });
  const activeUsesQuery = useQuery({
    queryKey: ["dashboard", "active-uses"],
    queryFn: () => apiRequest<CountableRecord[]>(endpoints.uses.active),
  });

  const queries = [
    healthQuery,
    membersQuery,
    projectsQuery,
    equipmentQuery,
    devicesQuery,
    activeUsesQuery,
  ];
  const isLoading = queries.some((query) => query.isLoading);
  const hasError = queries.some((query) => query.isError);

  useEffect(() => {
    if (hasError && !isLoggedIn()) {
      navigate("/login");
    }
  }, [hasError, navigate]);

  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Overview</span>
        <h2>Dashboard</h2>
        <p>Admin dashboard for the Research Lab Manager API.</p>
      </div>

      {isLoading ? <LoadingState message="Loading dashboard data..." /> : null}
      {hasError ? (
        <ErrorState message="Some dashboard data could not load. Check the API and refresh the page." />
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
        </Card>
        <CountCard
          label="Members"
          note="GET /members"
          value={membersQuery.data?.length ?? "-"}
        />
        <CountCard
          label="Projects"
          note="GET /projects"
          value={projectsQuery.data?.length ?? "-"}
        />
        <CountCard
          label="Equipment"
          note="GET /equipment"
          value={equipmentQuery.data?.length ?? "-"}
        />
        <CountCard
          label="Devices"
          note="GET /devices"
          value={devicesQuery.data?.length ?? "-"}
        />
        <CountCard
          label="Active Uses"
          note="GET /uses?active_only=true"
          value={activeUsesQuery.data?.length ?? "-"}
        />
      </div>

      <Card
        description="Jump to the main sections."
        title="Quick Navigation"
      >
        <div className="quick-link-grid">
          {quickLinks.map(([to, label]) => (
            <Link className="quick-link-card" key={to} to={to}>
              {label}
            </Link>
          ))}
        </div>
      </Card>
    </section>
  );
}
