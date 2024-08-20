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

- User creation

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