"""Example usage of authentication and session management."""

from job_hunter_agent.auth import (
    AuthenticationError,
    authenticate_user,
    create_session_token,
    get_user_context,
    register_user,
    validate_session_token,
)


def example_registration_and_login() -> None:
    """Example: Register a new user and login."""
    print("=== User Registration Example ===")

    # Register a new user
    try:
        user_id = register_user(
            email="john.doe@example.com", password="SecurePassword123!"
        )
        print(f"✓ User registered successfully with ID: {user_id}")
    except ValueError as e:
        print(f"✗ Registration failed: {e}")
        return

    print("\n=== User Login Example ===")

    # Authenticate user
    try:
        authenticated_user_id = authenticate_user(
            email="john.doe@example.com", password="SecurePassword123!"
        )
        print(f"✓ User authenticated successfully: {authenticated_user_id}")
    except AuthenticationError as e:
        print(f"✗ Authentication failed: {e}")
        return

    # Create session token
    session_token = create_session_token(authenticated_user_id)
    print(f"✓ Session token created: {session_token.token[:20]}...")
    print(f"  Expires at: {session_token.expires_at}")


def example_session_validation() -> None:
    """Example: Validate session token and load user context."""
    print("\n=== Session Validation Example ===")

    # First, create a session (normally done during login)
    user_id = register_user(
        email="jane.smith@example.com", password="AnotherSecure123!"
    )
    session_token = create_session_token(user_id)
    token_string = session_token.token

    print(f"Session token: {token_string[:20]}...")

    # Validate the token
    validated_user_id = validate_session_token(token_string)
    if validated_user_id:
        print(f"✓ Token is valid for user: {validated_user_id}")

        # Load user context
        user_context = get_user_context(validated_user_id)
        print(f"✓ User context loaded:")
        print(f"  Email: {user_context.email}")
        print(f"  Profile: {user_context.profile}")
        print(f"  Conversation history: {len(user_context.conversation_history)} messages")
        print(f"  Cached analyses: {len(user_context.cached_analyses)} items")
    else:
        print("✗ Token is invalid or expired")


def example_authentication_flow() -> None:
    """Example: Complete authentication flow."""
    print("\n=== Complete Authentication Flow ===")

    email = "user@example.com"
    password = "MyPassword123!"

    # Step 1: Register
    print(f"1. Registering user: {email}")
    try:
        user_id = register_user(email, password)
        print(f"   ✓ Registered with ID: {user_id}")
    except ValueError as e:
        print(f"   ✗ Registration failed: {e}")
        # User might already exist, try to login
        print("   Attempting to login instead...")

    # Step 2: Login
    print(f"2. Logging in user: {email}")
    try:
        user_id = authenticate_user(email, password)
        print(f"   ✓ Authenticated with ID: {user_id}")
    except AuthenticationError as e:
        print(f"   ✗ Login failed: {e}")
        return

    # Step 3: Create session
    print("3. Creating session token")
    session_token = create_session_token(user_id)
    print(f"   ✓ Token: {session_token.token[:20]}...")

    # Step 4: Validate session (simulating subsequent request)
    print("4. Validating session token")
    validated_user_id = validate_session_token(session_token.token)
    if validated_user_id:
        print(f"   ✓ Session valid for user: {validated_user_id}")
    else:
        print("   ✗ Session invalid")
        return

    # Step 5: Load user context
    print("5. Loading user context")
    user_context = get_user_context(validated_user_id)
    print(f"   ✓ Context loaded for: {user_context.email}")
    print(f"   Last login: {user_context.last_login}")


def example_error_handling() -> None:
    """Example: Error handling in authentication."""
    print("\n=== Error Handling Examples ===")

    # Invalid email format
    print("1. Testing invalid email format")
    try:
        register_user(email="not-an-email", password="Password123!")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")

    # Weak password
    print("2. Testing weak password")
    try:
        register_user(email="test@example.com", password="weak")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")

    # Duplicate email
    print("3. Testing duplicate email")
    try:
        register_user(email="duplicate@example.com", password="Password123!")
        register_user(email="duplicate@example.com", password="Password123!")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Caught error: {e}")

    # Wrong password
    print("4. Testing wrong password")
    try:
        register_user(email="correct@example.com", password="CorrectPassword123!")
        authenticate_user(email="correct@example.com", password="WrongPassword123!")
        print("   ✗ Should have raised AuthenticationError")
    except AuthenticationError as e:
        print(f"   ✓ Caught error: {e}")

    # Invalid token
    print("5. Testing invalid token")
    result = validate_session_token("invalid-token-12345")
    if result is None:
        print("   ✓ Invalid token correctly rejected")
    else:
        print("   ✗ Invalid token should return None")


if __name__ == "__main__":
    """Run all examples."""
    print("=" * 60)
    print("Authentication System Examples")
    print("=" * 60)

    # Note: These examples require a running PostgreSQL database
    # with the schema created. See database/README.md for setup.

    try:
        example_registration_and_login()
        example_session_validation()
        example_authentication_flow()
        example_error_handling()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        print("Make sure PostgreSQL is running and schema is created.")
