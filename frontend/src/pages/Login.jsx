import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

export default function Login() {
  const { login } = useContext(AuthContext);
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      await login(email, password);
      nav("/products");
    } catch (error) {
      setErr(error?.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex">
      {/* Left Side - Different Design */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-tr from-emerald-500 via-teal-600 to-cyan-700 dark:from-emerald-400 dark:via-teal-500 dark:to-cyan-600 animate-gradient-x items-center justify-center p-12 rounded-r-3xl relative overflow-hidden" style={{backgroundSize: '400% 400%'}}>
        {/* Geometric Shapes */}
        <div className="absolute top-10 left-10 w-20 h-20 border-2 border-white/30 rotate-45"></div>
        <div className="absolute bottom-20 right-16 w-16 h-16 bg-white/10 rounded-full"></div>
        <div className="absolute top-1/3 right-8 w-12 h-12 border-2 border-white/20 rounded-full"></div>
        
        <div className="text-center text-white relative z-10">
          <div className="text-6xl font-bold mb-4">Welcome Back</div>
          <p className="text-xl opacity-90 mb-8">Continue your Inquiro experience</p>
          <div className="grid grid-cols-2 gap-4 max-w-sm">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">🚀</div>
              <span className="text-sm">Fast Access</span>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">💬</div>
              <span className="text-sm">Chat History</span>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">📎</div>
              <span className="text-sm">Products</span>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center">
              <div className="text-2xl mb-2">🔍</div>
              <span className="text-sm">Search</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="max-w-md w-full">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Sign In
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Welcome back to Inquiro
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-8 border border-gray-200 dark:border-gray-700">
            {err && (
              <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-red-600 dark:text-red-400 text-sm">{err}</p>
              </div>
            )}

            <form onSubmit={onSubmit} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  required
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading || !email || !password}
                className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 hover:shadow-lg disabled:cursor-not-allowed flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing in...
                  </>
                ) : (
                  'Sign In'
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                Don't have an account?{' '}
                <Link to="/register" className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors">
                  Sign up
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}