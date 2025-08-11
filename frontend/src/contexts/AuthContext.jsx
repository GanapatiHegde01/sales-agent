import React, { createContext, useState, useEffect } from "react";
import * as authService from "../services/auth";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const nav = useNavigate();
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("user")); } catch { return null; }
  });
  const [token, setToken] = useState(() => localStorage.getItem("token") || null);

  useEffect(() => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  useEffect(() => {
    if (user) localStorage.setItem("user", JSON.stringify(user));
    else localStorage.removeItem("user");
  }, [user]);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    setToken(data.token);
    setUser(data.user || null);
    return data;
  };

  const register = async (name, email, password) => {
    const data = await authService.register(name, email, password);
    return data;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    // clear axios auth header
    delete api.defaults.headers.common.Authorization;
    nav("/login");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
