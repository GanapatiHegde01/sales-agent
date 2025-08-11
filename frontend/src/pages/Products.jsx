import React, { useEffect, useState } from "react";
import { getProducts } from "../services/product";
import ProductCard from "../components/ProductCard";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [meta, setMeta] = useState({ page:1, total_pages:1 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  const fetchProducts = async (page) => {
    try {
      setLoading(true);
      setError(null);
      const data = await getProducts(page, 20);
      const { products: list, page: currentPage, total_pages } = data;
      setProducts(list || []);
      setMeta({ page: currentPage, total_pages });
    } catch (e) {
      console.error('Error fetching products:', e);
      setError(e.message || 'Failed to fetch products');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(currentPage);
  }, [currentPage]);

  if (loading) return <div>Loading products...</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-2xl mb-4">Products</h1>
      {products.length === 0 ? (
        <div>No products found.</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {products.map((p) => <ProductCard p={p} key={p.id} />)}
          </div>
          
          {meta.total_pages > 1 && (
            <div className="flex justify-center gap-2 mt-6">
              <button 
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-3 py-1 bg-blue-600 text-white rounded disabled:bg-gray-300"
              >
                Previous
              </button>
              <span className="px-3 py-1">
                Page {currentPage} of {meta.total_pages}
              </span>
              <button 
                onClick={() => setCurrentPage(p => Math.min(meta.total_pages, p + 1))}
                disabled={currentPage === meta.total_pages}
                className="px-3 py-1 bg-blue-600 text-white rounded disabled:bg-gray-300"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
