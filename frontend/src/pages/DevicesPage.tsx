import Card from "../components/ui/Card";

export default function DevicesPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Hardware</span>
        <h2>Devices</h2>
        <p>Manage device instances attached to equipment records.</p>
      </div>
      <Card title="Devices workspace">
        <p className="placeholder-text">
          Device management is in progress. It will list devices with status and
          equipment filters, plus admin create, edit, and delete actions.
        </p>
      </Card>
    </section>
  );
}
