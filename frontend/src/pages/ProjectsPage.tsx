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
          Project management is in progress. It will show project tables with
          status filters, detail panels, and status cards, plus admin create,
          edit, and delete actions.
        </p>
      </Card>
    </section>
  );
}
