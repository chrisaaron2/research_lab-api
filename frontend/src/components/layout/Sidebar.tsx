import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/members", label: "Members" },
  { to: "/projects", label: "Projects" },
  { to: "/grants", label: "Grants" },
  { to: "/equipment", label: "Equipment" },
  { to: "/devices", label: "Devices" },
  { to: "/usage", label: "Usage" },
  { to: "/publications", label: "Publications" },
  { to: "/reports", label: "Reports" },
  { to: "/system-status", label: "System Status" },
];

export default function Sidebar(): JSX.Element {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-mark">RL</span>
        <div>
          <strong>Research Lab</strong>
          <span>Manager</span>
        </div>
      </div>
      <nav className="sidebar-nav" aria-label="Main navigation">
        {navItems.map((item) => (
          <NavLink
            className={({ isActive }) => (isActive ? "nav-item active" : "nav-item")}
            key={item.to}
            to={item.to}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
