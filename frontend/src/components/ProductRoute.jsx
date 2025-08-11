import React, { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

export default function ProtectedRoute() {
  const { token } = useContext(AuthContext);
  if (!token) return <Navigate to="/login" replace />;
  return <Outlet />;
}
