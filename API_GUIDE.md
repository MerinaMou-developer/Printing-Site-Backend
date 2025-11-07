# PrintPro API - Complete Integration Guide

This guide provides detailed examples for integrating the PrintPro API with your frontend application.

## 🎯 Quick Start Integration

### Base Configuration

```typescript
// config/api.ts
export const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
};

// Helper function for API calls
export async function apiCall(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const url = `${API_CONFIG.baseUrl}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'API request failed');
  }

  return response.json();
}
```

## 🔐 Authentication Flow

### 1. User Registration

```typescript
// services/auth.ts
export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone?: string;
}

export async function register(data: RegisterData) {
  return apiCall('/auth/register/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Usage in component
const handleRegister = async (formData: RegisterData) => {
  try {
    const response = await register(formData);
    // Store tokens
    localStorage.setItem('access_token', response.tokens.access);
    localStorage.setItem('refresh_token', response.tokens.refresh);
    // Store user data
    localStorage.setItem('user', JSON.stringify(response.user));
    // Redirect to dashboard
    router.push('/dashboard');
  } catch (error) {
    console.error('Registration failed:', error);
  }
};
```

### 2. User Login

```typescript
export interface LoginData {
  username: string;
  password: string;
}

export async function login(data: LoginData) {
  return apiCall('/auth/login/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Usage
const handleLogin = async (credentials: LoginData) => {
  try {
    const response = await login(credentials);
    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);
    
    // Fetch user profile
    const profile = await getProfile(response.access);
    localStorage.setItem('user', JSON.stringify(profile));
    
    router.push('/dashboard');
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

### 3. Token Management

```typescript
// utils/auth.ts
export function getAccessToken(): string | null {
  return localStorage.getItem('access_token');
}

export function getRefreshToken(): string | null {
  return localStorage.getItem('refresh_token');
}

export async function refreshAccessToken(): Promise<string> {
  const refreshToken = getRefreshToken();
  
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await apiCall('/auth/token/refresh/', {
    method: 'POST',
    body: JSON.stringify({ refresh: refreshToken }),
  });

  localStorage.setItem('access_token', response.access);
  return response.access;
}

// Authenticated API call with auto-refresh
export async function authenticatedApiCall(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  let token = getAccessToken();

  try {
    return await apiCall(endpoint, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (error: any) {
    // If unauthorized, try to refresh token
    if (error.status === 401) {
      token = await refreshAccessToken();
      return await apiCall(endpoint, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        },
      });
    }
    throw error;
  }
}
```

## 📦 Products Integration

### Fetch All Products

```typescript
// services/products.ts
export interface Product {
  id: number;
  name: string;
  slug: string;
  category: string;
  category_name: string;
  description: string;
  short_description: string;
  price: string;
  sale_price: string | null;
  current_price: string;
  main_image: string | null;
  in_stock: boolean;
  is_featured: boolean;
  created_at: string;
}

export async function getProducts(params?: {
  category?: string;
  search?: string;
  in_stock?: boolean;
  page?: number;
}): Promise<{ results: Product[]; count: number }> {
  const queryParams = new URLSearchParams();
  
  if (params?.category) queryParams.append('category', params.category);
  if (params?.search) queryParams.append('search', params.search);
  if (params?.in_stock) queryParams.append('in_stock', 'true');
  if (params?.page) queryParams.append('page', params.page.toString());

  const query = queryParams.toString();
  return apiCall(`/products/${query ? `?${query}` : ''}`);
}

export async function getProduct(slug: string): Promise<Product> {
  return apiCall(`/products/${slug}/`);
}

export async function getFeaturedProducts(): Promise<Product[]> {
  return apiCall('/products/featured/');
}

export async function searchProducts(query: string): Promise<Product[]> {
  return apiCall(`/products/search/?q=${encodeURIComponent(query)}`);
}
```

### Product Display Component

```tsx
// components/ProductCard.tsx
import Image from 'next/image';
import { Product } from '@/services/products';

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: number) => void;
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const hasDiscount = product.sale_price && 
    parseFloat(product.sale_price) < parseFloat(product.price);

  return (
    <div className="card">
      {product.main_image && (
        <Image
          src={product.main_image}
          alt={product.name}
          width={300}
          height={300}
          className="w-full h-48 object-cover"
        />
      )}
      
      <div className="p-4">
        <h3 className="font-bold text-lg">{product.name}</h3>
        <p className="text-sm text-gray-600">{product.short_description}</p>
        
        <div className="mt-2 flex items-center gap-2">
          {hasDiscount ? (
            <>
              <span className="text-lg font-bold text-green-600">
                AED {product.current_price}
              </span>
              <span className="text-sm line-through text-gray-500">
                AED {product.price}
              </span>
            </>
          ) : (
            <span className="text-lg font-bold">
              AED {product.price}
            </span>
          )}
        </div>

        {product.in_stock ? (
          <button
            onClick={() => onAddToCart(product.id)}
            className="mt-4 w-full btn btn-primary"
          >
            Add to Cart
          </button>
        ) : (
          <button disabled className="mt-4 w-full btn btn-disabled">
            Out of Stock
          </button>
        )}
      </div>
    </div>
  );
}
```

## 🛒 Shopping Cart Integration

### Cart Service

```typescript
// services/cart.ts
export interface CartItem {
  id: number;
  product: number;
  product_name: string;
  product_slug: string;
  product_image: string | null;
  variant: number | null;
  variant_name: string | null;
  quantity: number;
  price: string;
  total_price: string;
}

export interface Cart {
  id: number;
  items: CartItem[];
  total_items: number;
  subtotal: string;
}

export async function getCart(): Promise<Cart> {
  return authenticatedApiCall('/cart/retrieve/');
}

export async function addToCart(
  productId: number,
  quantity: number = 1,
  variantId?: number
): Promise<{ cart: Cart; message: string }> {
  return authenticatedApiCall('/cart/add_item/', {
    method: 'POST',
    body: JSON.stringify({
      product_id: productId,
      quantity,
      variant_id: variantId,
    }),
  });
}

export async function updateCartItem(
  itemId: number,
  quantity: number
): Promise<{ cart: Cart; message: string }> {
  return authenticatedApiCall(`/cart/items/${itemId}/`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
}

export async function removeCartItem(
  itemId: number
): Promise<{ cart: Cart; message: string }> {
  return authenticatedApiCall(`/cart/items/${itemId}/`, {
    method: 'DELETE',
  });
}

export async function clearCart(): Promise<{ cart: Cart; message: string }> {
  return authenticatedApiCall('/cart/clear/', {
    method: 'POST',
  });
}
```

### Cart Hook

```typescript
// hooks/useCart.ts
import { useState, useEffect } from 'react';
import * as CartService from '@/services/cart';

export function useCart() {
  const [cart, setCart] = useState<CartService.Cart | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchCart = async () => {
    setLoading(true);
    try {
      const data = await CartService.getCart();
      setCart(data);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const addItem = async (productId: number, quantity: number = 1) => {
    try {
      const response = await CartService.addToCart(productId, quantity);
      setCart(response.cart);
      return response;
    } catch (error) {
      console.error('Failed to add item:', error);
      throw error;
    }
  };

  const updateItem = async (itemId: number, quantity: number) => {
    try {
      const response = await CartService.updateCartItem(itemId, quantity);
      setCart(response.cart);
      return response;
    } catch (error) {
      console.error('Failed to update item:', error);
      throw error;
    }
  };

  const removeItem = async (itemId: number) => {
    try {
      const response = await CartService.removeCartItem(itemId);
      setCart(response.cart);
      return response;
    } catch (error) {
      console.error('Failed to remove item:', error);
      throw error;
    }
  };

  const clear = async () => {
    try {
      const response = await CartService.clearCart();
      setCart(response.cart);
      return response;
    } catch (error) {
      console.error('Failed to clear cart:', error);
      throw error;
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  return {
    cart,
    loading,
    fetchCart,
    addItem,
    updateItem,
    removeItem,
    clear,
  };
}
```

## 📦 Orders & Checkout

### Checkout Service

```typescript
// services/orders.ts
export interface CheckoutData {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  company_name?: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state?: string;
  country: string;
  postal_code?: string;
  order_notes?: string;
}

export interface Order {
  id: number;
  order_number: string;
  full_name: string;
  email: string;
  phone: string;
  status: string;
  payment_status: string;
  subtotal: string;
  shipping_cost: string;
  tax: string;
  total: string;
  items: OrderItem[];
  created_at: string;
}

export async function checkout(
  data: CheckoutData,
  files?: Record<string, File>
): Promise<Order> {
  const formData = new FormData();
  
  // Add checkout data
  Object.entries(data).forEach(([key, value]) => {
    if (value) formData.append(key, value);
  });

  // Add files if provided
  if (files) {
    Object.entries(files).forEach(([key, file]) => {
      formData.append(key, file);
    });
  }

  const token = getAccessToken();
  const response = await fetch(`${API_CONFIG.baseUrl}/orders/checkout/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Checkout failed');
  }

  return response.json();
}

export async function getOrders(): Promise<Order[]> {
  const response = await authenticatedApiCall('/orders/');
  return response.results;
}

export async function getOrder(id: number): Promise<Order> {
  return authenticatedApiCall(`/orders/${id}/`);
}
```

### Checkout Form Component

```tsx
// components/CheckoutForm.tsx
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { checkout, CheckoutData } from '@/services/orders';
import { useCart } from '@/hooks/useCart';

export function CheckoutForm() {
  const router = useRouter();
  const { cart, clear } = useCart();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<CheckoutData>({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address_line_1: '',
    city: '',
    country: 'UAE',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const order = await checkout(formData);
      await clear(); // Clear cart after successful order
      router.push(`/orders/${order.id}`);
    } catch (error) {
      console.error('Checkout failed:', error);
      alert('Checkout failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <input
          type="text"
          placeholder="First Name *"
          required
          value={formData.first_name}
          onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
          className="input"
        />
        <input
          type="text"
          placeholder="Last Name *"
          required
          value={formData.last_name}
          onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
          className="input"
        />
      </div>

      <input
        type="email"
        placeholder="Email *"
        required
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        className="input"
      />

      <input
        type="tel"
        placeholder="Phone *"
        required
        value={formData.phone}
        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
        className="input"
      />

      <input
        type="text"
        placeholder="Address *"
        required
        value={formData.address_line_1}
        onChange={(e) => setFormData({ ...formData, address_line_1: e.target.value })}
        className="input"
      />

      <input
        type="text"
        placeholder="City *"
        required
        value={formData.city}
        onChange={(e) => setFormData({ ...formData, city: e.target.value })}
        className="input"
      />

      <button
        type="submit"
        disabled={loading || !cart?.items.length}
        className="w-full btn btn-primary"
      >
        {loading ? 'Processing...' : 'Place Order'}
      </button>
    </form>
  );
}
```

## 📊 Categories Integration

```typescript
// services/categories.ts
export interface Category {
  id: number;
  name: string;
  slug: string;
  image: string | null;
  is_active: boolean;
}

export async function getCategories(): Promise<Category[]> {
  return apiCall('/categories/');
}

export async function getCategory(slug: string): Promise<Category> {
  return apiCall(`/categories/${slug}/`);
}

export async function getCategoryProducts(
  slug: string
): Promise<Product[]> {
  const response = await apiCall(`/categories/${slug}/products/`);
  return response.results || response;
}
```

## 🎯 Best Practices

### Error Handling

```typescript
// utils/errorHandler.ts
export function handleApiError(error: any) {
  if (error.response) {
    // Server responded with error
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return 'Invalid request. Please check your input.';
      case 401:
        return 'Authentication required. Please login.';
      case 403:
        return 'You don't have permission to perform this action.';
      case 404:
        return 'Resource not found.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return data.message || 'An error occurred.';
    }
  }
  
  return 'Network error. Please check your connection.';
}
```

### Loading States

```typescript
// components/LoadingSpinner.tsx
export function LoadingSpinner() {
  return (
    <div className="flex justify-center items-center p-8">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}
```

### Type Safety

Always use TypeScript interfaces for API responses to ensure type safety and better developer experience.

---

**For more examples and detailed API documentation, visit: http://localhost:8000/api/docs/**

