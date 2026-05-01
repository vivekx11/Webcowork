/**
 * Products Page
 * Browse all products with filters and pagination
 */
import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { productsAPI, categoriesAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import { FiShoppingCart, FiHeart } from 'react-icons/fi';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({});
  const [searchParams, setSearchParams] = useSearchParams();
  const { addToCart } = useCart();

  const page = parseInt(searchParams.get('page')) || 1;
  const category = searchParams.get('category') || '';
  const search = searchParams.get('search') || '';

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [page, category, search]);

  const fetchCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = { page, per_page: 12 };
      if (category) params.category_id = category;
      if (search) params.search = search;

      const response = await productsAPI.getAll(params);
      setProducts(response.data.products);
      setPagination({
        total: response.data.total,
        pages: response.data.pages,
        current: response.data.current_page,
      });
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryFilter = (categoryId) => {
    const params = new URLSearchParams(searchParams);
    if (categoryId) {
      params.set('category', categoryId);
    } else {
      params.delete('category');
    }
    params.set('page', '1');
    setSearchParams(params);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const searchValue = formData.get('search');
    const params = new URLSearchParams(searchParams);
    if (searchValue) {
      params.set('search', searchValue);
    } else {
      params.delete('search');
    }
    params.set('page', '1');
    setSearchParams(params);
  };

  const handlePageChange = (newPage) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    setSearchParams(params);
    window.scrollTo(0, 0);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Products</h1>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Sidebar Filters */}
        <div className="lg:col-span-1">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Filters</h2>

            {/* Search */}
            <form onSubmit={handleSearch} className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search
              </label>
              <div className="flex">
                <input
                  type="text"
                  name="search"
                  defaultValue={search}
                  placeholder="Search products..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded-r-md hover:bg-primary-700"
                >
                  Go
                </button>
              </div>
            </form>

            {/* Categories */}
            <div>
              <h3 className="text-lg font-medium mb-3">Categories</h3>
              <div className="space-y-2">
                <button
                  onClick={() => handleCategoryFilter('')}
                  className={`block w-full text-left px-3 py-2 rounded ${
                    !category ? 'bg-primary-100 text-primary-700' : 'hover:bg-gray-100'
                  }`}
                >
                  All Products
                </button>
                {categories.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => handleCategoryFilter(cat.id)}
                    className={`block w-full text-left px-3 py-2 rounded ${
                      category === cat.id.toString()
                        ? 'bg-primary-100 text-primary-700'
                        : 'hover:bg-gray-100'
                    }`}
                  >
                    {cat.name} ({cat.product_count})
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Products Grid */}
        <div className="lg:col-span-3">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="spinner"></div>
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No products found</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                  <div
                    key={product.id}
                    className="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
                  >
                    <Link to={`/products/${product.id}`}>
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
                    </Link>
                    <div className="p-4">
                      <Link to={`/products/${product.id}`}>
                        <h3 className="font-semibold mb-2 hover:text-primary-600 truncate">
                          {product.name}
                        </h3>
                      </Link>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                        {product.description}
                      </p>
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-xl font-bold text-primary-600">
                          ${product.price.toFixed(2)}
                        </span>
                        {product.stock > 0 ? (
                          <span className="text-sm text-green-600">In Stock</span>
                        ) : (
                          <span className="text-sm text-red-600">Out of Stock</span>
                        )}
                      </div>
                      <button
                        onClick={() => addToCart(product.id)}
                        disabled={product.stock === 0}
                        className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                      >
                        <FiShoppingCart className="mr-2" />
                        Add to Cart
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {pagination.pages > 1 && (
                <div className="mt-8 flex justify-center">
                  <nav className="flex space-x-2">
                    <button
                      onClick={() => handlePageChange(pagination.current - 1)}
                      disabled={pagination.current === 1}
                      className="px-4 py-2 border rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Previous
                    </button>
                    {[...Array(pagination.pages)].map((_, i) => (
                      <button
                        key={i + 1}
                        onClick={() => handlePageChange(i + 1)}
                        className={`px-4 py-2 border rounded-md ${
                          pagination.current === i + 1
                            ? 'bg-primary-600 text-white'
                            : 'hover:bg-gray-50'
                        }`}
                      >
                        {i + 1}
                      </button>
                    ))}
                    <button
                      onClick={() => handlePageChange(pagination.current + 1)}
                      disabled={pagination.current === pagination.pages}
                      className="px-4 py-2 border rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                    >
                      Next
                    </button>
                  </nav>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Products;
