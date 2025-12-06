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

"""Tests for the Application Strategist sub-agent."""

import pytest

# Check if google.adk is available
try:
    import google.adk
    GOOGLE_ADK_AVAILABLE = True
except ImportError:
    GOOGLE_ADK_AVAILABLE = False


class TestApplicationStrategistAgent:
    """Test suite for Application Strategist agent."""

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_agent_exists(self):
        """Test that the Application Strategist agent can be imported."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        assert application_strategist_agent is not None
        assert application_strategist_agent.name == "application_strategist"

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_has_correct_output_key(self):
        """Test that the Application Strategist has the correct output key."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        assert application_strategist_agent.output_key == "application_materials_output"

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_has_description(self):
        """Test that the Application Strategist has a description."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        assert application_strategist_agent.description is not None
        assert len(application_strategist_agent.description) > 0
        assert "ATS" in application_strategist_agent.description

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_has_instruction(self):
        """Test that the Application Strategist has an instruction prompt."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        assert application_strategist_agent.instruction is not None
        assert len(application_strategist_agent.instruction) > 0

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_wired_to_coordinator(self):
        """Test that the Application Strategist is wired to the Career Coordinator."""
        from job_hunter_agent.agent import career_coordinator

        # Check that the coordinator has tools
        assert career_coordinator.tools is not None
        assert len(career_coordinator.tools) > 0

        # Check that one of the tools is the Application Strategist
        tool_names = [tool.agent.name for tool in career_coordinator.tools]
        assert "application_strategist" in tool_names

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_prompt_contains_key_sections(self):
        """Test that the prompt contains key sections for application materials generation."""
        from job_hunter_agent.sub_agents.application_strategist import prompt

        prompt_text = prompt.APPLICATION_STRATEGIST_PROMPT

        # Check for key sections
        assert "Agent Role: Application Strategist" in prompt_text
        assert "ATS" in prompt_text
        assert "resume" in prompt_text.lower()
        assert "cover letter" in prompt_text.lower()
        assert "keywords" in prompt_text.lower()
        assert "optimization" in prompt_text.lower()
        assert "linkedin" in prompt_text.lower()

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_prompt_mentions_ats_analyzer(self):
        """Test that the prompt mentions the ATS Keyword Analyzer utility."""
        from job_hunter_agent.sub_agents.application_strategist import prompt

        prompt_text = prompt.APPLICATION_STRATEGIST_PROMPT

        assert "ATS Keyword Analyzer" in prompt_text or "keyword" in prompt_text.lower()

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_prompt_includes_authenticity_requirements(self):
        """Test that the prompt includes authenticity requirements."""
        from job_hunter_agent.sub_agents.application_strategist import prompt

        prompt_text = prompt.APPLICATION_STRATEGIST_PROMPT

        assert "authentic" in prompt_text.lower()
        assert "fabricate" in prompt_text.lower() or "do not" in prompt_text.lower()

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_prompt_includes_formatting_guidelines(self):
        """Test that the prompt includes ATS-friendly formatting guidelines."""
        from job_hunter_agent.sub_agents.application_strategist import prompt

        prompt_text = prompt.APPLICATION_STRATEGIST_PROMPT

        assert "formatting" in prompt_text.lower()
        assert "ATS-friendly" in prompt_text or "ats" in prompt_text.lower()

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_uses_gemini_3_pro(self):
        """Test that the Application Strategist uses Gemini 3 Pro model."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        assert application_strategist_agent.model == "gemini-3-pro-preview"

    @pytest.mark.skipif(not GOOGLE_ADK_AVAILABLE, reason="google.adk not installed")
    def test_application_strategist_description_mentions_gemini_3(self):
        """Test that the Application Strategist description mentions Gemini 3 Pro."""
        from job_hunter_agent.sub_agents.application_strategist import (
            application_strategist_agent,
        )

        description = application_strategist_agent.description
        assert "Gemini 3 Pro" in description or "gemini-3" in description.lower()
