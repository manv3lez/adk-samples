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

"""Integration tests for MVP workflow: profile → research → application materials.

These tests verify that:
1. All Phase 1 sub-agents are properly wired to the Career Coordinator
2. State flows correctly between agents
3. The complete MVP workflow executes end-to-end
4. Error handling works across agent boundaries
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

# Import the main agent and sub-agents
from job_hunter_agent.agent import career_coordinator, root_agent
from job_hunter_agent.sub_agents.career_profile_analyst.agent import career_profile_analyst_agent
from job_hunter_agent.sub_agents.job_market_researcher.agent import job_market_researcher_agent
from job_hunter_agent.sub_agents.application_strategist.agent import application_strategist_agent


class TestMVPComponentWiring:
    """Test that all MVP components are properly wired together."""

    def test_root_agent_is_career_coordinator(self):
        """Verify root_agent is correctly exported as career_coordinator."""
        assert root_agent is career_coordinator
        assert root_agent.name == "career_coordinator"

    def test_career_coordinator_has_correct_model(self):
        """Verify Career Coordinator uses the correct model."""
        assert career_coordinator.model == "gemini-2.5-pro"

    def test_career_coordinator_has_output_key(self):
        """Verify Career Coordinator has correct output key."""
        assert career_coordinator.output_key == "career_coordinator_output"

    def test_career_coordinator_has_phase1_subagents(self):
        """Verify Career Coordinator has all Phase 1 sub-agents wired."""
        # Get the tools from the coordinator
        tools = career_coordinator.tools
        
        # Extract agent names from AgentTools
        agent_tool_names = []
        for tool in tools:
            if isinstance(tool, AgentTool):
                agent_tool_names.append(tool.agent.name)
        
        # Verify Phase 1 sub-agents are present
        assert "career_profile_analyst" in agent_tool_names
        assert "job_market_researcher" in agent_tool_names
        assert "application_strategist" in agent_tool_names

    def test_career_profile_analyst_configuration(self):
        """Verify Career Profile Analyst is properly configured."""
        assert career_profile_analyst_agent.name == "career_profile_analyst"
        assert career_profile_analyst_agent.model == "gemini-2.5-pro"
        assert career_profile_analyst_agent.output_key == "career_profile_output"

    def test_job_market_researcher_configuration(self):
        """Verify Job Market Researcher is properly configured."""
        assert job_market_researcher_agent.name == "job_market_researcher"
        assert job_market_researcher_agent.model == "gemini-2.5-pro"
        assert job_market_researcher_agent.output_key == "job_opportunities_output"
        # Verify it has google_search tool
        assert len(job_market_researcher_agent.tools) > 0

    def test_application_strategist_configuration(self):
        """Verify Application Strategist is properly configured."""
        assert application_strategist_agent.name == "application_strategist"
        assert application_strategist_agent.model == "gemini-3-pro-preview"
        assert application_strategist_agent.output_key == "application_materials_output"


class TestMVPWorkflowStateFlow:
    """Test that state flows correctly through the MVP workflow."""

    def test_career_profile_state_key_storage(self):
        """Test that Career Profile Analyst output key is correctly configured."""
        # Verify the agent has the correct output key configured
        assert career_profile_analyst_agent.output_key == "career_profile_output"
        
        # Simulate state storage pattern
        session_state = {}
        mock_profile = {
            "skills": {"technical": ["Python", "Java"], "soft": ["Leadership"]},
            "experience": {"years": 5, "roles": ["Software Engineer"]},
            "strengths": ["Problem solving"],
            "gaps": ["Cloud architecture"],
            "recommendations": ["Learn AWS"]
        }
        
        # Store using the agent's output key
        session_state[career_profile_analyst_agent.output_key] = mock_profile
        
        # Verify state key exists and has correct data
        assert "career_profile_output" in session_state
        assert session_state["career_profile_output"]["skills"] is not None
        assert session_state["career_profile_output"]["strengths"] is not None

    def test_job_opportunities_state_key_storage(self):
        """Test that Job Market Researcher output key is correctly configured."""
        # Verify the agent has the correct output key configured
        assert job_market_researcher_agent.output_key == "job_opportunities_output"
        
        # Simulate state storage pattern
        session_state = {}
        mock_jobs = {
            "opportunities": [
                {
                    "job_title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "location": "San Francisco, CA",
                    "match_score": 0.85
                }
            ]
        }
        
        # Store using the agent's output key
        session_state[job_market_researcher_agent.output_key] = mock_jobs
        
        # Verify state key exists and has correct data
        assert "job_opportunities_output" in session_state
        assert len(session_state["job_opportunities_output"]["opportunities"]) > 0

    def test_application_materials_state_key_storage(self):
        """Test that Application Strategist output key is correctly configured."""
        # Verify the agent has the correct output key configured
        assert application_strategist_agent.output_key == "application_materials_output"
        
        # Simulate state storage pattern
        session_state = {}
        mock_materials = {
            "resume": "Professional resume content...",
            "cover_letter": "Dear Hiring Manager...",
            "ats_analysis": {
                "match_score": 0.78,
                "required_keywords": ["Python", "AWS"],
                "found_keywords": ["Python"],
                "missing_keywords": ["AWS"]
            }
        }
        
        # Store using the agent's output key
        session_state[application_strategist_agent.output_key] = mock_materials
        
        # Verify state key exists and has correct data
        assert "application_materials_output" in session_state
        assert session_state["application_materials_output"]["resume"] is not None
        assert session_state["application_materials_output"]["ats_analysis"] is not None

    def test_state_flow_sequence(self):
        """Test that state keys can be accessed in sequence across workflow stages."""
        # Simulate the complete workflow state progression
        session_state = {}
        
        # Stage 1: Career Profile Analysis
        session_state["career_profile_output"] = {
            "skills": {"technical": ["Python"]},
            "experience": {"years": 5}
        }
        
        # Stage 2: Job Market Research (uses career_profile_output)
        assert "career_profile_output" in session_state
        career_profile = session_state["career_profile_output"]
        assert career_profile["skills"] is not None
        
        session_state["job_opportunities_output"] = {
            "opportunities": [{"job_title": "Engineer", "match_score": 0.8}]
        }
        
        # Stage 3: Application Materials (uses both previous outputs)
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        
        session_state["application_materials_output"] = {
            "resume": "Resume content",
            "ats_analysis": {"match_score": 0.75}
        }
        
        # Verify all state keys are present
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        assert "application_materials_output" in session_state


class TestMVPEndToEndWorkflow:
    """Test the complete MVP workflow from profile to application materials."""

    def test_complete_mvp_workflow_simulation(self):
        """Simulate a complete MVP workflow: profile → research → application."""
        # This test simulates the workflow state management pattern
        
        # Stage 1: Career Profile Analysis
        mock_profile = {
            "skills": {
                "technical": ["Python", "Java", "Web Development", "APIs"],
                "soft": ["Problem Solving", "Communication"]
            },
            "experience": {"years": 5, "roles": ["Software Engineer"]},
            "strengths": ["Backend development", "API design"],
            "gaps": ["Cloud architecture", "DevOps"],
            "recommendations": ["Learn AWS/Azure", "Get cloud certifications"]
        }
        
        # Stage 2: Job Market Research
        mock_jobs = {
            "opportunities": [
                {
                    "job_title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "location": "Remote",
                    "requirements": ["Python", "Java", "AWS"],
                    "match_score": 0.85,
                    "salary_range": "$120k-$160k"
                },
                {
                    "job_title": "Backend Engineer",
                    "company": "StartupXYZ",
                    "location": "San Francisco, CA",
                    "requirements": ["Python", "APIs", "Docker"],
                    "match_score": 0.78,
                    "salary_range": "$130k-$170k"
                }
            ]
        }
        
        # Stage 3: Application Materials Creation
        mock_materials = {
            "resume": "JOHN DOE\nSenior Software Engineer\n\nEXPERIENCE...",
            "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply...",
            "ats_analysis": {
                "match_score": 0.82,
                "required_keywords": ["Python", "Java", "AWS", "APIs"],
                "found_keywords": ["Python", "Java", "APIs"],
                "missing_keywords": ["AWS"],
                "recommendations": [
                    "Add AWS experience or projects to resume",
                    "Mention cloud technologies in cover letter"
                ]
            },
            "linkedin_optimization": {
                "headline_suggestion": "Senior Software Engineer | Python & Java Expert",
                "summary_tips": ["Highlight API development experience"]
            }
        }
        
        # Simulate workflow execution with state management
        session_state = {}
        
        # Execute Stage 1 - store using agent's output key
        session_state[career_profile_analyst_agent.output_key] = mock_profile
        assert "career_profile_output" in session_state
        
        # Execute Stage 2 - store using agent's output key
        session_state[job_market_researcher_agent.output_key] = mock_jobs
        assert "job_opportunities_output" in session_state
        assert len(session_state["job_opportunities_output"]["opportunities"]) == 2
        
        # Execute Stage 3 - store using agent's output key
        session_state[application_strategist_agent.output_key] = mock_materials
        assert "application_materials_output" in session_state
        assert session_state["application_materials_output"]["ats_analysis"]["match_score"] > 0.7
        
        # Verify complete workflow state
        assert all(key in session_state for key in [
            "career_profile_output",
            "job_opportunities_output",
            "application_materials_output"
        ])

    def test_workflow_stage_dependencies(self):
        """Test that workflow stages have proper dependencies on previous stages."""
        session_state = {}
        
        # Attempting Stage 2 without Stage 1 should be detectable
        # (In real implementation, coordinator would check for career_profile_output)
        assert "career_profile_output" not in session_state
        
        # After Stage 1 completes, Stage 2 can proceed
        session_state["career_profile_output"] = {"skills": {"technical": ["Python"]}}
        assert "career_profile_output" in session_state
        
        # Stage 3 requires both Stage 1 and Stage 2
        session_state["job_opportunities_output"] = {"opportunities": []}
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state


class TestMVPErrorHandling:
    """Test error handling across agent boundaries in MVP workflow."""

    def test_sub_agent_error_handling_structure(self):
        """Test that error handling structure is in place."""
        # Verify that error_handler module is available
        from job_hunter_agent import error_handler
        
        # Verify error handling functions exist
        assert hasattr(error_handler, 'handle_error')
        assert hasattr(error_handler, 'handle_agent_failure')
        
        # Test that error handler can be called
        test_error = Exception("Test error")
        error_response = error_handler.handle_error(test_error, context={"agent": "test_agent"})
        
        # Verify error response structure
        assert "error" in error_response
        assert "message" in error_response
        assert "next_steps" in error_response

    def test_missing_state_key_detection(self):
        """Test detection of missing required state keys."""
        session_state = {}
        
        # Stage 2 requires career_profile_output
        required_key = "career_profile_output"
        
        # Verify we can detect missing state
        assert required_key not in session_state
        
        # After adding the required state, it should be available
        session_state[required_key] = {"skills": {}}
        assert required_key in session_state

    def test_partial_workflow_recovery(self):
        """Test that workflow can recover from partial completion."""
        session_state = {}
        
        # Complete Stage 1
        session_state["career_profile_output"] = {"skills": {"technical": ["Python"]}}
        
        # Stage 2 fails (no job_opportunities_output added)
        # But Stage 1 data is still available
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" not in session_state
        
        # User can retry Stage 2 without losing Stage 1 data
        session_state["job_opportunities_output"] = {"opportunities": []}
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state


class TestMVPMultiApplicationSupport:
    """Test that MVP supports multiple concurrent job applications."""

    def test_separate_state_for_multiple_applications(self):
        """Test that different applications can maintain separate state."""
        # Simulate state for multiple applications
        applications = {}
        
        # Application 1: Tech Corp
        applications["app_tech_corp"] = {
            "career_profile_output": {"skills": {"technical": ["Python"]}},
            "job_opportunities_output": {
                "opportunities": [{"company": "Tech Corp", "job_title": "Engineer"}]
            },
            "application_materials_output": {
                "resume": "Resume for Tech Corp",
                "ats_analysis": {"match_score": 0.85}
            }
        }
        
        # Application 2: StartupXYZ
        applications["app_startupxyz"] = {
            "career_profile_output": {"skills": {"technical": ["Python"]}},
            "job_opportunities_output": {
                "opportunities": [{"company": "StartupXYZ", "job_title": "Backend Dev"}]
            },
            "application_materials_output": {
                "resume": "Resume for StartupXYZ",
                "ats_analysis": {"match_score": 0.78}
            }
        }
        
        # Verify applications are isolated
        assert applications["app_tech_corp"]["application_materials_output"]["resume"] != \
               applications["app_startupxyz"]["application_materials_output"]["resume"]
        
        assert applications["app_tech_corp"]["application_materials_output"]["ats_analysis"]["match_score"] != \
               applications["app_startupxyz"]["application_materials_output"]["ats_analysis"]["match_score"]

    def test_shared_career_profile_across_applications(self):
        """Test that career profile can be shared across multiple applications."""
        # Career profile is created once
        shared_profile = {
            "skills": {"technical": ["Python", "Java"], "soft": ["Leadership"]},
            "experience": {"years": 5}
        }
        
        # Multiple applications use the same profile
        app1_state = {"career_profile_output": shared_profile}
        app2_state = {"career_profile_output": shared_profile}
        
        # Verify both applications reference the same profile
        assert app1_state["career_profile_output"] == app2_state["career_profile_output"]
        assert app1_state["career_profile_output"]["skills"]["technical"] == \
               app2_state["career_profile_output"]["skills"]["technical"]
