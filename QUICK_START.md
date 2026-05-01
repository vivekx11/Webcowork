# 🚀 Quick Start Guide

Get your e-commerce application running in **10 minutes**!

## Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)

## Step 1: Backend Setup (5 minutes)

Open a terminal and run these commands:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Initialize database
python run.py init-db

# Start backend server
python run.py
```

✅ Backend should now be running on `http://localhost:5000`

**Keep this terminal open!**

## Step 2: Frontend Setup (5 minutes)

Open a **NEW** terminal and run these commands:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start frontend server
npm start
```

✅ Frontend should now be running on `http://localhost:3000`

Your browser should automatically open to the application!

## Step 3: Test the Application

### Login as Admin

1. Click "Login" in the top right
2. Use these credentials:
   - **Email:** `admin@ecommerce.com`
   - **Password:** `admin123`
3. Click on your name → "Admin Dashboard"

### Add Your First Product

1. In Admin Dashboard, click "Manage Products"
2. Click "Add Product" (note: full admin interface is a placeholder - use API or extend it)
3. For now, you can test with the existing setup

### Create a User Account

1. Logout from admin
2. Click "Login" → "create a new account"
3. Fill in your details
4. Register and start shopping!

## 🎉 You're All Set!

Your e-commerce application is now running!

## What's Next?

1. **Customize the Design**
   - Edit `frontend/src/index.css` for global styles
   - Modify `frontend/tailwind.config.js` for theme colors

2. **Add Products**
   - Use the admin panel
   - Or use API endpoints (see API_DOCUMENTATION.md)

3. **Configure Optional Services**
   - ImageKit for image storage
   - Stripe for payment processing

4. **Extend Features**
   - Complete admin pages (Products, Orders, Users)
   - Add more user features
   - Implement email notifications

## 📚 Documentation

- **SETUP_GUIDE.md** - Detailed setup instructions
- **API_DOCUMENTATION.md** - Complete API reference
- **PROJECT_SUMMARY.md** - Project overview
- **README.md** - Features and architecture

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" error:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal
pip install -r requirements.txt
```

**"Port 5000 already in use":**
```bash
# Change port in backend/run.py
# Line: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**"npm: command not found":**
- Install Node.js from [nodejs.org](https://nodejs.org/)

**"Port 3000 already in use":**
- The app will ask if you want to use a different port
- Type 'Y' and press Enter

**API connection errors:**
- Make sure backend is running on port 5000
- Check browser console for errors (F12)

## 🔑 Default Credentials

**Admin Account:**
- Email: `admin@ecommerce.com`
- Password: `admin123`

⚠️ **IMPORTANT:** Change the admin password after first login!

## 📊 Test Data

The database starts with:
- 1 admin user
- 6 default categories (Electronics, Clothing, Books, etc.)
- 0 products (add your own!)

## 🎯 Quick Testing Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access home page
- [ ] Can login as admin
- [ ] Can access admin dashboard
- [ ] Can register new user
- [ ] Can browse products page
- [ ] Can view cart

## 💡 Pro Tips

1. **Keep both terminals open** - One for backend, one for frontend
2. **Check terminal output** - Errors will show here
3. **Use browser DevTools** - Press F12 to see console errors
4. **Hot reload enabled** - Changes auto-refresh (no restart needed)

## 🚀 Ready to Deploy?

See **SETUP_GUIDE.md** section "Production Deployment" for deployment instructions.

## 📞 Need Help?

1. Check error messages in terminal
2. Review SETUP_GUIDE.md for detailed instructions
3. Check API_DOCUMENTATION.md for API usage
4. Verify environment variables in .env files

---

**Happy Coding! 🎉**

Now go build something amazing!
