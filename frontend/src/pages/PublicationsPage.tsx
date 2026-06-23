import Card from "../components/ui/Card";

export default function PublicationsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Publications</span>
        <h2>Publications</h2>
        <p>Review publication reporting and student publication trends.</p>
      </div>
      <Card title="Publications workspace">
        <p className="placeholder-text">
          Publication management is in progress. It will start with publication
          reporting views, then add admin create, edit, and authorship actions.
        </p>
      </Card>
    </section>
  );
}
