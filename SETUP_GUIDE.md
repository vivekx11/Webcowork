# E-Commerce Application - Complete Setup Guide

This guide will walk you through setting up and running the full-stack e-commerce application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** and npm - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

## Project Structure

```
ecommerce-app/
├── backend/          # Python Flask backend
├── frontend/         # React frontend
├── README.md         # Project documentation
└── SETUP_GUIDE.md    # This file
```

## Part 1: Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including Flask, SQLAlchemy, JWT, etc.

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Open `.env` file and configure the following:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too
FLASK_ENV=development

# Database (SQLite - no configuration needed)
DATABASE_URL=sqlite:///ecommerce.db

# ImageKit Configuration (Sign up at https://imagekit.io/)
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id

# Stripe Configuration (Get test keys from https://stripe.com/)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# CORS
FRONTEND_URL=http://localhost:3000
```

**Important Notes:**
- Generate strong random strings for SECRET_KEY and JWT_SECRET_KEY
- ImageKit is optional for development (products can work without images)
- Stripe is optional (you can test without payment integration)

### Step 5: Initialize Database

```bash
python run.py init-db
```

This will:
- Create all database tables
- Create a default admin user
- Create default product categories

**Default Admin Credentials:**
- Email: `admin@ecommerce.com`
- Password: `admin123`

⚠️ **IMPORTANT:** Change the admin password after first login!

### Step 6: Run Backend Server

```bash
python run.py
```

The backend server will start on `http://localhost:5000`

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * Restarting with stat
```

**Test the API:**
Open your browser and visit: `http://localhost:5000/api/health`

You should see: `{"status": "healthy", "message": "E-commerce API is running"}`

---

## Part 2: Frontend Setup

### Step 1: Open New Terminal

Keep the backend server running and open a new terminal window.

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Node Dependencies

```bash
npm install
```

This will install React, Tailwind CSS, Axios, and other dependencies.

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Open `.env` file and configure:

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
REACT_APP_IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_imagekit_id
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

**Note:** Use the same ImageKit and Stripe keys as in the backend.

### Step 5: Run Frontend Development Server

```bash
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

---

## Part 3: Testing the Application

### 1. Access the Application

Open your browser and go to: `http://localhost:3000`

### 2. Test User Registration

1. Click "Login" in the navigation bar
2. Click "create a new account"
3. Fill in the registration form
4. Submit to create a user account

### 3. Test Admin Panel

1. Logout if you're logged in as a regular user
2. Login with admin credentials:
   - Email: `admin@ecommerce.com`
   - Password: `admin123`
3. Click on your name → "Admin Dashboard"
4. You should see the admin panel with analytics

### 4. Add Products (Admin)

1. In Admin Dashboard, go to "Products"
2. Click "Add Product"
3. Fill in product details:
   - Name
   - Description
   - Price
   - Category
   - Stock quantity
   - Image (optional if ImageKit is configured)
4. Click "Create Product"

### 5. Test Shopping Flow (User)

1. Logout from admin account
2. Login as a regular user (or register new account)
3. Browse products on the home page
4. Click on a product to view details
5. Click "Add to Cart"
6. View cart by clicking the cart icon
7. Proceed to checkout
8. Fill in shipping information
9. Complete order (payment optional)

### 6. Test Order Management (Admin)

1. Login as admin
2. Go to Admin Dashboard → Orders
3. View all orders placed by users
4. Click on an order to view details
5. Update order status (pending → processing → shipped → delivered)

---

## Part 4: API Testing with Postman/Thunder Client

### Import API Collection

You can test the API endpoints using tools like Postman or Thunder Client.

### Example API Endpoints:

**Authentication:**
```
POST http://localhost:5000/api/auth/register
POST http://localhost:5000/api/auth/login
GET  http://localhost:5000/api/auth/me
```

**Products:**
```
GET    http://localhost:5000/api/products
GET    http://localhost:5000/api/products/1
POST   http://localhost:5000/api/products (Admin only)
PUT    http://localhost:5000/api/products/1 (Admin only)
DELETE http://localhost:5000/api/products/1 (Admin only)
```

**Cart:**
```
GET    http://localhost:5000/api/cart
POST   http://localhost:5000/api/cart
PUT    http://localhost:5000/api/cart/1
DELETE http://localhost:5000/api/cart/1
```

**Orders:**
```
GET  http://localhost:5000/api/orders
POST http://localhost:5000/api/orders
GET  http://localhost:5000/api/orders/1
PUT  http://localhost:5000/api/orders/1/status (Admin only)
```

### Authentication Header

For protected endpoints, include the JWT token:
```
Authorization: Bearer <your_jwt_token>
```

---

## Part 5: Optional Integrations

### ImageKit Setup (Image Storage)

1. Sign up at [https://imagekit.io/](https://imagekit.io/)
2. Get your credentials from the dashboard:
   - Private Key
   - Public Key
   - URL Endpoint
3. Add them to both backend and frontend `.env` files
4. Restart both servers

### Stripe Setup (Payment Processing)

1. Sign up at [https://stripe.com/](https://stripe.com/)
2. Get your test API keys from the dashboard
3. Add them to both backend and frontend `.env` files
4. Use test card numbers for testing:
   - Success: `4242 4242 4242 4242`
   - Decline: `4000 0000 0000 0002`
   - Any future expiry date and any 3-digit CVC

---

## Part 6: Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem:** Database errors
**Solution:** Delete the database and reinitialize:
```bash
rm ecommerce.db
python run.py init-db
```

**Problem:** Port 5000 already in use
**Solution:** Change the port in `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**Problem:** `npm: command not found`
**Solution:** Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem:** Port 3000 already in use
**Solution:** The app will prompt you to use a different port, or set it manually:
```bash
PORT=3001 npm start
```

**Problem:** API connection errors
**Solution:** 
1. Ensure backend is running on port 5000
2. Check REACT_APP_API_URL in frontend `.env`
3. Check browser console for CORS errors

### CORS Issues

If you see CORS errors in the browser console:

1. Check that FRONTEND_URL in backend `.env` matches your frontend URL
2. Restart the backend server after changing `.env`

---

## Part 7: Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Backend:** Flask automatically reloads when you save Python files
- **Frontend:** React automatically reloads when you save JS/JSX files

### Database Management

View database contents:
```bash
# Install SQLite browser or use command line
sqlite3 backend/ecommerce.db
.tables
SELECT * FROM users;
.quit
```

### Logs

- **Backend logs:** Visible in the terminal running `python run.py`
- **Frontend logs:** Check browser console (F12)

---

## Part 8: Production Deployment

### Backend Deployment (Heroku/Railway)

1. Set environment variables in hosting platform
2. Change `FLASK_ENV=production`
3. Use PostgreSQL instead of SQLite for production
4. Set strong SECRET_KEY and JWT_SECRET_KEY
5. Enable HTTPS

### Frontend Deployment (Vercel/Netlify)

1. Build the production bundle:
```bash
npm run build
```

2. Deploy the `build` folder
3. Set environment variables in hosting platform
4. Update REACT_APP_API_URL to production backend URL

---

## Part 9: Security Checklist

Before deploying to production:

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set proper CORS origins
- [ ] Use production Stripe keys (not test keys)
- [ ] Enable rate limiting
- [ ] Set up proper logging
- [ ] Regular security updates
- [ ] Backup database regularly

---

## Support

If you encounter any issues:

1. Check this guide thoroughly
2. Review error messages in terminal/console
3. Check the README.md for API documentation
4. Verify all environment variables are set correctly

---

## Next Steps

After successful setup:

1. Explore the admin dashboard
2. Add products and categories
3. Test the complete shopping flow
4. Customize the UI/UX
5. Add more features as needed

Happy coding! 🚀
