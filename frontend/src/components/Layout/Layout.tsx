import { Outlet } from "react-router-dom";
import Navbar from "../Navbar/Navbar";
import RouteLoadingIndicator from "../RouteLoadingIndicator/RouteLoadingIndicator";
import "./Layout.css";

export default function Layout() {
  return (
    <div className="app-shell">
      <RouteLoadingIndicator />
      <Navbar />
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  );
}
