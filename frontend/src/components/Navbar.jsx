import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import { useTheme } from "../contexts/ThemeContext";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();
  const { isDark, toggleTheme } = useTheme();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-lg border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/products" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">I</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-700 bg-clip-text text-transparent">
              Inquiro
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            <Link 
              to="/products" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/products') 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 shadow-sm' 
                  : 'text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              Products
            </Link>
            <Link 
              to="/chat" 
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                isActive('/chat') 
                  ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 shadow-sm' 
                  : 'text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              Chat
            </Link>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-3">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-200 hover:scale-105"
              aria-label="Toggle theme"
            >
              {isDark ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              )}
            </button>

            {/* User Menu */}
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="hidden sm:flex items-center space-x-2">
                  <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                    <span className="text-primary-600 dark:text-primary-400 font-medium text-sm">
                      {user.name?.charAt(0)?.toUpperCase()}
                    </span>
                  </div>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">{user.name}</span>
                </div>
                <button 
                  onClick={logout} 
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium hover:shadow-md"
                >
                  Logout
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link 
                  to="/login" 
                  className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-lg transition-colors font-medium"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium hover:shadow-md"
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
