import Card from "../components/ui/Card";

export default function SystemStatusPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Demo readiness</span>
        <h2>System Status / Demo</h2>
        <p>Health checks, docs links, local commands, and demo checklist.</p>
      </div>
      <Card title="System status workspace">
        <p className="placeholder-text">
          Later UI phases will show API health, docs link, CI note, test count,
          and a guided live-demo checklist.
        </p>
      </Card>
    </section>
  );
}
