"""Session storage for persistent session management (optional enhancement)."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from job_hunter_agent.database.connection import DatabaseConnection, get_db_connection


class SessionStorage:
    """
    Persistent session storage using PostgreSQL.

    This is an optional enhancement to store sessions in the database
    instead of in-memory. Useful for multi-server deployments.
    """

    def __init__(self, db_connection: Optional[DatabaseConnection] = None):
        """
        Initialize session storage.

        Args:
            db_connection: Database connection instance. If None, uses global connection.
        """
        self.db_connection = db_connection or get_db_connection()

    def create_session_table(self) -> None:
        """Create sessions table if it doesn't exist."""
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token VARCHAR(255) PRIMARY KEY,
                    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
                """
            )

    def store_session(
        self, token: str, user_id: UUID, expires_at: datetime
    ) -> None:
        """
        Store session token in database.

        Args:
            token: Session token string.
            user_id: User ID associated with the session.
            expires_at: Expiration timestamp.
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sessions (token, user_id, expires_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (token) DO UPDATE
                SET expires_at = EXCLUDED.expires_at
                """,
                (token, str(user_id), expires_at),
            )

    def get_session(self, token: str) -> Optional[tuple[UUID, datetime]]:
        """
        Retrieve session from database.

        Args:
            token: Session token string.

        Returns:
            Tuple of (user_id, expires_at) if session exists and is valid, None otherwise.
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT user_id, expires_at
                FROM sessions
                WHERE token = %s
                AND expires_at > CURRENT_TIMESTAMP
                """,
                (token,),
            )
            result = cursor.fetchone()

            if result is None:
                return None

            user_id, expires_at = result
            return (
                UUID(user_id) if isinstance(user_id, str) else user_id,
                expires_at,
            )

    def delete_session(self, token: str) -> None:
        """
        Delete session from database (logout).

        Args:
            token: Session token string to delete.
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM sessions
                WHERE token = %s
                """,
                (token,),
            )

    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions from database.

        Returns:
            Number of sessions deleted.
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM sessions
                WHERE expires_at <= CURRENT_TIMESTAMP
                """
            )
            return cursor.rowcount
