import Card from "../components/ui/Card";

export default function EquipmentPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Inventory</span>
        <h2>Equipment</h2>
        <p>Manage equipment inventory and active user context.</p>
      </div>
      <Card title="Equipment workspace">
        <p className="placeholder-text">
          Equipment management is in progress. It will show equipment tables,
          detail panels, and active users, plus admin create, edit, and delete
          actions.
        </p>
      </Card>
    </section>
  );
}
