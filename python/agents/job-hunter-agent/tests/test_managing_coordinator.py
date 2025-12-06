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

"""Tests for the Managing Coordinator agent with flexible routing.

These tests verify that:
1. Managing Coordinator is properly configured
2. All specialist agents are wired correctly
3. Context building functions work as expected
4. The coordinator is exported as root_agent
"""

import pytest
from google.adk.tools.agent_tool import AgentTool

from job_hunter_agent.managing_coordinator import (
    managing_coordinator,
    build_coordinator_context,
)
from job_hunter_agent import root_agent


class TestManagingCoordinatorConfiguration:
    """Test Managing Coordinator configuration and setup."""

    def test_managing_coordinator_exists(self):
        """Verify Managing Coordinator agent is created."""
        assert managing_coordinator is not None
        assert managing_coordinator.name == "managing_coordinator"

    def test_managing_coordinator_model(self):
        """Verify Managing Coordinator uses Gemini 3 Pro."""
        assert managing_coordinator.model == "gemini-3-pro-preview"

    def test_managing_coordinator_output_key(self):
        """Verify Managing Coordinator has correct output key."""
        assert managing_coordinator.output_key == "managing_coordinator_output"

    def test_managing_coordinator_description(self):
        """Verify Managing Coordinator has appropriate description."""
        description = managing_coordinator.description
        assert "flexible" in description.lower()
        assert "conversational" in description.lower()
        assert "specialist" in description.lower()

    def test_managing_coordinator_has_all_specialists(self):
        """Verify Managing Coordinator has all specialist agents wired."""
        tools = managing_coordinator.tools
        
        # Extract agent names from AgentTools
        agent_tool_names = []
        for tool in tools:
            if isinstance(tool, AgentTool):
                agent_tool_names.append(tool.agent.name)
        
        # Verify all specialists are present
        expected_specialists = [
            "career_profile_analyst",
            "job_market_researcher",
            "application_strategist",
            "interview_coach",
            "career_strategy_advisor",
        ]
        
        for specialist in expected_specialists:
            assert specialist in agent_tool_names, f"Missing specialist: {specialist}"

    def test_managing_coordinator_is_root_agent(self):
        """Verify Managing Coordinator is exported as root_agent."""
        assert root_agent is not None
        assert root_agent.name == "managing_coordinator"


class TestContextBuilding:
    """Test context building functions for Managing Coordinator."""

    def test_build_context_empty(self):
        """Test building context with no data."""
        context = build_coordinator_context()
        
        assert "Recent Conversation: (No previous messages)" in context
        assert "User Profile: (Not yet created)" in context
        assert "Cached Analyses: (None)" in context

    def test_build_context_with_conversation_history(self):
        """Test building context with conversation history."""
        history = [
            {"role": "user", "content": "What jobs should I apply to?"},
            {"role": "assistant", "content": "Let me help you find suitable jobs."},
        ]
        
        context = build_coordinator_context(conversation_history=history)
        
        assert "Recent Conversation:" in context
        assert "What jobs should I apply to?" in context
        assert "Let me help you find suitable jobs." in context

    def test_build_context_with_user_profile(self):
        """Test building context with user profile."""
        profile = {
            "background": "Software engineer with 5 years experience",
            "career_goals": "Transition to senior engineering role",
            "target_roles": ["Senior Software Engineer", "Tech Lead"],
        }
        
        context = build_coordinator_context(user_profile=profile)
        
        assert "User Profile:" in context
        assert "Background: Software engineer with 5 years experience" in context
        assert "Career Goals: Transition to senior engineering role" in context
        assert "Target Roles: Senior Software Engineer, Tech Lead" in context

    def test_build_context_with_cached_analyses(self):
        """Test building context with cached analyses."""
        analyses = {
            "profile_analysis": {"skills": ["Python", "Java"]},
            "job_research": {"opportunities": []},
        }
        
        context = build_coordinator_context(cached_analyses=analyses)
        
        assert "Cached Analyses:" in context
        assert "profile_analysis: Available" in context
        assert "job_research: Available" in context

    def test_build_context_complete(self):
        """Test building context with all data."""
        history = [
            {"role": "user", "content": "Help me with my resume"},
        ]
        profile = {
            "background": "Data scientist",
            "career_goals": "Move to ML engineering",
        }
        analyses = {
            "profile_analysis": {},
        }
        
        context = build_coordinator_context(
            conversation_history=history,
            user_profile=profile,
            cached_analyses=analyses,
        )
        
        # Verify all sections are present
        assert "Recent Conversation:" in context
        assert "User Profile:" in context
        assert "Cached Analyses:" in context
        
        # Verify content
        assert "Help me with my resume" in context
        assert "Data scientist" in context
        assert "profile_analysis: Available" in context

    def test_build_context_limits_conversation_history(self):
        """Test that context building limits conversation history to last 10 messages."""
        # Create 15 messages
        history = [
            {"role": "user", "content": f"Message {i}"}
            for i in range(15)
        ]
        
        context = build_coordinator_context(conversation_history=history)
        
        # Should only include last 10 messages (5-14)
        assert "Message 14" in context
        assert "Message 5" in context
        assert "Message 4" not in context
        assert "Message 0" not in context


class TestManagingCoordinatorPrompt:
    """Test Managing Coordinator prompt configuration."""

    def test_prompt_includes_flexible_routing_guidance(self):
        """Verify prompt includes flexible routing instructions."""
        from job_hunter_agent.managing_coordinator_prompt import (
            MANAGING_COORDINATOR_INSTRUCTION,
        )
        
        prompt = MANAGING_COORDINATOR_INSTRUCTION
        
        # Check for key flexible routing concepts
        assert "LISTEN" in prompt
        assert "flexible" in prompt.lower() or "route" in prompt.lower()
        assert "specialist" in prompt.lower()

    def test_prompt_lists_all_specialists(self):
        """Verify prompt lists all available specialists."""
        from job_hunter_agent.managing_coordinator_prompt import (
            MANAGING_COORDINATOR_INSTRUCTION,
        )
        
        prompt = MANAGING_COORDINATOR_INSTRUCTION
        
        # Check for all specialist names
        assert "Career Profile Analyst" in prompt
        assert "Job Market Researcher" in prompt
        assert "Application Strategist" in prompt
        assert "Interview Preparation" in prompt
        assert "Strategic Career Advisor" in prompt

    def test_prompt_includes_response_synthesis_guidance(self):
        """Verify prompt includes response synthesis instructions."""
        from job_hunter_agent.managing_coordinator_prompt import (
            MANAGING_COORDINATOR_INSTRUCTION,
        )
        
        prompt = MANAGING_COORDINATOR_INSTRUCTION
        
        # Check for synthesis guidance
        assert "SYNTHESIZE" in prompt or "synthesize" in prompt.lower()
        assert "coherent" in prompt.lower() or "combine" in prompt.lower()

    def test_prompt_includes_conversational_guidance(self):
        """Verify prompt emphasizes conversational tone."""
        from job_hunter_agent.managing_coordinator_prompt import (
            MANAGING_COORDINATOR_INSTRUCTION,
        )
        
        prompt = MANAGING_COORDINATOR_INSTRUCTION
        
        # Check for conversational guidance
        assert "conversational" in prompt.lower() or "CONVERSATIONAL" in prompt
        assert "advisor" in prompt.lower()


class TestBackwardCompatibility:
    """Test backward compatibility with Phase 1."""

    def test_career_coordinator_still_available(self):
        """Verify Phase 1 Career Coordinator is still available."""
        from job_hunter_agent.agent import career_coordinator
        
        assert career_coordinator is not None
        assert career_coordinator.name == "career_coordinator"

    def test_both_coordinators_have_same_specialists(self):
        """Verify both coordinators have access to all specialists."""
        from job_hunter_agent.agent import career_coordinator
        
        # Get specialist names from both coordinators
        managing_specialists = [
            tool.agent.name
            for tool in managing_coordinator.tools
            if isinstance(tool, AgentTool)
        ]
        
        career_specialists = [
            tool.agent.name
            for tool in career_coordinator.tools
            if isinstance(tool, AgentTool)
        ]
        
        # Both should have the same specialists
        assert set(managing_specialists) == set(career_specialists)
