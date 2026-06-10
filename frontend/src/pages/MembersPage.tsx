import Card from "../components/ui/Card";

export default function MembersPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>People</span>
        <h2>Members</h2>
        <p>Manage lab members and student, faculty, collaborator subtype fields.</p>
      </div>
      <Card title="Members workspace">
        <p className="placeholder-text">
          UI Phase 3 will add member tables, type filters, detail panels, subtype
          create/edit forms, mentor selectors, and delete confirmations.
        </p>
      </Card>
    </section>
  );
}
