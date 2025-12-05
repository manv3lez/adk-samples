"""Tests for authentication and session management."""

import pytest
from uuid import UUID

from job_hunter_agent.auth import (
    AuthenticationError,
    AuthManager,
    authenticate_user,
    create_session_token,
    get_user_context,
    register_user,
    validate_session_token,
)
from job_hunter_agent.database.connection import DatabaseConnection
from job_hunter_agent.database.schema import create_schema, drop_schema


@pytest.fixture
def test_db():
    """Create a test database connection and schema."""
    # Use test database
    db = DatabaseConnection(
        database="job_hunter_test",
        host="localhost",
        user="postgres",
        password="",
    )
    db.initialize_pool()

    # Create schema
    try:
        create_schema(db)
    except Exception:
        # Schema might already exist
        pass

    yield db

    # Cleanup
    try:
        drop_schema(db)
    except Exception:
        pass
    db.close_pool()


@pytest.fixture
def auth_manager(test_db):
    """Create an AuthManager instance for testing."""
    return AuthManager(db_connection=test_db, token_expiry_hours=1)


class TestUserRegistration:
    """Tests for user registration."""

    def test_register_user_success(self, auth_manager):
        """Test successful user registration."""
        email = "test@example.com"
        password = "SecurePassword123!"

        user_id = auth_manager.register_user(email, password)

        assert isinstance(user_id, UUID)
        assert user_id is not None

    def test_register_user_invalid_email(self, auth_manager):
        """Test registration with invalid email format."""
        with pytest.raises(ValueError, match="Invalid email format"):
            auth_manager.register_user("not-an-email", "Password123!")

    def test_register_user_weak_password(self, auth_manager):
        """Test registration with weak password."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            auth_manager.register_user("test@example.com", "weak")

    def test_register_user_duplicate_email(self, auth_manager):
        """Test registration with duplicate email."""
        email = "duplicate@example.com"
        password = "Password123!"

        # First registration should succeed
        auth_manager.register_user(email, password)

        # Second registration should fail
        with pytest.raises(ValueError, match="already registered"):
            auth_manager.register_user(email, password)


class TestUserAuthentication:
    """Tests for user authentication."""

    def test_authenticate_user_success(self, auth_manager):
        """Test successful user authentication."""
        email = "auth@example.com"
        password = "AuthPassword123!"

        # Register user first
        registered_user_id = auth_manager.register_user(email, password)

        # Authenticate
        authenticated_user_id = auth_manager.authenticate_user(email, password)

        assert authenticated_user_id == registered_user_id

    def test_authenticate_user_wrong_password(self, auth_manager):
        """Test authentication with wrong password."""
        email = "wrong@example.com"
        password = "CorrectPassword123!"

        # Register user
        auth_manager.register_user(email, password)

        # Try to authenticate with wrong password
        with pytest.raises(AuthenticationError, match="Invalid email or password"):
            auth_manager.authenticate_user(email, "WrongPassword123!")

    def test_authenticate_user_nonexistent_email(self, auth_manager):
        """Test authentication with non-existent email."""
        with pytest.raises(AuthenticationError, match="Invalid email or password"):
            auth_manager.authenticate_user("nonexistent@example.com", "Password123!")


class TestSessionManagement:
    """Tests for session token management."""

    def test_create_session_token(self, auth_manager):
        """Test session token creation."""
        email = "session@example.com"
        password = "SessionPassword123!"

        # Register and authenticate user
        user_id = auth_manager.register_user(email, password)

        # Create session token
        session_token = auth_manager.create_session_token(user_id)

        assert session_token.token is not None
        assert len(session_token.token) > 0
        assert session_token.user_id == user_id
        assert session_token.expires_at > session_token.created_at

    def test_validate_session_token_success(self, auth_manager):
        """Test successful session token validation."""
        email = "validate@example.com"
        password = "ValidatePassword123!"

        # Register user and create session
        user_id = auth_manager.register_user(email, password)
        session_token = auth_manager.create_session_token(user_id)

        # Validate token
        validated_user_id = auth_manager.validate_session_token(session_token.token)

        assert validated_user_id == user_id

    def test_validate_session_token_invalid(self, auth_manager):
        """Test validation of invalid session token."""
        result = auth_manager.validate_session_token("invalid-token-12345")

        assert result is None

    def test_invalidate_session_token(self, auth_manager):
        """Test session token invalidation (logout)."""
        email = "logout@example.com"
        password = "LogoutPassword123!"

        # Register user and create session
        user_id = auth_manager.register_user(email, password)
        session_token = auth_manager.create_session_token(user_id)

        # Validate token (should work)
        assert auth_manager.validate_session_token(session_token.token) == user_id

        # Invalidate token
        auth_manager.invalidate_session_token(session_token.token)

        # Validate token again (should fail)
        assert auth_manager.validate_session_token(session_token.token) is None


class TestUserContext:
    """Tests for user context loading."""

    def test_get_user_context_basic(self, auth_manager):
        """Test loading basic user context."""
        email = "context@example.com"
        password = "ContextPassword123!"

        # Register user
        user_id = auth_manager.register_user(email, password)

        # Load user context
        user_context = auth_manager.get_user_context(user_id)

        assert user_context.user_id == user_id
        assert user_context.email == email
        assert user_context.profile is None  # No profile created yet
        assert user_context.conversation_history == []
        assert user_context.cached_analyses == {}

    def test_get_user_context_nonexistent_user(self, auth_manager):
        """Test loading context for non-existent user."""
        from uuid import uuid4

        fake_user_id = uuid4()

        with pytest.raises(ValueError, match="User not found"):
            auth_manager.get_user_context(fake_user_id)


class TestPasswordSecurity:
    """Tests for password security features."""

    def test_password_hashed_not_plaintext(self, auth_manager):
        """Test that passwords are hashed, not stored in plaintext."""
        email = "security@example.com"
        password = "PlaintextTest123!"

        # Register user
        user_id = auth_manager.register_user(email, password)

        # Query database directly to check password storage
        with auth_manager.db_connection.get_cursor() as cursor:
            cursor.execute(
                "SELECT password_hash FROM users WHERE id = %s", (str(user_id),)
            )
            result = cursor.fetchone()
            password_hash = result[0]

            # Password hash should not equal plaintext password
            assert password_hash != password

            # Password hash should start with bcrypt prefix
            assert password_hash.startswith("$2b$")

    def test_same_password_different_hashes(self, auth_manager):
        """Test that same password produces different hashes (salt)."""
        password = "SamePassword123!"

        # Register two users with same password
        user_id_1 = auth_manager.register_user("user1@example.com", password)
        user_id_2 = auth_manager.register_user("user2@example.com", password)

        # Get password hashes
        with auth_manager.db_connection.get_cursor() as cursor:
            cursor.execute(
                "SELECT password_hash FROM users WHERE id IN (%s, %s)",
                (str(user_id_1), str(user_id_2)),
            )
            results = cursor.fetchall()
            hash_1 = results[0][0]
            hash_2 = results[1][0]

            # Hashes should be different due to different salts
            assert hash_1 != hash_2


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_convenience_register_user(self, test_db):
        """Test convenience register_user function."""
        # Note: This uses the global auth manager
        email = "convenience@example.com"
        password = "ConveniencePassword123!"

        user_id = register_user(email, password)

        assert isinstance(user_id, UUID)

    def test_convenience_authenticate_user(self, test_db):
        """Test convenience authenticate_user function."""
        email = "convenience2@example.com"
        password = "ConveniencePassword123!"

        # Register first
        registered_id = register_user(email, password)

        # Authenticate
        authenticated_id = authenticate_user(email, password)

        assert authenticated_id == registered_id

    def test_convenience_session_flow(self, test_db):
        """Test complete flow with convenience functions."""
        email = "flow@example.com"
        password = "FlowPassword123!"

        # Register
        user_id = register_user(email, password)

        # Create session
        session_token = create_session_token(user_id)

        # Validate session
        validated_id = validate_session_token(session_token.token)
        assert validated_id == user_id

        # Load context
        user_context = get_user_context(user_id)
        assert user_context.email == email


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
