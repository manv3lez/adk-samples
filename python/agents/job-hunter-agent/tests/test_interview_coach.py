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

"""Tests for the Interview Preparation Coach sub-agent."""

import pytest

# Check if google.adk is available
try:
    import google.adk
    GOOGLE_ADK_AVAILABLE = True
except ImportError:
    GOOGLE_ADK_AVAILABLE = False


class TestInterviewCoachAgent:
    """Test suite for Interview Preparation Coach agent."""

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_agent_exists(self):
        """Test that the Interview Coach agent can be imported."""
        from job_hunter_agent.sub_agents.interview_coach import interview_coach_agent

        assert interview_coach_agent is not None
        assert interview_coach_agent.name == "interview_coach"

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_has_correct_output_key(self):
        """Test that the Interview Coach has the correct output key."""
        from job_hunter_agent.sub_agents.interview_coach import interview_coach_agent

        assert interview_coach_agent.output_key == "interview_prep_output"

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_has_description(self):
        """Test that the Interview Coach has a description."""
        from job_hunter_agent.sub_agents.interview_coach import interview_coach_agent

        assert interview_coach_agent.description is not None
        assert len(interview_coach_agent.description) > 0
        assert "interview preparation" in interview_coach_agent.description.lower()

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_has_google_search_tool(self):
        """Test that the Interview Coach has Google Search tool for company research."""
        from job_hunter_agent.sub_agents.interview_coach import interview_coach_agent

        assert interview_coach_agent.tools is not None
        assert len(interview_coach_agent.tools) > 0
        # Check that google_search is in the tools
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in interview_coach_agent.tools]
        assert any('google_search' in str(tool).lower() for tool in tool_names)

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_has_instruction(self):
        """Test that the Interview Coach has instruction prompt."""
        from job_hunter_agent.sub_agents.interview_coach import interview_coach_agent

        assert interview_coach_agent.instruction is not None
        assert len(interview_coach_agent.instruction) > 0

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_prompt_contains_key_elements(self):
        """Test that the Interview Coach prompt contains key required elements."""
        from job_hunter_agent.sub_agents.interview_coach import prompt

        prompt_text = prompt.INTERVIEW_COACH_PROMPT
        
        # Check for key elements mentioned in requirements
        assert "company culture" in prompt_text.lower()
        assert "behavioral" in prompt_text.lower()
        assert "technical" in prompt_text.lower()
        assert "star" in prompt_text.lower()
        assert "study topics" in prompt_text.lower() or "study topic" in prompt_text.lower()
        assert "interview_prep_output" in prompt_text

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_interview_coach_integrated_in_coordinator(self):
        """Test that the Interview Coach is integrated into the Career Coordinator."""
        from job_hunter_agent.agent import root_agent

        # Check that interview_coach is in the coordinator's tools
        tool_names = [tool.agent.name if hasattr(tool, 'agent') else str(tool) for tool in root_agent.tools]
        assert "interview_coach" in tool_names
