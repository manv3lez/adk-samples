#!/usr/bin/env python3
"""Database setup and management script."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from job_hunter_agent.database import create_schema, drop_schema, get_db_connection
from job_hunter_agent.database.migrations import MigrationManager, run_initial_migration


def setup_database() -> None:
    """Set up the database with schema and migrations."""
    print("Setting up database...")
    try:
        db = get_db_connection()
        print("✓ Database connection established")

        print("\nRunning migrations...")
        run_initial_migration(db)
        print("✓ Migrations complete")

        print("\n✓ Database setup complete!")
    except Exception as e:
        print(f"\n✗ Error setting up database: {e}")
        sys.exit(1)


def reset_database() -> None:
    """Reset the database (drop and recreate schema)."""
    print("WARNING: This will delete all data!")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() != "yes":
        print("Aborted.")
        return

    print("\nResetting database...")
    try:
        db = get_db_connection()

        print("Dropping existing schema...")
        drop_schema(db)
        print("✓ Schema dropped")

        print("\nCreating new schema...")
        create_schema(db)
        print("✓ Schema created")

        print("\nRunning migrations...")
        run_initial_migration(db)
        print("✓ Migrations complete")

        print("\n✓ Database reset complete!")
    except Exception as e:
        print(f"\n✗ Error resetting database: {e}")
        sys.exit(1)


def show_status() -> None:
    """Show database migration status."""
    try:
        db = get_db_connection()
        manager = MigrationManager(db)

        print("\nDatabase Migration Status")
        print("=" * 60)

        migrations = manager.get_applied_migrations()
        if not migrations:
            print("No migrations applied yet.")
        else:
            print(f"\nApplied migrations ({len(migrations)}):")
            for version, applied_at, description in migrations:
                print(f"\n  Version: {version}")
                print(f"  Applied: {applied_at}")
                print(f"  Description: {description}")

        print("\n" + "=" * 60)
    except Exception as e:
        print(f"\n✗ Error checking status: {e}")
        sys.exit(1)


def test_connection() -> None:
    """Test database connection."""
    print("Testing database connection...")
    try:
        db = get_db_connection()
        with db.get_cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"\n✓ Connection successful!")
            print(f"PostgreSQL version: {version[0]}")
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Database setup and management for Job Hunter Agent"
    )
    parser.add_argument(
        "command",
        choices=["setup", "reset", "status", "test"],
        help="Command to execute",
    )

    args = parser.parse_args()

    if args.command == "setup":
        setup_database()
    elif args.command == "reset":
        reset_database()
    elif args.command == "status":
        show_status()
    elif args.command == "test":
        test_connection()


if __name__ == "__main__":
    main()
