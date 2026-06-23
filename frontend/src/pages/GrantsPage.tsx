import Card from "../components/ui/Card";

export default function GrantsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Funding</span>
        <h2>Grants</h2>
        <p>Explore grant-funded project and member relationships.</p>
      </div>
      <Card title="Grants workspace">
        <p className="placeholder-text">
          Grant management is in progress. It will start with grant-funded member
          lookup and funding reports, then add admin create, edit, and delete
          actions.
        </p>
      </Card>
    </section>
  );
}
