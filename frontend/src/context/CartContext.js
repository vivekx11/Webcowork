/**
 * Cart Context
 * Manages shopping cart state and provides cart methods
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import { cartAPI } from '../services/api';
import { useAuth } from './AuthContext';
import toast from 'react-hot-toast';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  // Load cart when user is authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      fetchCart();
    } else {
      setCartItems([]);
    }
  }, [isAuthenticated]);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const response = await cartAPI.get();
      setCartItems(response.data.cart_items || []);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      const response = await cartAPI.add({ product_id: productId, quantity });
      await fetchCart();
      toast.success('Added to cart!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to add to cart';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const updateCartItem = async (cartId, quantity) => {
    try {
      await cartAPI.update(cartId, { quantity });
      await fetchCart();
      toast.success('Cart updated!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to update cart';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const removeFromCart = async (cartId) => {
    try {
      await cartAPI.remove(cartId);
      await fetchCart();
      toast.success('Removed from cart!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to remove from cart';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const clearCart = async () => {
    try {
      await cartAPI.clear();
      setCartItems([]);
      toast.success('Cart cleared!');
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.error || 'Failed to clear cart';
      toast.error(message);
      return { success: false, error: message };
    }
  };

  const getCartTotal = () => {
    return cartItems.reduce((total, item) => total + (item.subtotal || 0), 0);
  };

  const getCartCount = () => {
    return cartItems.reduce((count, item) => count + item.quantity, 0);
  };

  const value = {
    cartItems,
    loading,
    fetchCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    getCartTotal,
    getCartCount,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};
