import React from "react";
import { Link } from "react-router-dom";

export default function ProductCard({ p }) {
  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded p-4 bg-white dark:bg-gray-800">
      <h3 className="font-semibold text-gray-900 dark:text-white">{p.name}</h3>
      <p className="text-sm text-gray-600 dark:text-gray-400">{p.category}</p>
      <div className="mt-2 flex items-center justify-between">
        <div className="text-lg font-bold text-gray-900 dark:text-white">₹ {p.price}</div>
        <Link to={`/products/${p.id}`} className="text-blue-600 dark:text-blue-400">View</Link>
      </div>
    </div>
  );
}
