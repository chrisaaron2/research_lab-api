import Card from "../components/ui/Card";

export default function GrantsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Funding</span>
        <h2>Grants</h2>
        <p>Explore grant-funded project and member relationships.</p>
      </div>
      <Card title="Grant planning note">
        <p className="placeholder-text">
          Full Grant CRUD is a planned backend extension. Current UI will start
          with grant-funded member lookup and funding reports.
        </p>
      </Card>
    </section>
  );
}
