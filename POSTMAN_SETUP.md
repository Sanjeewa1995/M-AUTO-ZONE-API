# Vehicle Parts API - Postman Collection Setup

## 📋 Overview

This document provides instructions for setting up and using the Postman collection for the Vehicle Parts API. The collection includes all authentication endpoints, JWT token management, and health check endpoints.

## 🚀 Quick Setup

### 1. Import Collection and Environment

1. **Import Collection:**
   - Open Postman
   - Click "Import" button
   - Select `Vehicle_Parts_API.postman_collection.json`
   - Click "Import"

2. **Import Environment:**
   - Click "Import" button again
   - Select `Vehicle_Parts_API.postman_environment.json`
   - Click "Import"

3. **Set Active Environment:**
   - In the top-right corner, select "Vehicle Parts API - Development" environment

### 2. Configure Environment Variables

The environment includes these variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `base_url` | API base URL | `http://localhost:8000` |
| `access_token` | JWT access token | (auto-populated) |
| `refresh_token` | JWT refresh token | (auto-populated) |
| `user_id` | Current user ID | (auto-populated) |
| `user_email` | Current user email | (auto-populated) |

## 📚 API Endpoints

### Authentication Endpoints

#### 1. Register User
- **Method:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/register/`
- **Description:** Register a new user account
- **Body Example:**
```json
{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "user_type": "user",
    "password": "password123",
    "password_confirm": "password123"
}
```

#### 2. Login User
- **Method:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/login/`
- **Description:** Login with email and password
- **Body Example:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

#### 3. Get User Profile
- **Method:** `GET`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Description:** Get current user profile (requires authentication)

#### 4. Update User Profile
- **Method:** `PUT`
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Description:** Update current user profile (requires authentication)
- **Body Example:**
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "+9876543210",
    "user_type": "user"
}
```

#### 5. Logout User
- **Method:** `POST`
- **URL:** `{{base_url}}/api/v1/auth/logout/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Description:** Logout user and blacklist refresh token

### JWT Token Management

#### 1. Get Access Token (SimpleJWT)
- **Method:** `POST`
- **URL:** `{{base_url}}/api/v1/token/`
- **Description:** Get JWT access and refresh tokens using SimpleJWT
- **Body Example:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

#### 2. Refresh Access Token
- **Method:** `POST`
- **URL:** `{{base_url}}/api/v1/token/refresh/`
- **Description:** Refresh access token using refresh token
- **Body Example:**
```json
{
    "refresh": "{{refresh_token}}"
}
```

### Health Check

#### 1. API Health Check
- **Method:** `GET`
- **URL:** `{{base_url}}/api/v1/health/`
- **Description:** Check if the API is running and healthy

## 🔧 Features

### Automatic Token Management
The collection includes automatic token extraction and management:

- **Auto-extraction:** Tokens are automatically extracted from login/register responses
- **Auto-storage:** Tokens are stored in environment variables
- **Auto-usage:** Access tokens are automatically used in authenticated requests

### Test Scripts
Each request includes test scripts that:

- **Validate Response Status:** Ensures responses are successful (200/201)
- **Check Response Time:** Validates response time is under 5 seconds
- **Extract Tokens:** Automatically saves tokens to environment variables

### Pre-request Scripts
The collection includes pre-request scripts that:

- **Auto-set Tokens:** Automatically sets access tokens from previous responses
- **Environment Management:** Manages environment variables seamlessly

## 🧪 Testing Workflow

### 1. Basic Testing Flow

1. **Start Server:**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Test Registration:**
   - Run "Register User" request
   - Verify tokens are automatically saved
   - Check user data in response

3. **Test Login:**
   - Run "Login User" request
   - Verify tokens are updated
   - Check user data in response

4. **Test Authenticated Endpoints:**
   - Run "Get User Profile" request
   - Run "Update User Profile" request
   - Run "Logout User" request

### 2. Token Management Testing

1. **Get Tokens:**
   - Run "Get Access Token" request
   - Verify both access and refresh tokens are returned

2. **Refresh Tokens:**
   - Run "Refresh Access Token" request
   - Verify new access token is returned

### 3. Health Check Testing

1. **API Status:**
   - Run "API Health Check" request
   - Verify API is running and healthy

## 📝 User Types

The API supports different user types:

| User Type | Description |
|-----------|-------------|
| `user` | Regular user (default) |
| `admin` | Administrator |
| `moderator` | Moderator |

## 🔒 Security Features

### JWT Authentication
- **Access Tokens:** Short-lived tokens for API access
- **Refresh Tokens:** Long-lived tokens for token renewal
- **Token Blacklisting:** Logout blacklists refresh tokens

### Password Requirements
- **Minimum Length:** 8 characters
- **Confirmation:** Password confirmation required for registration

### User Model Fields
- **Email:** Unique identifier (no username)
- **Phone:** Optional with validation
- **User Type:** Role-based access control
- **Timestamps:** Created/updated tracking

## 🚨 Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

#### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

#### 500 Internal Server Error
```json
{
    "detail": "A server error occurred."
}
```

## 📊 Response Examples

### Successful Registration
```json
{
    "message": "User registered successfully",
    "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone": "+1234567890",
        "user_type": "user",
        "is_active": true,
        "created_at": "2025-10-13T17:39:30.334365Z",
        "updated_at": "2025-10-13T17:39:30.334372Z"
    }
}
```

### Successful Login
```json
{
    "message": "Login successful",
    "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone": "+1234567890",
        "user_type": "user",
        "is_active": true,
        "created_at": "2025-10-13T17:39:30.334365Z",
        "updated_at": "2025-10-13T17:39:30.334372Z"
    }
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Server Not Running:**
   - Ensure Django server is running on `http://localhost:8000`
   - Check server logs for errors

2. **Token Expired:**
   - Use "Refresh Access Token" request
   - Re-login if refresh token is expired

3. **Authentication Failed:**
   - Verify access token is valid
   - Check Authorization header format: `Bearer {{access_token}}`

4. **CORS Issues:**
   - Ensure CORS is properly configured in Django settings
   - Check allowed origins in settings

### Debug Tips

1. **Check Environment Variables:**
   - Verify `base_url` is correct
   - Check if tokens are properly set

2. **Test Individual Requests:**
   - Start with health check
   - Test registration without authentication
   - Test login with valid credentials

3. **Check Server Logs:**
   - Monitor Django server console for errors
   - Check database connection

## 📞 Support

For issues with the API or Postman collection:

1. **Check Server Status:** Ensure Django server is running
2. **Verify Environment:** Check environment variables
3. **Test Connectivity:** Use health check endpoint
4. **Review Logs:** Check server and database logs

## 🔄 Updates

To update the collection:

1. **Export Current Collection:** Save current collection as backup
2. **Import New Collection:** Import updated collection file
3. **Update Environment:** Import updated environment if needed
4. **Test Endpoints:** Verify all endpoints work correctly

---

**Happy Testing! 🚀**
