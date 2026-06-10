import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./auth/ProtectedRoute";
import AppLayout from "./components/layout/AppLayout";
import DashboardPage from "./pages/DashboardPage";
import DevicesPage from "./pages/DevicesPage";
import EquipmentPage from "./pages/EquipmentPage";
import GrantsPage from "./pages/GrantsPage";
import LoginPage from "./pages/LoginPage";
import MembersPage from "./pages/MembersPage";
import ProjectsPage from "./pages/ProjectsPage";
import PublicationsPage from "./pages/PublicationsPage";
import ReportsPage from "./pages/ReportsPage";
import SystemStatusPage from "./pages/SystemStatusPage";
import UsagePage from "./pages/UsagePage";

export default function App(): JSX.Element {
  return (
    <Routes>
      <Route element={<LoginPage />} path="/login" />
      <Route element={<Navigate replace to="/dashboard" />} path="/" />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route element={<DashboardPage />} path="/dashboard" />
        <Route element={<MembersPage />} path="/members" />
        <Route element={<ProjectsPage />} path="/projects" />
        <Route element={<GrantsPage />} path="/grants" />
        <Route element={<EquipmentPage />} path="/equipment" />
        <Route element={<DevicesPage />} path="/devices" />
        <Route element={<UsagePage />} path="/usage" />
        <Route element={<PublicationsPage />} path="/publications" />
        <Route element={<ReportsPage />} path="/reports" />
        <Route element={<SystemStatusPage />} path="/system-status" />
      </Route>
      <Route element={<Navigate replace to="/dashboard" />} path="*" />
    </Routes>
  );
}
