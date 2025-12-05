# Database Quick Start

## 5-Minute Setup

### 1. Install PostgreSQL
```bash
# macOS
brew install postgresql@15 && brew services start postgresql@15

# Ubuntu/Debian
sudo apt-get install postgresql-15 && sudo systemctl start postgresql
```

### 2. Create Database
```bash
psql -U postgres -c "CREATE DATABASE job_hunter;"
```

### 3. Configure
```bash
# Copy and edit .env
cp .env.example .env
# Set DB_PASSWORD in .env
```

### 4. Setup
```bash
python scripts/db_setup.py setup
```

## Quick Usage

### Get Connection
```python
from job_hunter_agent.database import get_db_connection

db = get_db_connection()
```

### Execute Query
```python
with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE email = %s", ("user@example.com",))
    user = cursor.fetchone()
```

### Insert Data
```python
with db.get_cursor() as cursor:
    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
        ("new@example.com", "hashed_password")
    )
    user_id = cursor.fetchone()[0]
```

## Common Commands

```bash
# Test connection
python scripts/db_setup.py test

# Check migrations
python scripts/db_setup.py status

# Reset database (WARNING: deletes all data!)
python scripts/db_setup.py reset
```

## Troubleshooting

**Connection refused?**
```bash
# Check if PostgreSQL is running
pg_isready
```

**Authentication failed?**
```bash
# Reset password
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'newpassword';"
```

**Database doesn't exist?**
```bash
psql -U postgres -c "CREATE DATABASE job_hunter;"
```

## Next Steps

- Read [DATABASE_SETUP.md](../../../DATABASE_SETUP.md) for detailed guide
- Read [README.md](README.md) for API documentation
- Implement user authentication (Task 2)
