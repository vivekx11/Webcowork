/**
 * Wishlist Page - Placeholder
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { FiHeart } from 'react-icons/fi';

const Wishlist = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">My Wishlist</h1>
      <div className="text-center py-12">
        <FiHeart className="mx-auto h-24 w-24 text-gray-400" />
        <h2 className="mt-4 text-2xl font-bold text-gray-900">Your wishlist is empty</h2>
        <p className="mt-2 text-gray-600">Save your favorite products here</p>
        <Link
          to="/products"
          className="mt-6 inline-block px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Browse Products
        </Link>
      </div>
    </div>
  );
};

export default Wishlist;
