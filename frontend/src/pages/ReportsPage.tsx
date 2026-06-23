import Card from "../components/ui/Card";

export default function ReportsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Analytics</span>
        <h2>Reports</h2>
        <p>Funding, mentorship, project, and publication report views.</p>
      </div>
      <Card title="Reports workspace">
        <p className="placeholder-text">
          Reporting views are in progress. This page will add report tables,
          simple charts, and date filters over the backend reporting endpoints.
        </p>
      </Card>
    </section>
  );
}
