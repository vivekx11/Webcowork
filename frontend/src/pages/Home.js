/**
 * Home Page
 * Landing page with featured products and categories
 */
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../services/api';
import { FiShoppingBag, FiTruck, FiShield, FiHeadphones } from 'react-icons/fi';

const Home = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        productsAPI.getAll({ per_page: 8 }),
        categoriesAPI.getAll(),
      ]);
      setFeaturedProducts(productsRes.data.products);
      setCategories(categoriesRes.data.categories);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Welcome to E-Shop
            </h1>
            <p className="text-xl md:text-2xl mb-8">
              Discover amazing products at unbeatable prices
            </p>
            <Link
              to="/products"
              className="inline-block px-8 py-3 bg-white text-primary-600 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Shop Now
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <FiTruck className="w-12 h-12 mx-auto text-primary-600 mb-4" />
              <h3 className="font-semibold mb-2">Free Shipping</h3>
              <p className="text-gray-600 text-sm">On orders over $50</p>
            </div>
            <div className="text-center">
              <FiShield className="w-12 h-12 mx-auto text-primary-600 mb-4" />
              <h3 className="font-semibold mb-2">Secure Payment</h3>
              <p className="text-gray-600 text-sm">100% secure transactions</p>
            </div>
            <div className="text-center">
              <FiHeadphones className="w-12 h-12 mx-auto text-primary-600 mb-4" />
              <h3 className="font-semibold mb-2">24/7 Support</h3>
              <p className="text-gray-600 text-sm">Dedicated support team</p>
            </div>
            <div className="text-center">
              <FiShoppingBag className="w-12 h-12 mx-auto text-primary-600 mb-4" />
              <h3 className="font-semibold mb-2">Easy Returns</h3>
              <p className="text-gray-600 text-sm">30-day return policy</p>
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-8">Shop by Category</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {categories.map((category) => (
              <Link
                key={category.id}
                to={`/products?category=${category.id}`}
                className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition text-center"
              >
                <h3 className="font-semibold">{category.name}</h3>
                <p className="text-sm text-gray-600 mt-1">
                  {category.product_count} items
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold">Featured Products</h2>
            <Link to="/products" className="text-primary-600 hover:text-primary-700">
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <Link
                key={product.id}
                to={`/products/${product.id}`}
                className="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
              >
                <div className="aspect-square bg-gray-200">
                  {product.image_url ? (
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                      No Image
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-semibold mb-2 truncate">{product.name}</h3>
                  <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                    {product.description}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-primary-600">
                      ${product.price.toFixed(2)}
                    </span>
                    {product.stock > 0 ? (
                      <span className="text-sm text-green-600">In Stock</span>
                    ) : (
                      <span className="text-sm text-red-600">Out of Stock</span>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
