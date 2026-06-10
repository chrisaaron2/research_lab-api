import Card from "../components/ui/Card";

export default function ProjectsPage(): JSX.Element {
  return (
    <section className="page-stack">
      <div className="page-heading">
        <span>Work</span>
        <h2>Projects</h2>
        <p>Manage research projects, leaders, status, members, and funding context.</p>
      </div>
      <Card title="Projects workspace">
        <p className="placeholder-text">
          UI Phase 3 will add project tables, status filters, detail panels,
          leader selectors, full create/edit/delete, and status cards.
        </p>
      </Card>
    </section>
  );
}
