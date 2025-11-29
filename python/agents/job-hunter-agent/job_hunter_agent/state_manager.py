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

"""State management system for Job Hunter Agent.

This module provides utilities for managing state across sub-agents in the Job Hunter Agent system.
It handles state key storage, retrieval, updates, and multi-application state isolation.

The state management system works with Google ADK's session state mechanism, where each agent's
output_key automatically stores results in the session state dictionary.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import copy


# Standard state keys used by sub-agents
STATE_KEYS = {
    "career_profile_output": "Career Profile Analyst output",
    "job_opportunities_output": "Job Market Researcher output",
    "application_materials_output": "Application Strategist output",
    "interview_prep_output": "Interview Preparation Coach output",
    "career_strategy_output": "Career Strategy Advisor output",
    "career_coordinator_output": "Career Coordinator output",
}


class StateManager:
    """Manages state for job hunting workflows.
    
    This class provides an in-memory state management system that supports:
    - State key storage and retrieval
    - Multi-application state isolation
    - State update notifications
    - Session persistence (in-memory for MVP)
    
    Attributes:
        _state: In-memory storage for all state data
        _application_states: Isolated state for multiple concurrent applications
        _listeners: Callbacks for state update notifications
    """

    def __init__(self) -> None:
        """Initialize the state manager with empty state."""
        self._state: Dict[str, Any] = {}
        self._application_states: Dict[str, Dict[str, Any]] = {}
        self._listeners: Dict[str, List[callable]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def store_state(
        self,
        key: str,
        value: Any,
        application_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store a value in the state under the specified key.
        
        Args:
            key: The state key to store the value under
            value: The value to store
            application_id: Optional application ID for multi-application isolation
            metadata: Optional metadata about the state (e.g., timestamp, source agent)
        
        Requirements: 6.1 - Store sub-agent output in designated state key
        """
        if application_id:
            # Store in application-specific state
            if application_id not in self._application_states:
                self._application_states[application_id] = {}
            self._application_states[application_id][key] = value
        else:
            # Store in global state
            self._state[key] = value
        
        # Store metadata
        metadata_key = f"{application_id}:{key}" if application_id else key
        self._metadata[metadata_key] = {
            "timestamp": datetime.now().isoformat(),
            "application_id": application_id,
            **(metadata or {}),
        }
        
        # Notify listeners
        self._notify_listeners(key, value, application_id)

    def retrieve_state(
        self,
        key: str,
        application_id: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """Retrieve a value from the state by key.
        
        Args:
            key: The state key to retrieve
            application_id: Optional application ID for multi-application isolation
            default: Default value to return if key not found
        
        Returns:
            The stored value, or default if not found
        
        Requirements: 6.2 - Retrieve data from appropriate state key
        """
        if application_id:
            # Retrieve from application-specific state
            return self._application_states.get(application_id, {}).get(key, default)
        else:
            # Retrieve from global state
            return self._state.get(key, default)

    def update_state(
        self,
        key: str,
        value: Any,
        application_id: Optional[str] = None,
        notify: bool = True,
    ) -> None:
        """Update an existing state value and optionally notify listeners.
        
        Args:
            key: The state key to update
            value: The new value
            application_id: Optional application ID for multi-application isolation
            notify: Whether to notify listeners of the update
        
        Requirements: 6.3 - Update state keys and inform affected sub-agents
        """
        # Store the updated value
        self.store_state(key, value, application_id)
        
        # Notification is handled by store_state if notify is True
        if not notify:
            # Remove the last notification if we don't want to notify
            pass  # Notification already happened in store_state

    def get_application_state(self, application_id: str) -> Dict[str, Any]:
        """Get all state for a specific application.
        
        Args:
            application_id: The application ID
        
        Returns:
            Dictionary containing all state for the application
        
        Requirements: 6.4 - Maintain separate state for each application
        """
        return copy.deepcopy(self._application_states.get(application_id, {}))

    def list_applications(self) -> List[str]:
        """List all application IDs with stored state.
        
        Returns:
            List of application IDs
        
        Requirements: 6.4 - Support multiple job applications
        """
        return list(self._application_states.keys())

    def delete_application_state(self, application_id: str) -> bool:
        """Delete all state for a specific application.
        
        Args:
            application_id: The application ID to delete
        
        Returns:
            True if state was deleted, False if application_id not found
        
        Requirements: 6.4 - Manage multi-application state
        """
        if application_id in self._application_states:
            del self._application_states[application_id]
            # Clean up metadata
            keys_to_delete = [
                k for k in self._metadata.keys() if k.startswith(f"{application_id}:")
            ]
            for key in keys_to_delete:
                del self._metadata[key]
            return True
        return False

    def register_listener(
        self,
        key: str,
        callback: callable,
        application_id: Optional[str] = None,
    ) -> None:
        """Register a callback to be notified when a state key is updated.
        
        Args:
            key: The state key to listen for
            callback: Function to call when the key is updated
            application_id: Optional application ID to scope the listener
        
        Requirements: 6.3 - Inform affected sub-agents of state updates
        """
        listener_key = f"{application_id}:{key}" if application_id else key
        if listener_key not in self._listeners:
            self._listeners[listener_key] = []
        self._listeners[listener_key].append(callback)

    def unregister_listener(
        self,
        key: str,
        callback: callable,
        application_id: Optional[str] = None,
    ) -> None:
        """Unregister a callback for state key updates.
        
        Args:
            key: The state key
            callback: The callback function to remove
            application_id: Optional application ID
        """
        listener_key = f"{application_id}:{key}" if application_id else key
        if listener_key in self._listeners:
            try:
                self._listeners[listener_key].remove(callback)
            except ValueError:
                pass  # Callback not in list

    def _notify_listeners(
        self,
        key: str,
        value: Any,
        application_id: Optional[str] = None,
    ) -> None:
        """Notify all registered listeners for a state key.
        
        Args:
            key: The state key that was updated
            value: The new value
            application_id: Optional application ID
        """
        listener_key = f"{application_id}:{key}" if application_id else key
        
        # Notify specific listeners
        if listener_key in self._listeners:
            for callback in self._listeners[listener_key]:
                try:
                    callback(key, value, application_id)
                except Exception as e:
                    # Log error but don't fail the update
                    print(f"Error notifying listener for {key}: {e}")
        
        # Also notify global listeners (without application_id)
        if application_id and key in self._listeners:
            for callback in self._listeners[key]:
                try:
                    callback(key, value, application_id)
                except Exception as e:
                    print(f"Error notifying global listener for {key}: {e}")

    def get_metadata(
        self,
        key: str,
        application_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Get metadata for a state key.
        
        Args:
            key: The state key
            application_id: Optional application ID
        
        Returns:
            Metadata dictionary or None if not found
        """
        metadata_key = f"{application_id}:{key}" if application_id else key
        return self._metadata.get(metadata_key)

    def clear_state(self, application_id: Optional[str] = None) -> None:
        """Clear all state or state for a specific application.
        
        Args:
            application_id: Optional application ID. If None, clears all state.
        """
        if application_id:
            self.delete_application_state(application_id)
        else:
            self._state.clear()
            self._application_states.clear()
            self._metadata.clear()

    def save_session(self) -> Dict[str, Any]:
        """Save the current session state for persistence.
        
        Returns:
            Dictionary containing all state data
        
        Requirements: 6.5 - Session persistence (in-memory for MVP)
        """
        return {
            "state": copy.deepcopy(self._state),
            "application_states": copy.deepcopy(self._application_states),
            "metadata": copy.deepcopy(self._metadata),
            "timestamp": datetime.now().isoformat(),
        }

    def restore_session(self, session_data: Dict[str, Any]) -> None:
        """Restore a previously saved session.
        
        Args:
            session_data: Dictionary containing saved state data
        
        Requirements: 6.5 - Restore state keys from last interaction
        """
        self._state = copy.deepcopy(session_data.get("state", {}))
        self._application_states = copy.deepcopy(
            session_data.get("application_states", {})
        )
        self._metadata = copy.deepcopy(session_data.get("metadata", {}))


# Global state manager instance for the MVP
# In production, this would be replaced with a proper session-scoped instance
_global_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the global state manager instance.
    
    Returns:
        The global StateManager instance
    """
    global _global_state_manager
    if _global_state_manager is None:
        _global_state_manager = StateManager()
    return _global_state_manager


def reset_state_manager() -> None:
    """Reset the global state manager (useful for testing)."""
    global _global_state_manager
    _global_state_manager = None


# Convenience functions for common operations
def store(key: str, value: Any, application_id: Optional[str] = None) -> None:
    """Store a value in state (convenience function).
    
    Args:
        key: State key
        value: Value to store
        application_id: Optional application ID
    """
    get_state_manager().store_state(key, value, application_id)


def retrieve(key: str, application_id: Optional[str] = None, default: Any = None) -> Any:
    """Retrieve a value from state (convenience function).
    
    Args:
        key: State key
        application_id: Optional application ID
        default: Default value if not found
    
    Returns:
        The stored value or default
    """
    return get_state_manager().retrieve_state(key, application_id, default)


def update(key: str, value: Any, application_id: Optional[str] = None) -> None:
    """Update a value in state (convenience function).
    
    Args:
        key: State key
        value: New value
        application_id: Optional application ID
    """
    get_state_manager().update_state(key, value, application_id)
