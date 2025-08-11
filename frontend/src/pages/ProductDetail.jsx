import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProduct, getOffers, getWarranty } from "../services/product";

export default function ProductDetail() {
  const { id } = useParams();
  const nav = useNavigate();
  const [product, setProduct] = useState(null);
  const [offers, setOffers] = useState([]);
  const [warranty, setWarranty] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const p = await getProduct(id);
        setProduct(p);
        const off = await getOffers();
        setOffers((off || []).filter(o => o.product_id === p.id));
        const w = await getWarranty(p.id);
        setWarranty(w);
      } catch (e) {
        console.error(e);
      }
    })();
  }, [id]);

  if (!product) return <div>Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
      <button onClick={() => nav(-1)} className="mb-3 text-blue-600">← Back</button>
      <h2 className="text-2xl font-semibold">{product.name}</h2>
      <p className="text-gray-600">{product.description}</p>
      <div className="mt-4">
        <div className="text-lg font-bold">₹ {product.price}</div>
        <div className="mt-2">
          <strong>Offers:</strong>
          {offers.length ? offers.map(o => (
            <div key={o.id} className="p-2 border rounded mt-2">
              <div>{o.coupon_code} — {o.discount_percentage}%</div>
              <div className="text-sm text-gray-600">Valid till: {o.valid_till}</div>
            </div>
          )) : <div className="text-sm text-gray-600">No offers</div>}
        </div>

        <div className="mt-4">
          <strong>Warranty:</strong>
          {warranty ? <div className="p-2 border rounded mt-2">{warranty.warranty_period}<div className="text-sm text-gray-600">{warranty.claim_process}</div></div> : <div className="text-sm text-gray-600">No warranty info</div>}
        </div>

        <div className="mt-6">
          <button onClick={() => nav("/chat", { state: { prefill: `Tell me about ${product.name}` } })} className="bg-blue-600 text-white px-4 py-2 rounded">Ask about this product</button>
        </div>
      </div>
    </div>
  );
}
