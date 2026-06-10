import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { isLoggedIn } from "./auth";

type ProtectedRouteProps = {
  children: ReactNode;
};

export default function ProtectedRoute({
  children,
}: ProtectedRouteProps): JSX.Element {
  const location = useLocation();

  if (!isLoggedIn()) {
    return <Navigate replace state={{ from: location }} to="/login" />;
  }

  return <>{children}</>;
}
