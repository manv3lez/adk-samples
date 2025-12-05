"""Database connection utilities with connection pooling."""

import os
from contextlib import contextmanager
from typing import Generator, Optional

import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection as Connection


class DatabaseConnection:
    """Manages PostgreSQL database connections with connection pooling."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        min_connections: int = 1,
        max_connections: int = 10,
    ):
        """
        Initialize database connection pool.

        Args:
            host: Database host (defaults to env var DB_HOST or 'localhost')
            port: Database port (defaults to env var DB_PORT or 5432)
            database: Database name (defaults to env var DB_NAME or 'job_hunter')
            user: Database user (defaults to env var DB_USER or 'postgres')
            password: Database password (defaults to env var DB_PASSWORD)
            min_connections: Minimum number of connections in pool
            max_connections: Maximum number of connections in pool
        """
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = port or int(os.getenv("DB_PORT", "5432"))
        self.database = database or os.getenv("DB_NAME", "job_hunter")
        self.user = user or os.getenv("DB_USER", "postgres")
        self.password = password or os.getenv("DB_PASSWORD", "")

        self._pool: Optional[pool.SimpleConnectionPool] = None
        self.min_connections = min_connections
        self.max_connections = max_connections

    def initialize_pool(self) -> None:
        """Initialize the connection pool."""
        if self._pool is not None:
            return

        try:
            self._pool = psycopg2.pool.SimpleConnectionPool(
                self.min_connections,
                self.max_connections,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
        except psycopg2.Error as e:
            raise ConnectionError(f"Failed to initialize database pool: {e}") from e

    def close_pool(self) -> None:
        """Close all connections in the pool."""
        if self._pool is not None:
            self._pool.closeall()
            self._pool = None

    @contextmanager
    def get_connection(self) -> Generator[Connection, None, None]:
        """
        Get a connection from the pool.

        Yields:
            A database connection from the pool.

        Raises:
            ConnectionError: If pool is not initialized or connection fails.
        """
        if self._pool is None:
            self.initialize_pool()

        conn = None
        try:
            conn = self._pool.getconn()  # type: ignore
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise ConnectionError(f"Database connection error: {e}") from e
        finally:
            if conn:
                self._pool.putconn(conn)  # type: ignore

    @contextmanager
    def get_cursor(self) -> Generator:
        """
        Get a cursor from a pooled connection.

        Yields:
            A database cursor.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()


# Global database connection instance
_db_connection: Optional[DatabaseConnection] = None


def get_db_connection() -> DatabaseConnection:
    """
    Get the global database connection instance.

    Returns:
        The global DatabaseConnection instance.
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
        _db_connection.initialize_pool()
    return _db_connection
