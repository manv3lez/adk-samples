# Database Setup Guide

This guide walks you through setting up PostgreSQL for the Job Hunter Agent Phase 2 flexible architecture.

## Prerequisites

- PostgreSQL 15 or higher
- Python 3.10 or higher
- Access to create databases

## Quick Start

### 1. Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql-15 postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
1. Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and follow prompts
3. Remember the password you set for the `postgres` user

### 2. Create Database

```bash
# Connect to PostgreSQL as postgres user
psql -U postgres

# Create the database
CREATE DATABASE job_hunter;

# Create a dedicated user (optional but recommended)
CREATE USER job_hunter_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE job_hunter TO job_hunter_user;

# Exit psql
\q
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update the database settings:

```bash
cp .env.example .env
```

Edit `.env` and set:

```bash
# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_hunter
DB_USER=job_hunter_user  # or postgres
DB_PASSWORD=your_secure_password
```

### 4. Install Dependencies

```bash
# Install psycopg2 (PostgreSQL adapter)
pip install psycopg2-binary

# Or if using uv
uv pip install psycopg2-binary
```

### 5. Run Database Setup

```bash
# Test connection
python scripts/db_setup.py test

# Set up schema and run migrations
python scripts/db_setup.py setup

# Check migration status
python scripts/db_setup.py status
```

## Database Schema

The database includes the following tables:

### Core Tables

1. **users** - User authentication and account information
   - `id` (UUID, primary key)
   - `email` (unique, indexed)
   - `password_hash` (bcrypt hashed)
   - `created_at`, `updated_at`, `last_login`

2. **user_profiles** - Career profiles with background and goals
   - `id` (UUID, primary key)
   - `user_id` (foreign key to users)
   - `background`, `career_goals` (text)
   - `target_roles`, `preferences` (JSONB)

3. **experiences** - Work experience entries
   - `id` (UUID, primary key)
   - `profile_id` (foreign key to user_profiles)
   - `role`, `company`, `start_date`, `end_date`
   - `responsibilities` (JSONB array)

4. **skills** - User skills with proficiency levels
   - `id` (UUID, primary key)
   - `profile_id` (foreign key to user_profiles)
   - `skill_name`, `proficiency`

5. **education** - Educational background
   - `id` (UUID, primary key)
   - `profile_id` (foreign key to user_profiles)
   - `degree`, `institution`, `graduation_year`

### Conversation & Analysis Tables

6. **conversations** - Chat history with specialists consulted
   - `id` (UUID, primary key)
   - `user_id` (foreign key to users)
   - `message`, `role` (user/assistant)
   - `specialists_consulted` (JSONB array)
   - `created_at` (indexed)

7. **cached_analyses** - Cached analysis results with TTL
   - `id` (UUID, primary key)
   - `user_id` (foreign key to users)
   - `analysis_type`, `analysis_data` (JSONB)
   - `created_at`, `expires_at` (indexed)

### Application Tracking Tables

8. **applications** - Job application tracking
   - `id` (UUID, primary key)
   - `user_id` (foreign key to users)
   - `company`, `role`, `status`
   - `applied_date` (indexed)
   - `resume_version`, `cover_letter`, `notes`

9. **resume_versions** - Multiple resume versions with response rates
   - `id` (UUID, primary key)
   - `user_id` (foreign key to users)
   - `version_name`, `content`, `target_role`
   - `response_rate` (calculated from applications)

## Performance Optimization

### Connection Pooling

The database module uses connection pooling for efficient resource management:

- **Min connections**: 1 (configurable)
- **Max connections**: 10 (configurable)
- Connections are reused across requests
- Automatic connection cleanup

### Indexes

All tables have appropriate indexes for common queries:

- Foreign keys (user_id, profile_id)
- Email lookups (users.email)
- Timestamp queries (conversations.created_at, applications.applied_date)
- Status filtering (applications.status)
- Cache expiration (cached_analyses.expires_at)

### JSONB Fields

JSONB is used for flexible schema fields:

- `target_roles` - Array of target job titles
- `preferences` - User preferences (location, remote, etc.)
- `responsibilities` - Array of job responsibilities
- `specialists_consulted` - Array of specialist names
- `analysis_data` - Cached analysis results

JSONB provides:
- Efficient storage and querying
- Schema flexibility
- Native PostgreSQL indexing support

## Usage Examples

### Python API

```python
from job_hunter_agent.database import get_db_connection

# Get database connection
db = get_db_connection()

# Execute query with context manager
with db.get_cursor() as cursor:
    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        ("user@example.com",)
    )
    user = cursor.fetchone()

# Insert data
with db.get_cursor() as cursor:
    cursor.execute(
        """
        INSERT INTO users (email, password_hash)
        VALUES (%s, %s)
        RETURNING id
        """,
        ("newuser@example.com", "hashed_password")
    )
    user_id = cursor.fetchone()[0]
```

### Schema Management

```python
from job_hunter_agent.database import create_schema, drop_schema

# Create all tables and indexes
create_schema()

# Reset database (WARNING: deletes all data!)
drop_schema()
create_schema()
```

### Migrations

```python
from job_hunter_agent.database.migrations import MigrationManager

manager = MigrationManager()

# Apply custom migration
manager.apply_migration(
    version="003_add_feature",
    sql="ALTER TABLE users ADD COLUMN feature_flag BOOLEAN DEFAULT FALSE;",
    description="Add feature flag to users"
)

# Check migration status
migrations = manager.get_applied_migrations()
for version, applied_at, description in migrations:
    print(f"{version}: {description}")
```

## Troubleshooting

### Connection Refused

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check PostgreSQL is running: `pg_isready`
2. Verify port: `sudo lsof -i :5432` (Unix) or `netstat -an | findstr 5432` (Windows)
3. Check `pg_hba.conf` allows local connections
4. Restart PostgreSQL: `brew services restart postgresql@15` (macOS)

### Authentication Failed

**Error:** `psycopg2.OperationalError: FATAL: password authentication failed`

**Solutions:**
1. Verify credentials in `.env` file
2. Reset password: `ALTER USER postgres WITH PASSWORD 'newpassword';`
3. Check `pg_hba.conf` authentication method (should be `md5` or `scram-sha-256`)

### Database Does Not Exist

**Error:** `psycopg2.OperationalError: FATAL: database "job_hunter" does not exist`

**Solution:**
```bash
psql -U postgres -c "CREATE DATABASE job_hunter;"
```

### Permission Denied

**Error:** `psycopg2.ProgrammingError: permission denied for table users`

**Solution:**
```bash
psql -U postgres -d job_hunter
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO job_hunter_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO job_hunter_user;
```

### Migration Already Applied

**Error:** Migration version already exists

**Solution:**
This is expected behavior. Migrations are idempotent and skip if already applied.

## Maintenance

### Backup Database

```bash
# Backup to file
pg_dump -U postgres job_hunter > backup.sql

# Backup with compression
pg_dump -U postgres job_hunter | gzip > backup.sql.gz
```

### Restore Database

```bash
# Restore from file
psql -U postgres job_hunter < backup.sql

# Restore from compressed file
gunzip -c backup.sql.gz | psql -U postgres job_hunter
```

### Reset Database

```bash
# Using script (interactive confirmation)
python scripts/db_setup.py reset

# Manual reset
psql -U postgres -c "DROP DATABASE job_hunter;"
psql -U postgres -c "CREATE DATABASE job_hunter;"
python scripts/db_setup.py setup
```

### View Database Size

```sql
SELECT pg_size_pretty(pg_database_size('job_hunter'));
```

### Vacuum and Analyze

```sql
-- Reclaim space and update statistics
VACUUM ANALYZE;

-- Full vacuum (requires exclusive lock)
VACUUM FULL;
```

## Security Best Practices

1. **Use Strong Passwords**: Generate secure passwords for database users
2. **Limit Connections**: Configure `max_connections` in `postgresql.conf`
3. **Enable SSL**: Use SSL/TLS for production connections
4. **Regular Backups**: Automate daily backups
5. **Monitor Access**: Review `pg_stat_activity` regularly
6. **Update PostgreSQL**: Keep PostgreSQL updated with security patches
7. **Restrict Network Access**: Use firewall rules to limit database access
8. **Use Connection Pooling**: Prevent connection exhaustion attacks

## Production Deployment

### Cloud SQL (Google Cloud)

```bash
# Create Cloud SQL instance
gcloud sql instances create job-hunter-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create job_hunter --instance=job-hunter-db

# Set password
gcloud sql users set-password postgres \
    --instance=job-hunter-db \
    --password=SECURE_PASSWORD
```

Update `.env`:
```bash
DB_HOST=/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME
DB_PORT=5432
DB_NAME=job_hunter
DB_USER=postgres
DB_PASSWORD=SECURE_PASSWORD
```

### AWS RDS

1. Create RDS PostgreSQL instance in AWS Console
2. Configure security groups for access
3. Update `.env` with RDS endpoint
4. Run migrations: `python scripts/db_setup.py setup`

### Docker

```dockerfile
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: job_hunter
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
docker-compose up -d
python scripts/db_setup.py setup
```

## Next Steps

After setting up the database:

1. ✅ Database is ready
2. ⏭️ Implement user authentication (Task 2)
3. ⏭️ Implement intent detection (Task 3)
4. ⏭️ Create Managing Coordinator (Task 5)

For more information, see:
- [Database Module README](job_hunter_agent/database/README.md)
- [Phase 2 Design Document](.kiro/specs/job-hunter-agent/phase2-flexible-design.md)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/15/)
