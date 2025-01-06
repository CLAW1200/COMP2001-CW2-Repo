# Trail Management API

A RESTful API service for managing hiking trails, users, and location points. Built with Flask and SQLAlchemy, featuring JWT authentication and integration with Plymouth University's authentication system.

## Features

- User management with secure authentication
- Trail CRUD operations with ownership control
- Location point management for mapping trails
- Swagger UI documentation
- Plymouth University SSO integration

## Prerequisites

- Python 3.7+
- SQL Server with ODBC Driver 17
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository
2. Install dependencies:
3. Configure your database connection in config.py:
## Running the Application

Start the server:
The server will run at `http://localhost:8000` by default.

- API Documentation UI: `http://localhost:8000/api/ui`
- Homepage: `http://localhost:8000/`

## API Endpoints

### Authentication
- POST `/api/auth` - Authenticate user and receive JWT token

### Trails
- GET `/api/trail` - List all trails
- POST `/api/trail` - Create new trail (requires authentication)
- GET `/api/trail/{trail_id}` - Get specific trail
- PUT `/api/trail/{trail_id}` - Update trail (requires authentication)
- DELETE `/api/trail/{trail_id}` - Delete trail (requires authentication)

### Users
- GET `/api/user` - List all users
- POST `/api/user` - Create new user
- GET `/api/user/{user_id}` - Get specific user
- PUT `/api/user/{user_id}` - Update user
- DELETE `/api/user/{user_id}` - Delete user

### Locations
- GET `/api/location` - List all locations
- POST `/api/location` - Create new location
- GET `/api/location/{location_id}` - Get specific location
- PUT `/api/location/{location_id}` - Update location
- DELETE `/api/location/{location_id}` - Delete location

## Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Authenticate using Plymouth credentials at `/api/auth`
2. Include the received token in subsequent requests:
## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password
- created_at

### Trails Table
- id (Primary Key)
- name
- length
- owner_id (Foreign Key to Users)

### Locations Table
- id (Primary Key)
- latitude
- longitude
- sequence
- trail_id (Foreign Key to Trails)

## Security Features

- JWT-based authentication
- Plymouth University SSO integration
- Password hashing
- Owner-based access control for trails
- CORS protection