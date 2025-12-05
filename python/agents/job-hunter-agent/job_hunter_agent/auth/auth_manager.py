"""Authentication manager with bcrypt password hashing and session management."""

import secrets
from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import UUID

import bcrypt
from pydantic import BaseModel, EmailStr

from job_hunter_agent.database.connection import DatabaseConnection, get_db_connection


class SessionToken(BaseModel):
    """Session token model."""

    token: str
    user_id: UUID
    created_at: datetime
    expires_at: datetime


class UserContext(BaseModel):
    """User context loaded from database."""

    user_id: UUID
    email: str
    profile: Optional[dict[str, Any]] = None
    conversation_history: list[dict[str, Any]] = []
    cached_analyses: dict[str, Any] = {}
    last_login: Optional[datetime] = None


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class AuthManager:
    """Manages user authentication and session tokens."""

    def __init__(
        self,
        db_connection: Optional[DatabaseConnection] = None,
        token_expiry_hours: int = 24,
    ):
        """
        Initialize authentication manager.

        Args:
            db_connection: Database connection instance. If None, uses global connection.
            token_expiry_hours: Number of hours before session tokens expire.
        """
        self.db_connection = db_connection or get_db_connection()
        self.token_expiry_hours = token_expiry_hours
        self._session_tokens: dict[str, SessionToken] = {}

    def register_user(self, email: str, password: str) -> UUID:
        """
        Register a new user with bcrypt password hashing.

        Args:
            email: User email address.
            password: Plain text password.

        Returns:
            UUID of the created user.

        Raises:
            ValueError: If email is already registered or password is too weak.
            ConnectionError: If database connection fails.
        """
        # Validate email format
        try:
            EmailStr._validate(email)
        except Exception as e:
            raise ValueError(f"Invalid email format: {email}") from e

        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert user into database
        with self.db_connection.get_cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, created_at, updated_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    RETURNING id
                    """,
                    (email, password_hash.decode("utf-8")),
                )
                result = cursor.fetchone()
                if result is None:
                    raise ValueError("Failed to create user")
                user_id = result[0]
                return UUID(user_id) if isinstance(user_id, str) else user_id
            except Exception as e:
                if "unique constraint" in str(e).lower():
                    raise ValueError(f"Email already registered: {email}") from e
                raise

    def authenticate_user(self, email: str, password: str) -> UUID:
        """
        Authenticate user with email and password.

        Args:
            email: User email address.
            password: Plain text password.

        Returns:
            UUID of the authenticated user.

        Raises:
            AuthenticationError: If credentials are invalid.
            ConnectionError: If database connection fails.
        """
        with self.db_connection.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, password_hash
                FROM users
                WHERE email = %s
                """,
                (email,),
            )
            result = cursor.fetchone()

            if result is None:
                raise AuthenticationError("Invalid email or password")

            user_id, password_hash = result

            # Verify password using bcrypt
            if not bcrypt.checkpw(
                password.encode("utf-8"), password_hash.encode("utf-8")
            ):
                raise AuthenticationError("Invalid email or password")

            # Update last login timestamp
            cursor.execute(
                """
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (user_id,),
            )

            return UUID(user_id) if isinstance(user_id, str) else user_id

    def create_session_token(self, user_id: UUID) -> SessionToken:
        """
        Create a new session token for authenticated user.

        Args:
            user_id: UUID of the authenticated user.

        Returns:
            SessionToken object with token string and expiry.
        """
        # Generate secure random token
        token = secrets.token_urlsafe(32)

        # Calculate expiry time
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(hours=self.token_expiry_hours)

        # Create session token object
        session_token = SessionToken(
            token=token,
            user_id=user_id,
            created_at=created_at,
            expires_at=expires_at,
        )

        # Store in memory (in production, use Redis or database)
        self._session_tokens[token] = session_token

        return session_token

    def validate_session_token(self, token: str) -> Optional[UUID]:
        """
        Validate session token and return user ID if valid.

        Args:
            token: Session token string.

        Returns:
            User ID if token is valid, None otherwise.
        """
        session_token = self._session_tokens.get(token)

        if session_token is None:
            return None

        # Check if token has expired
        if datetime.utcnow() > session_token.expires_at:
            # Remove expired token
            del self._session_tokens[token]
            return None

        return session_token.user_id

    def invalidate_session_token(self, token: str) -> None:
        """
        Invalidate (logout) a session token.

        Args:
            token: Session token string to invalidate.
        """
        if token in self._session_tokens:
            del self._session_tokens[token]

    def get_user_context(self, user_id: UUID) -> UserContext:
        """
        Load complete user context from database.

        Args:
            user_id: UUID of the user.

        Returns:
            UserContext object with profile, conversation history, and cached analyses.

        Raises:
            ValueError: If user not found.
            ConnectionError: If database connection fails.
        """
        with self.db_connection.get_cursor() as cursor:
            # Load user basic info
            cursor.execute(
                """
                SELECT email, last_login
                FROM users
                WHERE id = %s
                """,
                (str(user_id),),
            )
            user_result = cursor.fetchone()

            if user_result is None:
                raise ValueError(f"User not found: {user_id}")

            email, last_login = user_result

            # Load user profile
            cursor.execute(
                """
                SELECT background, career_goals, target_roles, preferences
                FROM user_profiles
                WHERE user_id = %s
                """,
                (str(user_id),),
            )
            profile_result = cursor.fetchone()

            profile = None
            if profile_result:
                background, career_goals, target_roles, preferences = profile_result
                profile = {
                    "background": background,
                    "career_goals": career_goals,
                    "target_roles": target_roles,
                    "preferences": preferences,
                }

            # Load recent conversation history (last 50 messages)
            cursor.execute(
                """
                SELECT message, role, specialists_consulted, created_at
                FROM conversations
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 50
                """,
                (str(user_id),),
            )
            conversation_results = cursor.fetchall()

            conversation_history = [
                {
                    "message": msg,
                    "role": role,
                    "specialists_consulted": specialists,
                    "created_at": created_at.isoformat() if created_at else None,
                }
                for msg, role, specialists, created_at in reversed(conversation_results)
            ]

            # Load cached analyses
            cursor.execute(
                """
                SELECT analysis_type, analysis_data
                FROM cached_analyses
                WHERE user_id = %s
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                """,
                (str(user_id),),
            )
            cache_results = cursor.fetchall()

            cached_analyses = {
                analysis_type: analysis_data
                for analysis_type, analysis_data in cache_results
            }

            return UserContext(
                user_id=user_id,
                email=email,
                profile=profile,
                conversation_history=conversation_history,
                cached_analyses=cached_analyses,
                last_login=last_login,
            )


# Global authentication manager instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """
    Get the global authentication manager instance.

    Returns:
        The global AuthManager instance.
    """
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


# Convenience functions for common operations
def register_user(email: str, password: str) -> UUID:
    """Register a new user."""
    return get_auth_manager().register_user(email, password)


def authenticate_user(email: str, password: str) -> UUID:
    """Authenticate user and return user ID."""
    return get_auth_manager().authenticate_user(email, password)


def create_session_token(user_id: UUID) -> SessionToken:
    """Create session token for user."""
    return get_auth_manager().create_session_token(user_id)


def validate_session_token(token: str) -> Optional[UUID]:
    """Validate session token and return user ID."""
    return get_auth_manager().validate_session_token(token)


def get_user_context(user_id: UUID) -> UserContext:
    """Load user context from database."""
    return get_auth_manager().get_user_context(user_id)
