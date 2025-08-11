import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Products from './pages/Products'
import ProductDetail from './pages/ProductDetail'
import Chat from './pages/Chat'
import ProtectedRoute from './components/ProductRoute'

const App = () => {
  return (
    <div className="min-h-screen transition-colors duration-200">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Navigate to="/products" replace />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/products" element={<Products />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            <Route path="/chat" element={<Chat />} />
          </Route>
        </Routes>
      </main>
    </div>
  )
}

export default App