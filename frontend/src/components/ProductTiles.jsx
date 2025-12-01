import React from "react";

export default function ProductTiles({ products }) {
  if (!products || products.length === 0) return null;

  return (
    <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {products.map((p, i) => (
        <div key={i} className="bg-white shadow-md rounded p-4">
          <h2 className="text-xl font-bold">{p.name}</h2>
          <p className="text-sm text-gray-600">{p.brand}</p>
          <p className="mt-2 font-semibold">₹{p.price}</p>

          <ul className="mt-3 text-sm list-disc pl-5">
            {p.features && typeof p.features === "object" ? (
              Object.entries(p.features).map(([k, v]) => (
                <li key={k}>
                  <strong>{k}:</strong> {v}
                </li>
              ))
            ) : (
              <li>No feature data available</li>
            )}
          </ul>
        </div>
      ))}
    </div>
  );
}
