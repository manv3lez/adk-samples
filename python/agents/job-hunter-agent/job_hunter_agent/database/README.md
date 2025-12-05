# Database Module

This module provides PostgreSQL database utilities for the Job Hunter Agent, including connection pooling, schema management, and migrations.

## Setup

### 1. Install PostgreSQL

Make sure PostgreSQL 15+ is installed on your system.

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql-15
sudo systemctl start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE job_hunter;

# Exit psql
\q
```

### 3. Configure Environment Variables

Add the following to your `.env` file:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_hunter
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Run Migrations

```bash
# From the project root
python -m job_hunter_agent.database.migrations
```

Or check migration status:

```bash
python -m job_hunter_agent.database.migrations status
```

## Usage

### Connection Management

```python
from job_hunter_agent.database import get_db_connection

# Get global database connection
db = get_db_connection()

# Use connection with context manager
with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE email = %s", ("user@example.com",))
    user = cursor.fetchone()
```

### Schema Management

```python
from job_hunter_agent.database import create_schema, drop_schema

# Create all tables and indexes
create_schema()

# Drop all tables (WARNING: deletes all data!)
drop_schema()
```

### Migrations

```python
from job_hunter_agent.database.migrations import MigrationManager

manager = MigrationManager()

# Apply a custom migration
manager.apply_migration(
    version="003_add_custom_field",
    sql="ALTER TABLE users ADD COLUMN custom_field TEXT;",
    description="Add custom field to users table"
)

# Check if migration was applied
if manager.is_migration_applied("003_add_custom_field"):
    print("Migration already applied")

# Get all applied migrations
migrations = manager.get_applied_migrations()
for version, applied_at, description in migrations:
    print(f"{version}: {description} (applied {applied_at})")
```

## Database Schema

### Tables

- **users**: User authentication and account information
- **user_profiles**: Career profiles with background and goals
- **experiences**: Work experience entries
- **skills**: User skills with proficiency levels
- **education**: Educational background
- **conversations**: Chat history with specialists consulted
- **cached_analyses**: Cached analysis results with TTL
- **applications**: Job application tracking
- **resume_versions**: Multiple resume versions with response rates

### Indexes

All foreign keys and frequently queried fields are indexed for performance:
- User email lookups
- Profile and experience queries by user
- Conversation history by user and timestamp
- Application filtering by status and date
- Cache expiration queries

## Connection Pooling

The module uses `psycopg2.pool.SimpleConnectionPool` for efficient connection management:

- **Min connections**: 1 (configurable)
- **Max connections**: 10 (configurable)
- Connections are automatically returned to the pool after use
- Thread-safe connection management

## Error Handling

All database operations raise `ConnectionError` with descriptive messages:

```python
try:
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM users")
except ConnectionError as e:
    print(f"Database error: {e}")
```

## Testing

The database module includes utilities for testing:

```python
from job_hunter_agent.database import DatabaseConnection

# Create test database connection
test_db = DatabaseConnection(database="job_hunter_test")
test_db.initialize_pool()

# Run tests...

# Clean up
test_db.close_pool()
```

## Performance Optimization

### Connection Pooling
- Reuses connections instead of creating new ones
- Reduces connection overhead
- Configurable pool size based on load

### Indexes
- All foreign keys indexed
- Frequently queried fields indexed
- Composite indexes for common query patterns

### Best Practices
- Use parameterized queries to prevent SQL injection
- Use context managers for automatic connection cleanup
- Batch operations when possible
- Use JSONB for flexible schema fields

## Migration Strategy

Migrations are tracked in the `schema_migrations` table:

1. Each migration has a unique version identifier
2. Migrations are applied in order
3. Already-applied migrations are skipped
4. Migration history is preserved

To add a new migration:

```python
manager = MigrationManager()
manager.apply_migration(
    version="004_my_migration",
    sql="-- Your SQL here",
    description="Description of changes"
)
```
