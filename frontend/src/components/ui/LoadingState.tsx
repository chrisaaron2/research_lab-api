type LoadingStateProps = {
  message?: string;
};

export default function LoadingState({
  message = "Loading...",
}: LoadingStateProps): JSX.Element {
  return <div className="state-box">{message}</div>;
}
