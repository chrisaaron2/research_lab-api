import Card from "../components/ui/Card";

export default function PublicationsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Publications</span>
        <h2>Publications</h2>
        <p>Review publication reporting and student publication trends.</p>
      </div>
      <Card title="Publication planning note">
        <p className="placeholder-text">
          Full Publication CRUD is a planned backend extension. Current UI will
          start with publication reporting views.
        </p>
      </Card>
    </section>
  );
}
