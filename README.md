# Expense Tracking Application

This project is a backend service for a Expense Tracking Application, built using the FastAPI framework.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project is an expense tracking application built with FastAPI for the backend and React for the frontend. It allows users to manage and track their expenses, categorize them, and generate reports. The application uses PostgreSQL as the database and SQLAlchemy as the ORM.


## Features

- **User Management**:
  - **User Creation**: 
    - Create new user accounts with essential details.
  - **User Authentication**: 
    - Secure login mechanism with token-based authentication to manage user sessions.
  - **Retrieve Users**: 
    - Fetch a list of users with support for pagination and sorting options.
  - **Update User Details**: 
    - Modify user profile information, including first name, last name, and role.
  - **Update User Password**: 
    - Change user password with validation to ensure security.
  - **Delete User**: 
    - Remove a user account from the system.

- **Role Management**:
  - **Create Role**: 
    - Define new roles with specific permissions and attributes.
  - **Update Role**: 
    - Modify existing roles, including updating role details.
  - **Retrieve Roles**: 
    - Get a list of all roles with support for pagination and sorting.
  - **Retrieve Role by ID**: 
    - Fetch detailed information for a specific role using its ID.
  - **Delete Role**: 
    - Remove a role from the system by its ID.

- **Token-Based Authentication**: 
  - Implement token-based authentication to secure access to private routes and manage user sessions.

- **Role-Based Access Control**: 
  - Enforce role-based access control to restrict API route access based on user roles, ensuring appropriate permissions and security levels.




## Installation

To set up the project locally, follow these steps:

### Clone the repository:

```bash
git clone https://github.com/Abhishek2063/Expense_tracking_backend_python_fastapi.git
cd Expense_tracking_backend_python_fastapi
```

### Create a virtual environment:

```bash
python -m venv expense_tracking_venv
source expense_tracking_venv/bin/activate  # On Windows use `expense_tracking_venv\Scripts\activate`
```

### Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a .env file in the root directory of the project and add the following environment variables:

```bash
# Common settings
ENVIORNMENT="local" #production
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Local environment
LOCAL_API_URL="http://127.0.0.1:8000/"
LOCAL_DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
LOCAL_APP_URL=""

# Production environment
PROD_API_URL="https://expense-tracking-backend-python-fastapi.onrender.com/"
PROD_APP_URL=""
PROD_DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"


```

## Running the Application

To run the application locally, use the following command:

```bash
uvicorn main:app --reload
The application will be accessible at http://127.0.0.1:8000.
```

## API Endpoints

Here are the available API endpoints:

### Create User

POST /api/user/

Request Body:

```bash
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123!"
}
```

### User Authentication

POST /api/auth/login

Request Body:

```bash
{
    "email": "john.doe@example.com",
    "password": "password123!"
}
```

### Get All Users

GET /api/users/

```bash
Query Parameters: order, sort_by, skip, limit

Example: http://127.0.0.1:8000/api/user/get_all_users/?order=asc&sort_by=email&skip=0&limit=10
```


### Get User by ID:

GET /api/users/{user_id}

```bash
Example: http://127.0.0.1:8000/api/user/1
```

### User Update By ID

PUT /api/users/{user_id}

Request Body:

```bash
{
    "first_name": "John",
    "last_name": "Doe",
    "role_id": 1
}
```

### User Update Password

PUT /api/users/password_update/{user_id}

Request Body:

```bash
{
    "current_password" : "Test#1234",
    "new_password" : "Test@1234"
}
```

### Delete User by ID:

DELETE /api/users/{user_id}

```bash
Example: http://127.0.0.1:8000/api/user/1
```


### Create Role

POST /api/role

Request Body:

```bash
{
    "name" : "admin",
    "description" : "All permission access"
}
```

### Get All User roles list

GET /api/role

```bash
Query Parameters: sort_order, sort_by, skip, limit

Example: http://127.0.0.1:8000/api/role/?sort_order=asc&sort_by=name&skip=0&limit=10
```

### Get User Role by ID:

GET /api/role/{role_id}

```bash
Example: http://127.0.0.1:8000/api/role/{role_id}
```

### User Role Update By ID

PUT /api/role/{role_id}

Request Body:

```bash
{
    "name" : "admin",
    "description" : "All permission access"
}
```

### Delete User role by ID:

DELETE /api/role/{role_id}

```bash
Example: http://127.0.0.1:8000/api/role/1
```


## Dependencies

The project dependencies are listed in requirements.txt:

```bash
uvicorn
fastapi
sqlalchemy
pydantic
python-dotenv
databases[postgresql] 
asyncpg
psycopg2-binary
bcrypt==4.0.1
passlib[bcrypt]
pydantic[email]

```

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.