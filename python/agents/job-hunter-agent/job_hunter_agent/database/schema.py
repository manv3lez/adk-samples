"""Database schema definitions and migration utilities."""

from typing import Optional

from job_hunter_agent.database.connection import DatabaseConnection


# SQL schema definitions
SCHEMA_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- User profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    background TEXT,
    career_goals TEXT,
    target_roles JSONB,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Experience table
CREATE TABLE IF NOT EXISTS experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    role VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    responsibilities JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills table
CREATE TABLE IF NOT EXISTS skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    skill_name VARCHAR(255) NOT NULL,
    proficiency VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Education table
CREATE TABLE IF NOT EXISTS education (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    degree VARCHAR(255) NOT NULL,
    institution VARCHAR(255) NOT NULL,
    graduation_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    specialists_consulted JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cached analyses table
CREATE TABLE IF NOT EXISTS cached_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL,
    analysis_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(user_id, analysis_type)
);

-- Applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    company VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    applied_date DATE NOT NULL,
    resume_version TEXT,
    cover_letter TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resume versions table
CREATE TABLE IF NOT EXISTS resume_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    version_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    target_role VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_rate FLOAT DEFAULT 0.0
);
"""

# Index creation SQL
INDEXES_SQL = """
-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- User profiles indexes
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON user_profiles(user_id);

-- Experience indexes
CREATE INDEX IF NOT EXISTS idx_experiences_profile_id ON experiences(profile_id);

-- Skills indexes
CREATE INDEX IF NOT EXISTS idx_skills_profile_id ON skills(profile_id);

-- Education indexes
CREATE INDEX IF NOT EXISTS idx_education_profile_id ON education(profile_id);

-- Conversations indexes
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);

-- Cached analyses indexes
CREATE INDEX IF NOT EXISTS idx_cached_analyses_user_id ON cached_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_cached_analyses_expires_at ON cached_analyses(expires_at);

-- Applications indexes
CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_applied_date ON applications(applied_date DESC);

-- Resume versions indexes
CREATE INDEX IF NOT EXISTS idx_resume_versions_user_id ON resume_versions(user_id);
"""

# Drop schema SQL
DROP_SCHEMA_SQL = """
DROP TABLE IF EXISTS resume_versions CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS cached_analyses CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS education CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;
"""


def create_schema(db_connection: Optional[DatabaseConnection] = None) -> None:
    """
    Create database schema with all tables and indexes.

    Args:
        db_connection: Database connection instance. If None, uses global connection.

    Raises:
        ConnectionError: If database connection fails.
        Exception: If schema creation fails.
    """
    from job_hunter_agent.database.connection import get_db_connection

    if db_connection is None:
        db_connection = get_db_connection()

    with db_connection.get_cursor() as cursor:
        # Create tables
        cursor.execute(SCHEMA_SQL)

        # Create indexes
        cursor.execute(INDEXES_SQL)


def drop_schema(db_connection: Optional[DatabaseConnection] = None) -> None:
    """
    Drop all database tables.

    WARNING: This will delete all data!

    Args:
        db_connection: Database connection instance. If None, uses global connection.

    Raises:
        ConnectionError: If database connection fails.
        Exception: If schema drop fails.
    """
    from job_hunter_agent.database.connection import get_db_connection

    if db_connection is None:
        db_connection = get_db_connection()

    with db_connection.get_cursor() as cursor:
        cursor.execute(DROP_SCHEMA_SQL)
