/**
 * Order Detail Page - Placeholder
 */
import React from 'react';
import { useParams, Link } from 'react-router-dom';

const OrderDetail = () => {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Order #{id}</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-600">Order details will be displayed here.</p>
        <Link to="/orders" className="text-primary-600 hover:text-primary-700 mt-4 inline-block">
          ← Back to Orders
        </Link>
      </div>
    </div>
  );
};

export default OrderDetail;
