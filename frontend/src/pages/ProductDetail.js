/**
 * Product Detail Page
 */
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { productsAPI, reviewsAPI, wishlistAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { FiShoppingCart, FiHeart, FiStar } from 'react-icons/fi';
import toast from 'react-hot-toast';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useCart();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      setLoading(true);
      const response = await productsAPI.getById(id);
      setProduct(response.data.product);
    } catch (error) {
      console.error('Failed to fetch product:', error);
      toast.error('Product not found');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    addToCart(product.id, quantity);
  };

  const handleAddToWishlist = async () => {
    if (!isAuthenticated()) {
      toast.error('Please login to add to wishlist');
      return;
    }
    try {
      await wishlistAPI.add({ product_id: product.id });
      toast.success('Added to wishlist!');
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to add to wishlist');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h2 className="text-2xl font-bold">Product not found</h2>
        <Link to="/products" className="text-primary-600 hover:text-primary-700 mt-4 inline-block">
          Back to Products
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="mb-8 text-sm">
        <Link to="/" className="text-gray-600 hover:text-primary-600">Home</Link>
        <span className="mx-2">/</span>
        <Link to="/products" className="text-gray-600 hover:text-primary-600">Products</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{product.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Product Image */}
        <div>
          <div className="aspect-square bg-gray-200 rounded-lg overflow-hidden">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No Image Available
              </div>
            )}
          </div>
        </div>

        {/* Product Info */}
        <div>
          <h1 className="text-3xl font-bold mb-4">{product.name}</h1>

          {/* Rating */}
          <div className="flex items-center mb-4">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <FiStar
                  key={i}
                  className={`w-5 h-5 ${
                    i < Math.floor(product.average_rating)
                      ? 'text-yellow-400 fill-current'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
            <span className="ml-2 text-gray-600">
              {product.average_rating.toFixed(1)} ({product.review_count} reviews)
            </span>
          </div>

          {/* Price */}
          <div className="mb-6">
            <span className="text-4xl font-bold text-primary-600">
              ${product.price.toFixed(2)}
            </span>
          </div>

          {/* Stock Status */}
          <div className="mb-6">
            {product.stock > 0 ? (
              <span className="text-green-600 font-semibold">
                In Stock ({product.stock} available)
              </span>
            ) : (
              <span className="text-red-600 font-semibold">Out of Stock</span>
            )}
          </div>

          {/* Description */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Description</h2>
            <p className="text-gray-700 leading-relaxed">{product.description}</p>
          </div>

          {/* Category */}
          <div className="mb-6">
            <span className="text-gray-600">Category: </span>
            <Link
              to={`/products?category=${product.category_id}`}
              className="text-primary-600 hover:text-primary-700"
            >
              {product.category_name}
            </Link>
          </div>

          {/* Quantity Selector */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity
            </label>
            <div className="flex items-center border rounded-md w-32">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="px-4 py-2 hover:bg-gray-100"
              >
                -
              </button>
              <span className="px-4 py-2 border-x flex-1 text-center">{quantity}</span>
              <button
                onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                className="px-4 py-2 hover:bg-gray-100"
              >
                +
              </button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <button
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              className="flex-1 flex items-center justify-center px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            >
              <FiShoppingCart className="mr-2" />
              Add to Cart
            </button>
            <button
              onClick={handleAddToWishlist}
              className="px-6 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition"
            >
              <FiHeart className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Reviews Section */}
      <div className="mt-16">
        <h2 className="text-2xl font-bold mb-6">Customer Reviews</h2>
        {product.reviews && product.reviews.length > 0 ? (
          <div className="space-y-6">
            {product.reviews.map((review) => (
              <div key={review.id} className="bg-white p-6 rounded-lg shadow">
                <div className="flex items-center mb-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <FiStar
                        key={i}
                        className={`w-4 h-4 ${
                          i < review.rating
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="ml-2 font-semibold">{review.user_name}</span>
                  <span className="ml-2 text-gray-500 text-sm">
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-700">{review.comment}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">No reviews yet. Be the first to review this product!</p>
        )}
      </div>
    </div>
  );
};

export default ProductDetail;
