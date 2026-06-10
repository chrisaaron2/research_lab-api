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
          UI Phase 4 will add equipment tables, detail panels, active users,
          and create/edit/delete flows.
        </p>
      </Card>
    </section>
  );
}
