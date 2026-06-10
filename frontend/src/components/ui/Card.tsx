import type { ReactNode } from "react";

type CardProps = {
  children: ReactNode;
  title?: string;
  description?: string;
};

export default function Card({
  children,
  description,
  title,
}: CardProps): JSX.Element {
  return (
    <section className="card">
      {title ? (
        <div className="card-heading">
          <h3>{title}</h3>
          {description ? <p>{description}</p> : null}
        </div>
      ) : null}
      {children}
    </section>
  );
}
