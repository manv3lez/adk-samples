# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Error handling system for Job Hunter Agent.

This module provides comprehensive error handling including:
- Error categorization
- User-friendly error message generation
- Next steps suggestion generation
- Error logging

Requirements: 9.5 - Explain errors in user-friendly terms and suggest next steps
"""

import logging
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime


# Configure logging
logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    """Categories of errors that can occur in the Job Hunter Agent system."""
    
    INPUT_VALIDATION = "input_validation"
    EXTERNAL_SERVICE = "external_service"
    STATE_MANAGEMENT = "state_management"
    AGENT_EXECUTION = "agent_execution"
    UNKNOWN = "unknown"


class JobHunterError(Exception):
    """Base exception class for Job Hunter Agent errors.
    
    Attributes:
        message: User-friendly error message
        category: Error category
        details: Technical details for logging
        next_steps: Suggested actions for the user
    """
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        details: Optional[str] = None,
        next_steps: Optional[List[str]] = None,
    ) -> None:
        """Initialize a JobHunterError.
        
        Args:
            message: User-friendly error message
            category: Error category
            details: Technical details for logging
            next_steps: Suggested actions for the user
        """
        super().__init__(message)
        self.message = message
        self.category = category
        self.details = details
        self.next_steps = next_steps or []
        self.timestamp = datetime.now().isoformat()


class InputValidationError(JobHunterError):
    """Error raised when user input is invalid or missing."""
    
    def __init__(self, message: str, details: Optional[str] = None, next_steps: Optional[List[str]] = None) -> None:
        super().__init__(
            message=message,
            category=ErrorCategory.INPUT_VALIDATION,
            details=details,
            next_steps=next_steps,
        )


class ExternalServiceError(JobHunterError):
    """Error raised when an external service (e.g., Google Search) fails."""
    
    def __init__(self, message: str, details: Optional[str] = None, next_steps: Optional[List[str]] = None) -> None:
        super().__init__(
            message=message,
            category=ErrorCategory.EXTERNAL_SERVICE,
            details=details,
            next_steps=next_steps,
        )


class StateManagementError(JobHunterError):
    """Error raised when state management operations fail."""
    
    def __init__(self, message: str, details: Optional[str] = None, next_steps: Optional[List[str]] = None) -> None:
        super().__init__(
            message=message,
            category=ErrorCategory.STATE_MANAGEMENT,
            details=details,
            next_steps=next_steps,
        )


class AgentExecutionError(JobHunterError):
    """Error raised when an agent fails to execute properly."""
    
    def __init__(self, message: str, details: Optional[str] = None, next_steps: Optional[List[str]] = None) -> None:
        super().__init__(
            message=message,
            category=ErrorCategory.AGENT_EXECUTION,
            details=details,
            next_steps=next_steps,
        )


def categorize_error(error: Exception) -> ErrorCategory:
    """Categorize an error based on its type and context.
    
    Args:
        error: The exception to categorize
    
    Returns:
        The appropriate ErrorCategory
    """
    if isinstance(error, JobHunterError):
        return error.category
    
    error_type = type(error).__name__
    error_message = str(error).lower()
    
    # Input validation errors
    if any(keyword in error_message for keyword in ["invalid", "missing", "required", "empty", "format"]):
        return ErrorCategory.INPUT_VALIDATION
    
    # External service errors
    if any(keyword in error_message for keyword in ["api", "network", "timeout", "connection", "rate limit"]):
        return ErrorCategory.EXTERNAL_SERVICE
    
    # State management errors
    if any(keyword in error_message for keyword in ["state", "key", "session", "storage"]):
        return ErrorCategory.STATE_MANAGEMENT
    
    # Agent execution errors
    if any(keyword in error_message for keyword in ["agent", "tool", "model", "generation"]):
        return ErrorCategory.AGENT_EXECUTION
    
    return ErrorCategory.UNKNOWN


def generate_user_friendly_message(error: Exception, category: ErrorCategory) -> str:
    """Generate a user-friendly error message.
    
    Args:
        error: The exception that occurred
        category: The error category
    
    Returns:
        A user-friendly error message
    
    Requirements: 9.5 - Explain errors in user-friendly terms
    """
    if isinstance(error, JobHunterError):
        return error.message
    
    # Generate user-friendly messages based on category
    if category == ErrorCategory.INPUT_VALIDATION:
        return (
            "There was an issue with the information provided. "
            "Please check that all required fields are filled out correctly."
        )
    elif category == ErrorCategory.EXTERNAL_SERVICE:
        return (
            "We're having trouble connecting to external services right now. "
            "This might be a temporary issue with our job search or research tools."
        )
    elif category == ErrorCategory.STATE_MANAGEMENT:
        return (
            "We encountered an issue managing your session data. "
            "Your progress might not have been saved correctly."
        )
    elif category == ErrorCategory.AGENT_EXECUTION:
        return (
            "One of our specialized assistants encountered an issue while processing your request. "
            "This might be a temporary problem."
        )
    else:
        return (
            "An unexpected error occurred. "
            "We're working to resolve this issue."
        )


def generate_next_steps(error: Exception, category: ErrorCategory) -> List[str]:
    """Generate suggested next steps for the user.
    
    Args:
        error: The exception that occurred
        category: The error category
    
    Returns:
        List of suggested next steps
    
    Requirements: 9.5 - Suggest next steps when errors occur
    """
    if isinstance(error, JobHunterError) and error.next_steps:
        return error.next_steps
    
    # Generate next steps based on category
    if category == ErrorCategory.INPUT_VALIDATION:
        return [
            "Review the information you provided and ensure all required fields are complete",
            "Check that your resume or profile is in a supported format (PDF, DOCX, or plain text)",
            "Try simplifying your input and submitting again",
            "If the issue persists, contact support for assistance",
        ]
    elif category == ErrorCategory.EXTERNAL_SERVICE:
        return [
            "Wait a few moments and try again",
            "Check your internet connection",
            "If the problem continues, try again later when the service may be more responsive",
            "Contact support if the issue persists for an extended period",
        ]
    elif category == ErrorCategory.STATE_MANAGEMENT:
        return [
            "Try refreshing your session",
            "Review your recent inputs to ensure they were saved",
            "If needed, re-enter your information to continue",
            "Contact support if you continue to experience data loss",
        ]
    elif category == ErrorCategory.AGENT_EXECUTION:
        return [
            "Try your request again - this may be a temporary issue",
            "Simplify your request and try breaking it into smaller steps",
            "Check that your input is clear and well-formatted",
            "Contact support if the problem persists",
        ]
    else:
        return [
            "Try your request again",
            "If the problem continues, please contact support with details about what you were trying to do",
            "Consider trying a different approach to your task",
        ]


def log_error(
    error: Exception,
    category: ErrorCategory,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """Log error details for debugging and monitoring.
    
    Args:
        error: The exception that occurred
        category: The error category
        context: Additional context about the error (e.g., agent name, user input)
    """
    log_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "category": category.value,
        "timestamp": datetime.now().isoformat(),
    }
    
    if isinstance(error, JobHunterError):
        log_data["details"] = error.details
        log_data["user_message"] = error.message
    
    if context:
        log_data["context"] = context
    
    logger.error(f"Job Hunter Agent Error: {log_data}")


def handle_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Handle an error by categorizing, logging, and generating user response.
    
    This is the main entry point for error handling in the Job Hunter Agent.
    
    Args:
        error: The exception that occurred
        context: Additional context about the error
    
    Returns:
        Dictionary containing error information for the user
    
    Requirements: 9.5 - Explain errors and suggest next steps
    """
    # Categorize the error
    category = categorize_error(error)
    
    # Generate user-friendly message
    user_message = generate_user_friendly_message(error, category)
    
    # Generate next steps
    next_steps = generate_next_steps(error, category)
    
    # Log the error
    log_error(error, category, context)
    
    # Return structured error response
    return {
        "error": True,
        "category": category.value,
        "message": user_message,
        "next_steps": next_steps,
        "timestamp": datetime.now().isoformat(),
    }


def create_error_response(
    message: str,
    next_steps: List[str],
    category: ErrorCategory = ErrorCategory.UNKNOWN,
) -> Dict[str, Any]:
    """Create a structured error response for returning to users.
    
    Args:
        message: User-friendly error message
        next_steps: List of suggested actions
        category: Error category
    
    Returns:
        Structured error response dictionary
    """
    return {
        "error": True,
        "category": category.value,
        "message": message,
        "next_steps": next_steps,
        "timestamp": datetime.now().isoformat(),
    }


# Convenience functions for common error scenarios

def handle_missing_input(field_name: str) -> Dict[str, Any]:
    """Handle missing required input error.
    
    Args:
        field_name: Name of the missing field
    
    Returns:
        Structured error response
    """
    error = InputValidationError(
        message=f"Required information is missing: {field_name}",
        details=f"Field '{field_name}' is required but was not provided",
        next_steps=[
            f"Please provide your {field_name}",
            "Ensure all required fields are filled out",
            "Try submitting your information again",
        ],
    )
    return handle_error(error)


def handle_invalid_format(field_name: str, expected_format: str) -> Dict[str, Any]:
    """Handle invalid format error.
    
    Args:
        field_name: Name of the field with invalid format
        expected_format: Description of the expected format
    
    Returns:
        Structured error response
    """
    error = InputValidationError(
        message=f"The {field_name} format is not valid. Expected: {expected_format}",
        details=f"Field '{field_name}' does not match expected format: {expected_format}",
        next_steps=[
            f"Please ensure your {field_name} is in the correct format: {expected_format}",
            "Check for any typos or formatting issues",
            "Try again with the corrected format",
        ],
    )
    return handle_error(error)


def handle_service_unavailable(service_name: str) -> Dict[str, Any]:
    """Handle external service unavailable error.
    
    Args:
        service_name: Name of the unavailable service
    
    Returns:
        Structured error response
    """
    error = ExternalServiceError(
        message=f"The {service_name} service is currently unavailable",
        details=f"Failed to connect to {service_name}",
        next_steps=[
            "Wait a few moments and try again",
            "Check your internet connection",
            f"The {service_name} service may be experiencing temporary issues",
            "Contact support if the problem persists",
        ],
    )
    return handle_error(error)


def handle_state_not_found(state_key: str) -> Dict[str, Any]:
    """Handle missing state key error.
    
    Args:
        state_key: Name of the missing state key
    
    Returns:
        Structured error response
    """
    error = StateManagementError(
        message="Some required information from a previous step is missing",
        details=f"State key '{state_key}' not found",
        next_steps=[
            "You may need to complete an earlier step first",
            "Try starting from the beginning of this workflow",
            "Ensure your session hasn't expired",
            "Contact support if you continue to experience this issue",
        ],
    )
    return handle_error(error)


def handle_agent_failure(agent_name: str, details: Optional[str] = None) -> Dict[str, Any]:
    """Handle agent execution failure.
    
    Args:
        agent_name: Name of the agent that failed
        details: Optional details about the failure
    
    Returns:
        Structured error response
    """
    error = AgentExecutionError(
        message=f"The {agent_name} assistant encountered an issue while processing your request",
        details=details or f"Agent '{agent_name}' failed to execute",
        next_steps=[
            "Try your request again - this may be a temporary issue",
            "Simplify your request if possible",
            "Ensure your input is clear and complete",
            "Contact support if the problem persists",
        ],
    )
    return handle_error(error)
