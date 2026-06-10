type ErrorStateProps = {
  message: string;
};

export default function ErrorState({ message }: ErrorStateProps): JSX.Element {
  return <div className="state-box error">{message}</div>;
}
