import Card from "../components/ui/Card";

const summaryCards = [
  ["Members", "GET /members"],
  ["Projects", "GET /projects"],
  ["Equipment", "GET /equipment"],
  ["Devices", "GET /devices"],
  ["Active Uses", "GET /uses?active_only=true"],
];

export default function DashboardPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Overview</span>
        <h2>Dashboard</h2>
        <p>Portfolio admin dashboard for the Research Lab Manager API.</p>
      </div>
      <div className="card-grid">
        {summaryCards.map(([title, endpoint]) => (
          <Card description={endpoint} key={title} title={title}>
            <p className="placeholder-text">Live counts arrive in UI Phase 2.</p>
          </Card>
        ))}
      </div>
    </section>
  );
}
