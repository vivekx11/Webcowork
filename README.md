# Advanced E-Commerce Web Application

A full-stack e-commerce platform with admin panel, user shopping interface, and advanced features.

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite
- **Frontend**: React, Tailwind CSS
- **Image Storage**: ImageKit API
- **Authentication**: JWT

## Features

### Admin Panel
- Secure authentication system
- Product management (CRUD operations)
- Order management and status updates
- Dashboard analytics
- Search and filter functionality

### User Interface
- User registration and login
- Product browsing with pagination
- Shopping cart functionality
- Checkout and order placement
- Order history tracking
- Responsive design

### Advanced Features
- Role-based access control
- RESTful API architecture
- Password hashing (bcrypt)
- Stock management
- Product categories and filtering
- Payment integration (Stripe sandbox)
- Wishlist feature
- Ratings and reviews
- Admin analytics with charts

## Project Structure

```
ecommerce-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── config.py
│   ├── migrations/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── utils/
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the backend directory:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///ecommerce.db
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
IMAGEKIT_URL_ENDPOINT=your-imagekit-url-endpoint
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

4. **Initialize database**
```bash
python run.py init-db
```

5. **Run the backend server**
```bash
python run.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment variables**
Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
REACT_APP_IMAGEKIT_URL_ENDPOINT=your-imagekit-url-endpoint
REACT_APP_STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

3. **Run the development server**
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## Default Admin Credentials

After initializing the database, use these credentials to login as admin:
- **Email**: admin@ecommerce.com
- **Password**: admin123

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Product Endpoints
- `GET /api/products` - Get all products (with pagination, filters)
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Create product (Admin only)
- `PUT /api/products/:id` - Update product (Admin only)
- `DELETE /api/products/:id` - Delete product (Admin only)

### Category Endpoints
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create category (Admin only)

### Order Endpoints
- `GET /api/orders` - Get user orders / all orders (Admin)
- `GET /api/orders/:id` - Get single order
- `POST /api/orders` - Create order
- `PUT /api/orders/:id/status` - Update order status (Admin only)

### Cart Endpoints
- `GET /api/cart` - Get user cart
- `POST /api/cart` - Add to cart
- `PUT /api/cart/:id` - Update cart item
- `DELETE /api/cart/:id` - Remove from cart

### Wishlist Endpoints
- `GET /api/wishlist` - Get user wishlist
- `POST /api/wishlist` - Add to wishlist
- `DELETE /api/wishlist/:id` - Remove from wishlist

### Review Endpoints
- `GET /api/products/:id/reviews` - Get product reviews
- `POST /api/products/:id/reviews` - Add review
- `PUT /api/reviews/:id` - Update review
- `DELETE /api/reviews/:id` - Delete review

### Admin Analytics Endpoints
- `GET /api/admin/analytics` - Get dashboard analytics
- `GET /api/admin/sales` - Get sales data

## Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- password_hash
- first_name
- last_name
- role (admin/user)
- created_at
- updated_at

### Products Table
- id (Primary Key)
- name
- description
- price
- category_id (Foreign Key)
- stock
- image_url
- created_at
- updated_at

### Categories Table
- id (Primary Key)
- name
- description

### Orders Table
- id (Primary Key)
- user_id (Foreign Key)
- total_amount
- status (pending/shipped/delivered)
- payment_status
- shipping_address
- created_at
- updated_at

### Order Items Table
- id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- price

### Cart Table
- id (Primary Key)
- user_id (Foreign Key)
- product_id (Foreign Key)
- quantity

### Wishlist Table
- id (Primary Key)
- user_id (Foreign Key)
- product_id (Foreign Key)

### Reviews Table
- id (Primary Key)
- user_id (Foreign Key)
- product_id (Foreign Key)
- rating (1-5)
- comment
- created_at

## Deployment

### Local Deployment
Follow the setup instructions above.

### Production Deployment

#### Backend (Heroku/Railway)
1. Create a production database
2. Set environment variables
3. Deploy using Git
4. Run database migrations

#### Frontend (Vercel/Netlify)
1. Build the React app: `npm run build`
2. Deploy the build folder
3. Set environment variables

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Input validation and sanitization
- SQL injection prevention
- CORS configuration
- Rate limiting

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
