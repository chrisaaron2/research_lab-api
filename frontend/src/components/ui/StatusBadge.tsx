type StatusBadgeProps = {
  label: string;
  tone?: "neutral" | "success" | "warning" | "danger";
};

export default function StatusBadge({
  label,
  tone = "neutral",
}: StatusBadgeProps): JSX.Element {
  return <span className={`status-badge ${tone}`}>{label}</span>;
}
