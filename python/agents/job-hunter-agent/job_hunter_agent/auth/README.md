# Authentication and Session Management

This module provides secure user authentication and session management for the Job Hunter Agent.

## Features

- **User Registration**: Create new user accounts with email and password
- **Password Security**: Bcrypt hashing for secure password storage
- **User Authentication**: Login with email and password
- **Session Management**: Token-based session management with expiration
- **User Context Loading**: Load complete user profile, conversation history, and cached analyses
- **Logout**: Invalidate session tokens

## Quick Start

### 1. Register a New User

```python
from job_hunter_agent.auth import register_user

user_id = register_user(
    email="user@example.com",
    password="SecurePassword123!"
)
print(f"User registered with ID: {user_id}")
```

### 2. Authenticate User (Login)

```python
from job_hunter_agent.auth import authenticate_user, create_session_token

# Authenticate user
user_id = authenticate_user(
    email="user@example.com",
    password="SecurePassword123!"
)

# Create session token
session_token = create_session_token(user_id)
print(f"Session token: {session_token.token}")
print(f"Expires at: {session_token.expires_at}")
```

### 3. Validate Session Token

```python
from job_hunter_agent.auth import validate_session_token

# Validate token (e.g., on subsequent requests)
user_id = validate_session_token(token_string)
if user_id:
    print(f"Valid session for user: {user_id}")
else:
    print("Invalid or expired session")
```

### 4. Load User Context

```python
from job_hunter_agent.auth import get_user_context

# Load complete user context
user_context = get_user_context(user_id)

print(f"Email: {user_context.email}")
print(f"Profile: {user_context.profile}")
print(f"Conversation history: {len(user_context.conversation_history)} messages")
print(f"Cached analyses: {user_context.cached_analyses}")
```

### 5. Logout

```python
from job_hunter_agent.auth import get_auth_manager

# Invalidate session token
auth_manager = get_auth_manager()
auth_manager.invalidate_session_token(token_string)
```

## API Reference

### `register_user(email: str, password: str) -> UUID`

Register a new user with email and password.

**Parameters:**
- `email`: User email address (must be valid email format)
- `password`: Plain text password (minimum 8 characters)

**Returns:**
- UUID of the created user

**Raises:**
- `ValueError`: If email is invalid, password is too weak, or email already exists

### `authenticate_user(email: str, password: str) -> UUID`

Authenticate user with email and password.

**Parameters:**
- `email`: User email address
- `password`: Plain text password

**Returns:**
- UUID of the authenticated user

**Raises:**
- `AuthenticationError`: If credentials are invalid

### `create_session_token(user_id: UUID) -> SessionToken`

Create a session token for authenticated user.

**Parameters:**
- `user_id`: UUID of the authenticated user

**Returns:**
- `SessionToken` object with token string, user_id, created_at, and expires_at

### `validate_session_token(token: str) -> Optional[UUID]`

Validate session token and return user ID if valid.

**Parameters:**
- `token`: Session token string

**Returns:**
- User ID if token is valid, None if invalid or expired

### `get_user_context(user_id: UUID) -> UserContext`

Load complete user context from database.

**Parameters:**
- `user_id`: UUID of the user

**Returns:**
- `UserContext` object with:
  - `user_id`: User UUID
  - `email`: User email
  - `profile`: User profile data (dict)
  - `conversation_history`: List of conversation messages
  - `cached_analyses`: Dictionary of cached analysis results
  - `last_login`: Last login timestamp

**Raises:**
- `ValueError`: If user not found

## Data Models

### SessionToken

```python
class SessionToken(BaseModel):
    token: str              # Secure random token
    user_id: UUID           # User ID
    created_at: datetime    # Creation timestamp
    expires_at: datetime    # Expiration timestamp
```

### UserContext

```python
class UserContext(BaseModel):
    user_id: UUID                           # User ID
    email: str                              # User email
    profile: Optional[dict[str, Any]]       # User profile data
    conversation_history: list[dict]        # Conversation messages
    cached_analyses: dict[str, Any]         # Cached analysis results
    last_login: Optional[datetime]          # Last login timestamp
```

## Security Features

### Password Hashing

Passwords are hashed using bcrypt with automatic salt generation:

```python
# Password is hashed before storage
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Password verification during login
bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
```

### Session Token Generation

Session tokens are generated using cryptographically secure random bytes:

```python
token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits of entropy
```

### Token Expiration

Session tokens expire after 24 hours by default (configurable):

```python
auth_manager = AuthManager(token_expiry_hours=48)  # 48-hour sessions
```

## Error Handling

### Registration Errors

```python
try:
    user_id = register_user(email, password)
except ValueError as e:
    # Handle validation errors:
    # - Invalid email format
    # - Password too weak (< 8 characters)
    # - Email already registered
    print(f"Registration failed: {e}")
```

### Authentication Errors

```python
try:
    user_id = authenticate_user(email, password)
except AuthenticationError as e:
    # Handle authentication failure:
    # - Invalid email
    # - Wrong password
    print(f"Login failed: {e}")
```

## Advanced Usage

### Custom Authentication Manager

```python
from job_hunter_agent.auth import AuthManager
from job_hunter_agent.database import DatabaseConnection

# Create custom auth manager with custom settings
db_connection = DatabaseConnection(host="custom-host")
auth_manager = AuthManager(
    db_connection=db_connection,
    token_expiry_hours=48  # 48-hour sessions
)

# Use custom manager
user_id = auth_manager.register_user(email, password)
session_token = auth_manager.create_session_token(user_id)
```

### Persistent Session Storage (Optional)

For multi-server deployments, use persistent session storage:

```python
from job_hunter_agent.auth.session_storage import SessionStorage

# Create sessions table
session_storage = SessionStorage()
session_storage.create_session_table()

# Store session in database
session_storage.store_session(
    token=session_token.token,
    user_id=user_id,
    expires_at=session_token.expires_at
)

# Retrieve session from database
result = session_storage.get_session(token)
if result:
    user_id, expires_at = result
    print(f"Session valid for user: {user_id}")
```

## Examples

See `auth_example.py` for complete working examples:

```bash
cd python/agents/job-hunter-agent
python -m job_hunter_agent.auth.auth_example
```

## Requirements

- PostgreSQL database with schema created (see `database/README.md`)
- bcrypt library for password hashing
- pydantic for data validation

## Database Schema

The authentication system uses the following tables:

```sql
-- Users table (created by database/schema.py)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Optional: Sessions table for persistent storage
CREATE TABLE sessions (
    token VARCHAR(255) PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
```

## Best Practices

1. **Never store plain text passwords**: Always use bcrypt hashing
2. **Use HTTPS**: Transmit session tokens over secure connections only
3. **Validate tokens on every request**: Check token validity before processing
4. **Set appropriate expiration**: Balance security and user experience
5. **Handle errors gracefully**: Provide clear error messages without leaking security info
6. **Clean up expired sessions**: Periodically remove expired tokens
7. **Use strong passwords**: Enforce minimum password requirements

## Testing

Run tests for the authentication module:

```bash
pytest tests/test_auth.py -v
```

## Contributing

When adding new authentication features:

1. Follow existing patterns for error handling
2. Add comprehensive docstrings
3. Include examples in this README
4. Write unit tests for new functionality
5. Update the examples file if needed
