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
          UI Phase 4 will add device tables, status badges, equipment selectors,
          and protected create/edit/delete actions.
        </p>
      </Card>
    </section>
  );
}
