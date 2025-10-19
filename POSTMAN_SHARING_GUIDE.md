# 🚀 Vehicle Parts API - Postman Collection Setup Guide

## 📋 Quick Setup Instructions

### **Step 1: Download Files**
Download these two files:
- `Vehicle_Parts_API.postman_collection.json`
- `Vehicle_Parts_API.postman_environment.json`

### **Step 2: Import into Postman**

1. **Open Postman**
2. **Click "Import" button** (top-left)
3. **Upload Collection:**
   - Drag & drop `Vehicle_Parts_API.postman_collection.json`
   - OR click "Upload Files" and select the file
4. **Upload Environment:**
   - Repeat the same process for `Vehicle_Parts_API.postman_environment.json`

### **Step 3: Select Environment**

1. **Click the environment dropdown** (top-right corner)
2. **Select "Vehicle Parts API - Development"**
3. **Verify the base URL shows:** `http://3.107.165.131:8000`

### **Step 4: Test the API**

1. **Open the collection** in Postman
2. **Try the "Health Check" request** first
3. **Register a new user** using the Register endpoint
4. **Login** with the registered credentials

## 🔧 Environment Variables

The environment includes these variables:
- `base_url`: `http://3.107.165.131:8000` (EC2 instance)
- `host_url`: `3.107.165.131:8000` (host only)
- `local_url`: `http://localhost:8000` (local development)
- `access_token`: (auto-populated after login)
- `refresh_token`: (auto-populated after login)
- `user_id`: (auto-populated after login)
- `user_email`: (auto-populated after login)

## 📚 Available Endpoints

### **Authentication:**
- **POST** `/api/v1/auth/register/` - Register new user
- **POST** `/api/v1/auth/login/` - Login user
- **POST** `/api/v1/auth/logout/` - Logout user
- **GET** `/api/v1/auth/profile/` - Get user profile
- **PUT** `/api/v1/auth/profile/` - Update user profile

### **JWT Tokens:**
- **POST** `/api/v1/token/` - Get JWT tokens
- **POST** `/api/v1/token/refresh/` - Refresh JWT token

### **Health Check:**
- **GET** `/api/v1/health/` - API health status

## 🚨 Troubleshooting

### **If requests fail:**
1. **Check environment is selected** (top-right dropdown)
2. **Verify base URL** shows the EC2 instance
3. **Try the Health Check** endpoint first
4. **Check if the API is running** on EC2

### **If you get 401 Unauthorized:**
1. **Register a new user** first
2. **Login** to get JWT tokens
3. **Use the tokens** for authenticated requests

## 📞 Support

If you encounter any issues:
1. **Check the API status** using the Health Check endpoint
2. **Verify the EC2 instance** is running
3. **Contact the API administrator** for assistance

---

**Happy Testing! 🎉**
