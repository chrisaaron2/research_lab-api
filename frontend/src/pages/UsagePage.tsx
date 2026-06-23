import Card from "../components/ui/Card";

export default function UsagePage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Relationships</span>
        <h2>Usage</h2>
        <p>Track member usage of device and equipment pairs.</p>
      </div>
      <Card title="Usage workspace">
        <p className="placeholder-text">
          Usage management is in progress. It will add active-only filters,
          member, device, and equipment selectors, and usage forms.
        </p>
      </Card>
    </section>
  );
}
