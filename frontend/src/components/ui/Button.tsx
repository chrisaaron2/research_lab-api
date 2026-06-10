import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger";
};

export default function Button({
  children,
  className = "",
  variant = "secondary",
  ...props
}: ButtonProps): JSX.Element {
  return (
    <button className={`button ${variant} ${className}`.trim()} type="button" {...props}>
      {children}
    </button>
  );
}
