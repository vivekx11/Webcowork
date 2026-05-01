/**
 * Admin Dashboard - Placeholder with basic structure
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { FiPackage, FiShoppingBag, FiUsers, FiDollarSign } from 'react-icons/fi';

const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Sales</p>
              <p className="text-2xl font-bold">$0.00</p>
            </div>
            <FiDollarSign className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Orders</p>
              <p className="text-2xl font-bold">0</p>
            </div>
            <FiPackage className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Products</p>
              <p className="text-2xl font-bold">0</p>
            </div>
            <FiShoppingBag className="w-12 h-12 text-purple-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Users</p>
              <p className="text-2xl font-bold">0</p>
            </div>
            <FiUsers className="w-12 h-12 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link
          to="/admin/products"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition text-center"
        >
          <FiShoppingBag className="w-12 h-12 mx-auto mb-4 text-primary-600" />
          <h3 className="font-semibold">Manage Products</h3>
        </Link>

        <Link
          to="/admin/orders"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition text-center"
        >
          <FiPackage className="w-12 h-12 mx-auto mb-4 text-primary-600" />
          <h3 className="font-semibold">Manage Orders</h3>
        </Link>

        <Link
          to="/admin/categories"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition text-center"
        >
          <FiShoppingBag className="w-12 h-12 mx-auto mb-4 text-primary-600" />
          <h3 className="font-semibold">Manage Categories</h3>
        </Link>

        <Link
          to="/admin/users"
          className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition text-center"
        >
          <FiUsers className="w-12 h-12 mx-auto mb-4 text-primary-600" />
          <h3 className="font-semibold">Manage Users</h3>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
