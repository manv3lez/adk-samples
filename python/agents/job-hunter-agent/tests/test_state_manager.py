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

"""Unit tests for state management system."""

import pytest
from job_hunter_agent.state_manager import (
    StateManager,
    get_state_manager,
    reset_state_manager,
    store,
    retrieve,
    update,
)


class TestStateManager:
    """Test suite for StateManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.state_manager = StateManager()

    def test_store_and_retrieve_state(self):
        """Test basic state storage and retrieval.
        
        Requirements: 6.1, 6.2
        """
        # Store a value
        test_data = {"skills": ["Python", "Java"], "experience": 5}
        self.state_manager.store_state("career_profile_output", test_data)
        
        # Retrieve the value
        retrieved = self.state_manager.retrieve_state("career_profile_output")
        assert retrieved == test_data

    def test_retrieve_nonexistent_key_returns_default(self):
        """Test that retrieving a non-existent key returns the default value.
        
        Requirements: 6.2
        """
        result = self.state_manager.retrieve_state("nonexistent_key", default="default_value")
        assert result == "default_value"

    def test_update_state(self):
        """Test state update functionality.
        
        Requirements: 6.3
        """
        # Store initial value
        self.state_manager.store_state("test_key", "initial_value")
        
        # Update the value
        self.state_manager.update_state("test_key", "updated_value")
        
        # Verify update
        result = self.state_manager.retrieve_state("test_key")
        assert result == "updated_value"

    def test_multi_application_state_isolation(self):
        """Test that state is isolated between different applications.
        
        Requirements: 6.4
        """
        # Store data for application 1
        app1_data = {"company": "Company A", "position": "Engineer"}
        self.state_manager.store_state("application_materials_output", app1_data, application_id="app1")
        
        # Store data for application 2
        app2_data = {"company": "Company B", "position": "Manager"}
        self.state_manager.store_state("application_materials_output", app2_data, application_id="app2")
        
        # Retrieve and verify isolation
        retrieved_app1 = self.state_manager.retrieve_state("application_materials_output", application_id="app1")
        retrieved_app2 = self.state_manager.retrieve_state("application_materials_output", application_id="app2")
        
        assert retrieved_app1 == app1_data
        assert retrieved_app2 == app2_data
        assert retrieved_app1 != retrieved_app2

    def test_get_application_state(self):
        """Test retrieving all state for a specific application.
        
        Requirements: 6.4
        """
        # Store multiple keys for an application
        self.state_manager.store_state("career_profile_output", {"skills": ["Python"]}, application_id="app1")
        self.state_manager.store_state("job_opportunities_output", {"jobs": []}, application_id="app1")
        
        # Get all state for the application
        app_state = self.state_manager.get_application_state("app1")
        
        assert "career_profile_output" in app_state
        assert "job_opportunities_output" in app_state
        assert len(app_state) == 2

    def test_list_applications(self):
        """Test listing all applications with stored state.
        
        Requirements: 6.4
        """
        # Store state for multiple applications
        self.state_manager.store_state("test_key", "value1", application_id="app1")
        self.state_manager.store_state("test_key", "value2", application_id="app2")
        self.state_manager.store_state("test_key", "value3", application_id="app3")
        
        # List applications
        apps = self.state_manager.list_applications()
        
        assert len(apps) == 3
        assert "app1" in apps
        assert "app2" in apps
        assert "app3" in apps

    def test_delete_application_state(self):
        """Test deleting state for a specific application.
        
        Requirements: 6.4
        """
        # Store state for an application
        self.state_manager.store_state("test_key", "value", application_id="app1")
        assert "app1" in self.state_manager.list_applications()
        
        # Delete the application state
        result = self.state_manager.delete_application_state("app1")
        
        assert result is True
        assert "app1" not in self.state_manager.list_applications()
        assert self.state_manager.retrieve_state("test_key", application_id="app1") is None

    def test_delete_nonexistent_application(self):
        """Test deleting a non-existent application returns False."""
        result = self.state_manager.delete_application_state("nonexistent_app")
        assert result is False

    def test_state_update_notifications(self):
        """Test that listeners are notified of state updates.
        
        Requirements: 6.3
        """
        # Track notifications
        notifications = []
        
        def listener(key, value, application_id):
            notifications.append({"key": key, "value": value, "application_id": application_id})
        
        # Register listener
        self.state_manager.register_listener("test_key", listener)
        
        # Update state
        self.state_manager.store_state("test_key", "test_value")
        
        # Verify notification
        assert len(notifications) == 1
        assert notifications[0]["key"] == "test_key"
        assert notifications[0]["value"] == "test_value"

    def test_unregister_listener(self):
        """Test unregistering a listener."""
        notifications = []
        
        def listener(key, value, application_id):
            notifications.append(value)
        
        # Register and then unregister
        self.state_manager.register_listener("test_key", listener)
        self.state_manager.unregister_listener("test_key", listener)
        
        # Update state
        self.state_manager.store_state("test_key", "test_value")
        
        # Verify no notification
        assert len(notifications) == 0

    def test_metadata_storage(self):
        """Test that metadata is stored with state."""
        metadata = {"source": "career_profile_analyst", "version": "1.0"}
        self.state_manager.store_state("test_key", "test_value", metadata=metadata)
        
        retrieved_metadata = self.state_manager.get_metadata("test_key")
        
        assert retrieved_metadata is not None
        assert "timestamp" in retrieved_metadata
        assert retrieved_metadata["source"] == "career_profile_analyst"
        assert retrieved_metadata["version"] == "1.0"

    def test_save_and_restore_session(self):
        """Test session persistence functionality.
        
        Requirements: 6.5
        """
        # Store some state
        self.state_manager.store_state("key1", "value1")
        self.state_manager.store_state("key2", "value2", application_id="app1")
        
        # Save session
        session_data = self.state_manager.save_session()
        
        # Create new state manager and restore
        new_manager = StateManager()
        new_manager.restore_session(session_data)
        
        # Verify restored state
        assert new_manager.retrieve_state("key1") == "value1"
        assert new_manager.retrieve_state("key2", application_id="app1") == "value2"

    def test_clear_state(self):
        """Test clearing all state."""
        # Store some state
        self.state_manager.store_state("key1", "value1")
        self.state_manager.store_state("key2", "value2", application_id="app1")
        
        # Clear all state
        self.state_manager.clear_state()
        
        # Verify state is cleared
        assert self.state_manager.retrieve_state("key1") is None
        assert self.state_manager.retrieve_state("key2", application_id="app1") is None
        assert len(self.state_manager.list_applications()) == 0

    def test_clear_application_specific_state(self):
        """Test clearing state for a specific application."""
        # Store state for multiple applications
        self.state_manager.store_state("key", "value1", application_id="app1")
        self.state_manager.store_state("key", "value2", application_id="app2")
        
        # Clear state for app1
        self.state_manager.clear_state(application_id="app1")
        
        # Verify app1 is cleared but app2 remains
        assert self.state_manager.retrieve_state("key", application_id="app1") is None
        assert self.state_manager.retrieve_state("key", application_id="app2") == "value2"


class TestGlobalStateManager:
    """Test suite for global state manager functions."""

    def setup_method(self):
        """Reset global state manager before each test."""
        reset_state_manager()

    def teardown_method(self):
        """Clean up after each test."""
        reset_state_manager()

    def test_get_state_manager_singleton(self):
        """Test that get_state_manager returns a singleton instance."""
        manager1 = get_state_manager()
        manager2 = get_state_manager()
        
        assert manager1 is manager2

    def test_convenience_functions(self):
        """Test convenience functions for state operations."""
        # Store using convenience function
        store("test_key", "test_value")
        
        # Retrieve using convenience function
        result = retrieve("test_key")
        assert result == "test_value"
        
        # Update using convenience function
        update("test_key", "updated_value")
        result = retrieve("test_key")
        assert result == "updated_value"

    def test_convenience_functions_with_application_id(self):
        """Test convenience functions with application isolation."""
        # Store for different applications
        store("test_key", "value1", application_id="app1")
        store("test_key", "value2", application_id="app2")
        
        # Retrieve and verify isolation
        assert retrieve("test_key", application_id="app1") == "value1"
        assert retrieve("test_key", application_id="app2") == "value2"
