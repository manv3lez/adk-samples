"""Database migration utilities."""

import os
from datetime import datetime
from typing import Optional

from job_hunter_agent.database.connection import DatabaseConnection


class MigrationManager:
    """Manages database migrations."""

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Initialize migration manager.

        Args:
            db_connection: Database connection instance. If None, uses global connection.
        """
        from job_hunter_agent.database.connection import get_db_connection

        self.db_connection = db_connection or get_db_connection()

    def create_migrations_table(self) -> None:
        """Create migrations tracking table if it doesn't exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            version VARCHAR(255) UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT
        );
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(sql)

    def is_migration_applied(self, version: str) -> bool:
        """
        Check if a migration has been applied.

        Args:
            version: Migration version identifier.

        Returns:
            True if migration has been applied, False otherwise.
        """
        sql = "SELECT COUNT(*) FROM schema_migrations WHERE version = %s;"
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(sql, (version,))
            result = cursor.fetchone()
            return result[0] > 0 if result else False

    def record_migration(self, version: str, description: str = "") -> None:
        """
        Record that a migration has been applied.

        Args:
            version: Migration version identifier.
            description: Optional description of the migration.
        """
        sql = """
        INSERT INTO schema_migrations (version, description)
        VALUES (%s, %s)
        ON CONFLICT (version) DO NOTHING;
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(sql, (version, description))

    def apply_migration(
        self, version: str, sql: str, description: str = ""
    ) -> None:
        """
        Apply a migration if it hasn't been applied yet.

        Args:
            version: Migration version identifier.
            sql: SQL statements to execute.
            description: Optional description of the migration.

        Raises:
            Exception: If migration fails.
        """
        self.create_migrations_table()

        if self.is_migration_applied(version):
            print(f"Migration {version} already applied, skipping.")
            return

        print(f"Applying migration {version}: {description}")
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(sql)

        self.record_migration(version, description)
        print(f"Migration {version} applied successfully.")

    def get_applied_migrations(self) -> list[tuple[str, datetime, str]]:
        """
        Get list of applied migrations.

        Returns:
            List of tuples (version, applied_at, description).
        """
        self.create_migrations_table()

        sql = """
        SELECT version, applied_at, description
        FROM schema_migrations
        ORDER BY applied_at;
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def run_initial_migration(db_connection: Optional[DatabaseConnection] = None) -> None:
    """
    Run the initial database migration.

    Args:
        db_connection: Database connection instance. If None, uses global connection.
    """
    from job_hunter_agent.database.schema import INDEXES_SQL, SCHEMA_SQL

    manager = MigrationManager(db_connection)

    # Apply initial schema
    manager.apply_migration(
        version="001_initial_schema",
        sql=SCHEMA_SQL,
        description="Create initial database schema with all tables",
    )

    # Apply indexes
    manager.apply_migration(
        version="002_create_indexes",
        sql=INDEXES_SQL,
        description="Create performance indexes on all tables",
    )


def main() -> None:
    """Run migrations from command line."""
    import sys

    from job_hunter_agent.database.connection import get_db_connection

    db = get_db_connection()

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Show migration status
        manager = MigrationManager(db)
        migrations = manager.get_applied_migrations()
        print("\nApplied migrations:")
        for version, applied_at, description in migrations:
            print(f"  {version} - {applied_at} - {description}")
    else:
        # Run migrations
        print("Running database migrations...")
        run_initial_migration(db)
        print("Migrations complete!")


if __name__ == "__main__":
    main()
