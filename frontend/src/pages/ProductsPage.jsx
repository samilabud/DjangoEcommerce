// src/pages/ProductsPage.jsx
import React, { useEffect, useState } from "react";
import { useApi } from "../api/useApi";

export default function ProductsPage() {
  const api = useApi();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/products/");
        setProducts(data);
      } catch (err) {
        console.error(err);
      }
    })();
  }, [api]);

  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((p) => (
        <div key={p.id}>{p.name}</div>
      ))}
    </div>
  );
}
