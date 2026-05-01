/**
 * Shopping Cart Page
 */
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { FiTrash2, FiShoppingBag } from 'react-icons/fi';

const Cart = () => {
  const { cartItems, loading, updateCartItem, removeFromCart, getCartTotal } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleQuantityChange = (cartId, newQuantity) => {
    if (newQuantity < 1) return;
    updateCartItem(cartId, newQuantity);
  };

  const handleCheckout = () => {
    if (!isAuthenticated()) {
      navigate('/login');
    } else {
      navigate('/checkout');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <FiShoppingBag className="mx-auto h-24 w-24 text-gray-400" />
          <h2 className="mt-4 text-2xl font-bold text-gray-900">Your cart is empty</h2>
          <p className="mt-2 text-gray-600">Start shopping to add items to your cart</p>
          <Link
            to="/products"
            className="mt-6 inline-block px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition"
          >
            Browse Products
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            {cartItems.map((item) => (
              <div
                key={item.id}
                className="flex items-center p-6 border-b last:border-b-0"
              >
                {/* Product Image */}
                <Link to={`/products/${item.product_id}`} className="flex-shrink-0">
                  <div className="w-24 h-24 bg-gray-200 rounded-md overflow-hidden">
                    {item.product?.image_url ? (
                      <img
                        src={item.product.image_url}
                        alt={item.product.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
                        No Image
                      </div>
                    )}
                  </div>
                </Link>

                {/* Product Details */}
                <div className="ml-6 flex-1">
                  <Link
                    to={`/products/${item.product_id}`}
                    className="text-lg font-semibold hover:text-primary-600"
                  >
                    {item.product?.name}
                  </Link>
                  <p className="text-gray-600 mt-1">
                    ${item.product?.price.toFixed(2)} each
                  </p>

                  {/* Quantity Controls */}
                  <div className="flex items-center mt-4 space-x-4">
                    <div className="flex items-center border rounded-md">
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                        className="px-3 py-1 hover:bg-gray-100"
                      >
                        -
                      </button>
                      <span className="px-4 py-1 border-x">{item.quantity}</span>
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                        className="px-3 py-1 hover:bg-gray-100"
                      >
                        +
                      </button>
                    </div>

                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="text-red-600 hover:text-red-700 flex items-center"
                    >
                      <FiTrash2 className="mr-1" />
                      Remove
                    </button>
                  </div>
                </div>

                {/* Subtotal */}
                <div className="ml-6 text-right">
                  <p className="text-xl font-bold text-primary-600">
                    ${item.subtotal.toFixed(2)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6 sticky top-20">
            <h2 className="text-xl font-bold mb-4">Order Summary</h2>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span className="font-semibold">${getCartTotal().toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Shipping</span>
                <span className="font-semibold">Free</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tax</span>
                <span className="font-semibold">$0.00</span>
              </div>
              <div className="border-t pt-3">
                <div className="flex justify-between">
                  <span className="text-lg font-bold">Total</span>
                  <span className="text-2xl font-bold text-primary-600">
                    ${getCartTotal().toFixed(2)}
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleCheckout}
              className="w-full py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition font-semibold"
            >
              Proceed to Checkout
            </button>

            <Link
              to="/products"
              className="block text-center mt-4 text-primary-600 hover:text-primary-700"
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
