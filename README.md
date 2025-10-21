# Vehicle Parts API

A Django REST API with JWT authentication system for user management and authentication.

## Features

- **User Authentication**: Complete JWT-based authentication system
- **User Registration**: Create new user accounts with validation
- **User Login**: Secure login with JWT tokens
- **User Profile Management**: View and update user profiles
- **Token Management**: Access and refresh token handling
- **Security**: Password validation, token blacklisting, and secure endpoints

## Authentication System

The API uses JWT (JSON Web Tokens) for authentication with the following features:
- **Access Tokens**: Short-lived tokens (60 minutes) for API access
- **Refresh Tokens**: Long-lived tokens (7 days) for token renewal
- **Token Blacklisting**: Secure logout by blacklisting refresh tokens
- **Password Validation**: Minimum 8 characters with confirmation

## API Endpoints

### Authentication Endpoints

#### User Registration
- **POST** `/api/v1/auth/register/` - Register a new user
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }
  ```

#### User Login
- **POST** `/api/v1/auth/login/` - Login user
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```

#### User Logout
- **POST** `/api/v1/auth/logout/` - Logout user (requires authentication)
  ```json
  {
    "refresh": "your_refresh_token_here"
  }
  ```

#### User Profile
- **GET** `/api/v1/auth/profile/` - Get current user profile (requires authentication)
- **PUT/PATCH** `/api/v1/auth/profile/update/` - Update user profile (requires authentication)

#### Token Management
- **POST** `/api/v1/auth/refresh/` - Refresh access token
  ```json
  {
    "refresh": "your_refresh_token_here"
  }
  ```

### JWT Token Endpoints (Built-in)
- **POST** `/api/v1/token/` - Obtain JWT tokens (alternative login)
- **POST** `/api/v1/token/refresh/` - Refresh JWT tokens

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vehicle-parts-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Database Configuration

The project is configured to use PostgreSQL by default. Make sure you have PostgreSQL installed and create a database named `vehicle_parts_db` (or update the settings in your `.env` file).

## API Documentation

Once the server is running, you can access:
- **API Root**: http://localhost:8000/api/v1/
- **Admin Interface**: http://localhost:8000/admin/
- **Browsable API**: Navigate to any endpoint for interactive API documentation

## Filtering and Search

The API supports various filtering options:

### Parts Filtering
- `category` - Filter by category ID
- `brand` - Filter by brand ID
- `condition` - Filter by condition (new, used, refurbished)
- `status` - Filter by status (available, out_of_stock, discontinued)
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `in_stock` - Filter by stock availability
- `low_stock` - Filter parts with low stock
- `search` - Search in name, part_number, and description

### Example API Calls
```bash
# Get all available parts
GET /api/v1/parts/?status=available&in_stock=true

# Search for brake parts
GET /api/v1/parts/?search=brake

# Get parts for a specific vehicle
GET /api/v1/parts/by_vehicle/?make=Toyota&model=Camry&year=2020

# Get low stock parts
GET /api/v1/parts/low_stock/
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
# Test deployment Tue Oct 21 18:54:19 +0530 2025
# Force deployment update Tue Oct 21 19:01:26 +0530 2025
