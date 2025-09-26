# Flask Authentication Lab - Complete Solution

A Flask blog application with user authentication functionality.

## Features

- User login with username
- User logout
- Session persistence (stay logged in after page refresh)
- Blog articles with view limits for non-authenticated users

## Quick Start

1. **Setup**
   ```bash
   pipenv install && pipenv shell
   npm install --prefix client
   cd server
   flask db upgrade
   python seed.py
   ```

2. **Run the Application**
   ```bash
   # Terminal 1 - Flask API
   python app.py
   
   # Terminal 2 - React Frontend
   npm start --prefix client
   ```

3. **Run Tests**
   ```bash
   pytest
   ```

## API Endpoints

### Authentication Routes

- **POST /login** - Login with username
  ```json
  {"username": "testuser1"}
  ```

- **DELETE /logout** - Logout current user

- **GET /check_session** - Check if user is logged in

### Other Routes

- **GET /articles** - Get all articles
- **GET /articles/:id** - Get specific article (3 view limit)
- **DELETE /clear** - Clear session data

## Project Structure

```
├── client/          # React frontend
├── server/
│   ├── app.py       # Main Flask application
│   ├── models.py    # Database models
│   ├── seed.py      # Database seeding
│   └── testing/     # Test files
└── README.md
```

## Technologies

- **Backend**: Flask, SQLAlchemy, Flask-RESTful
- **Frontend**: React
- **Database**: SQLite
- **Testing**: Pytest

## Authentication Flow

1. User enters username in login form
2. Backend finds user and sets `session['user_id']`
3. User remains logged in until logout or session expires
4. Protected routes check session for authentication

## Test Users

The seed script creates test users:
- testuser1
- testuser2

Use these usernames to test the login functionality.