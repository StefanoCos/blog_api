# Blog API

A RESTful API for a simple blog platform built with FastAPI and PostgreSQL.

## Features

- User authentication with JWT tokens
- Create, read, update, and delete blog posts
- Add, read, update, and delete comments on posts
- Pagination for listing posts and comments
- Containerized with Docker
- Interactive API documentation with Swagger UI

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development without Docker)

## Getting Started

### With Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd blog_api
   ```

2. Copy the example environment file and update the values if needed:
   ```bash
   cp .env.example .env
   ```

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

4. The API will be available at `http://localhost:8000`
5. Access the interactive API documentation at `http://localhost:8000/docs`
6. Access pgAdmin at `http://localhost:5050` (default credentials: admin@admin.com/admin)

### Without Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd blog_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update the .env file with your database credentials
   ```

5. Initialize the database:
   ```bash
   python -m app.db.init_db
   ```

6. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /api/v1/register` - Register a new user
- `POST /api/v1/token` - Get access token (login)
- `GET /api/v1/users/me` - Get current user details

### Posts

- `GET /api/v1/posts/` - List all posts (paginated)
- `POST /api/v1/posts/` - Create a new post (authenticated)
- `GET /api/v1/posts/{post_id}` - Get a specific post
- `PUT /api/v1/posts/{post_id}` - Update a post (authenticated, author only)
- `DELETE /api/v1/posts/{post_id}` - Delete a post (authenticated, author only)

### Comments

- `GET /api/v1/posts/{post_id}/comments/` - List all comments for a post (paginated)
- `POST /api/v1/posts/{post_id}/comments/` - Add a comment to a post (authenticated)
- `GET /api/v1/posts/{post_id}/comments/{comment_id}` - Get a specific comment
- `PUT /api/v1/posts/{post_id}/comments/{comment_id}` - Update a comment (authenticated, author only)
- `DELETE /api/v1/posts/{post_id}/comments/{comment_id}` - Delete a comment (authenticated, author only)

## Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT token generation
- `ALGORITHM` - Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time in minutes (default: 30)

## Testing with Postman

You can test the API using the provided Postman collection and environment files.

### Prerequisites
- [Postman](https://www.postman.com/downloads/) installed on your machine
- The API server running locally

### Importing the Collection and Environment

1. **Import the Collection**:
   - Open Postman
   - Click "Import" and select the `Blog_API.postman_collection.json` file
   - This will import all the API endpoints with example requests

2. **Import the Environment**:
   - In Postman, go to the "Environments" tab
   - Click "Import" and select the `Blog_API_Environment.postman_environment.json` file
   - Select the imported environment from the dropdown in the top-right corner

### Environment Variables

The environment includes these variables:
- `base_url`: Set to `http://localhost:8000` by default
- `auth_token`: Will be automatically set after login
- Test user credentials (username: `testuser`, password: `testpass123`)

### Testing Workflow

1. **Authentication**
   - Start with the "Register User" request to create a new account
   - Use the "Login" request to get an authentication token
   - The token will be automatically saved to the `auth_token` environment variable

2. **Testing Posts**
   - Use the "Create Post" request to add a new post
   - Test the "List Posts" endpoint to see all posts
   - Try updating and deleting posts (requires authentication)

3. **Testing Comments**
   - Use the "Create Comment" request to add a comment to a post
   - Test listing, updating, and deleting comments

### Running the Tests

1. Make sure your API server is running
2. In Postman, open the "Blog API" collection
3. Click the "Run" button next to the collection name
4. Select the environment and click "Run Blog API"
5. View the test results in the "Test Results" tab

