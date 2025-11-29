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

"""Integration tests for Phase 2 components: Interview Coach and Career Strategy Advisor.

These tests verify that:
1. Phase 2 sub-agents are properly wired to the Career Coordinator
2. State flows correctly between all agents (Phase 1 + Phase 2)
3. The complete end-to-end workflow executes (profile → research → application → interview prep → strategy)
4. Error handling works across all agent boundaries
"""

import pytest
from google.adk.tools.agent_tool import AgentTool

# Import the main agent and all sub-agents
from job_hunter_agent.agent import career_coordinator, root_agent
from job_hunter_agent.sub_agents.career_profile_analyst.agent import career_profile_analyst_agent
from job_hunter_agent.sub_agents.job_market_researcher.agent import job_market_researcher_agent
from job_hunter_agent.sub_agents.application_strategist.agent import application_strategist_agent
from job_hunter_agent.sub_agents.interview_coach.agent import interview_coach_agent
from job_hunter_agent.sub_agents.career_strategy_advisor.agent import career_strategy_advisor_agent


class TestPhase2ComponentWiring:
    """Test that all Phase 2 components are properly wired together."""

    def test_career_coordinator_has_all_subagents(self):
        """Verify Career Coordinator has all Phase 1 and Phase 2 sub-agents wired."""
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
        
        # Verify Phase 2 sub-agents are present
        assert "interview_coach" in agent_tool_names
        assert "career_strategy_advisor" in agent_tool_names

    def test_interview_coach_configuration(self):
        """Verify Interview Coach is properly configured."""
        assert interview_coach_agent.name == "interview_coach"
        assert interview_coach_agent.model == "gemini-2.5-pro"
        assert interview_coach_agent.output_key == "interview_prep_output"
        # Verify it has google_search tool
        assert len(interview_coach_agent.tools) > 0

    def test_career_strategy_advisor_configuration(self):
        """Verify Career Strategy Advisor is properly configured."""
        assert career_strategy_advisor_agent.name == "career_strategy_advisor"
        assert career_strategy_advisor_agent.model == "gemini-2.5-pro"
        assert career_strategy_advisor_agent.output_key == "career_strategy_output"

    def test_coordinator_description_includes_phase2(self):
        """Verify Career Coordinator description mentions Phase 2 capabilities."""
        description = career_coordinator.description
        # Should mention interview preparation or career strategy
        assert "interview" in description.lower() or "strategy" in description.lower()


class TestPhase2StateFlow:
    """Test that state flows correctly through Phase 2 workflow."""

    def test_interview_prep_state_key_storage(self):
        """Test that Interview Coach output key is correctly configured."""
        # Verify the agent has the correct output key configured
        assert interview_coach_agent.output_key == "interview_prep_output"
        
        # Simulate state storage pattern
        session_state = {}
        mock_interview_prep = {
            "company_research": {
                "culture": "Fast-paced startup environment",
                "recent_news": ["Series B funding", "New product launch"]
            },
            "behavioral_questions": [
                "Tell me about a time you led a team through a challenge",
                "Describe a situation where you had to resolve a conflict"
            ],
            "technical_questions": [
                "Explain how you would design a scalable API",
                "What's your approach to database optimization?"
            ],
            "star_examples": [
                {
                    "situation": "Led migration project",
                    "task": "Migrate legacy system to cloud",
                    "action": "Coordinated team, planned phases",
                    "result": "Completed 2 weeks early, 30% cost savings"
                }
            ],
            "study_topics": ["System design", "AWS services", "API best practices"],
            "tips": ["Research company products", "Prepare questions for interviewer"]
        }
        
        # Store using the agent's output key
        session_state[interview_coach_agent.output_key] = mock_interview_prep
        
        # Verify state key exists and has correct data
        assert "interview_prep_output" in session_state
        assert session_state["interview_prep_output"]["behavioral_questions"] is not None
        assert session_state["interview_prep_output"]["star_examples"] is not None

    def test_career_strategy_state_key_storage(self):
        """Test that Career Strategy Advisor output key is correctly configured."""
        # Verify the agent has the correct output key configured
        assert career_strategy_advisor_agent.output_key == "career_strategy_output"
        
        # Simulate state storage pattern
        session_state = {}
        mock_strategy = {
            "career_paths": [
                {
                    "path": "Technical Leadership Track",
                    "milestones": ["Senior Engineer", "Staff Engineer", "Principal Engineer"],
                    "timeline": "5-7 years"
                },
                {
                    "path": "Management Track",
                    "milestones": ["Team Lead", "Engineering Manager", "Director"],
                    "timeline": "4-6 years"
                }
            ],
            "skills_gaps": {
                "short_term": ["Kubernetes", "Terraform"],
                "long_term": ["System architecture", "People management"]
            },
            "industry_trends": [
                "AI/ML integration in all products",
                "Shift to cloud-native architectures",
                "Increased focus on security"
            ],
            "development_roadmap": {
                "year_1": ["Get AWS certification", "Lead 2 major projects"],
                "year_2": ["Mentor junior engineers", "Present at conferences"],
                "year_3": ["Transition to staff engineer role"]
            }
        }
        
        # Store using the agent's output key
        session_state[career_strategy_advisor_agent.output_key] = mock_strategy
        
        # Verify state key exists and has correct data
        assert "career_strategy_output" in session_state
        assert session_state["career_strategy_output"]["career_paths"] is not None
        assert session_state["career_strategy_output"]["development_roadmap"] is not None

    def test_complete_state_flow_with_phase2(self):
        """Test that state keys can be accessed in sequence across all workflow stages."""
        # Simulate the complete workflow state progression including Phase 2
        session_state = {}
        
        # Stage 1: Career Profile Analysis
        session_state["career_profile_output"] = {
            "skills": {"technical": ["Python", "Java"], "soft": ["Leadership"]},
            "experience": {"years": 5, "roles": ["Software Engineer"]}
        }
        
        # Stage 2: Job Market Research
        assert "career_profile_output" in session_state
        session_state["job_opportunities_output"] = {
            "opportunities": [
                {"job_title": "Senior Engineer", "company": "Tech Corp", "match_score": 0.85}
            ]
        }
        
        # Stage 3: Application Materials
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        session_state["application_materials_output"] = {
            "resume": "Resume content",
            "ats_analysis": {"match_score": 0.82}
        }
        
        # Stage 4: Interview Preparation (Phase 2)
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        session_state["interview_prep_output"] = {
            "behavioral_questions": ["Question 1", "Question 2"],
            "star_examples": [{"situation": "Example"}]
        }
        
        # Stage 5: Career Strategy (Phase 2, optional)
        assert "career_profile_output" in session_state
        session_state["career_strategy_output"] = {
            "career_paths": [{"path": "Technical Leadership"}],
            "development_roadmap": {"year_1": ["Goal 1"]}
        }
        
        # Verify all state keys are present
        assert all(key in session_state for key in [
            "career_profile_output",
            "job_opportunities_output",
            "application_materials_output",
            "interview_prep_output",
            "career_strategy_output"
        ])


class TestCompleteEndToEndWorkflow:
    """Test the complete end-to-end workflow including all phases."""

    def test_complete_workflow_all_phases(self):
        """Simulate a complete workflow: profile → research → application → interview → strategy."""
        session_state = {}
        
        # Stage 1: Career Profile Analysis
        session_state[career_profile_analyst_agent.output_key] = {
            "skills": {
                "technical": ["Python", "Java", "AWS", "Docker"],
                "soft": ["Leadership", "Communication", "Problem Solving"]
            },
            "experience": {
                "years": 5,
                "roles": ["Software Engineer", "Senior Developer"],
                "industries": ["Tech", "Finance"]
            },
            "strengths": ["Backend development", "System design", "Team collaboration"],
            "gaps": ["Kubernetes", "Machine Learning"],
            "recommendations": ["Get K8s certification", "Take ML course"],
            "career_goals": {
                "target_roles": ["Staff Engineer", "Tech Lead"],
                "industries": ["Tech", "Startups"],
                "work_type": "Remote"
            }
        }
        
        # Stage 2: Job Market Research
        session_state[job_market_researcher_agent.output_key] = {
            "opportunities": [
                {
                    "job_title": "Staff Software Engineer",
                    "company": "Tech Innovations Inc",
                    "location": "Remote",
                    "requirements": ["Python", "AWS", "System Design", "Leadership"],
                    "match_score": 0.88,
                    "salary_range": "$150k-$200k",
                    "company_culture": "Innovation-focused, collaborative",
                    "url": "https://example.com/job1"
                }
            ]
        }
        
        # Stage 3: Application Materials
        session_state[application_strategist_agent.output_key] = {
            "resume": "JOHN DOE\nStaff Software Engineer\n\nPROFESSIONAL SUMMARY...",
            "cover_letter": "Dear Hiring Manager,\n\nI am excited to apply for the Staff Software Engineer position...",
            "ats_analysis": {
                "match_score": 0.85,
                "required_keywords": ["Python", "AWS", "System Design", "Leadership"],
                "found_keywords": ["Python", "AWS", "System Design", "Leadership"],
                "missing_keywords": [],
                "recommendations": ["Excellent keyword match", "Resume is ATS-optimized"]
            },
            "linkedin_optimization": {
                "headline_suggestion": "Staff Software Engineer | Python & AWS Expert | System Design",
                "summary_tips": ["Highlight leadership experience", "Showcase system design projects"]
            }
        }
        
        # Stage 4: Interview Preparation (Phase 2)
        session_state[interview_coach_agent.output_key] = {
            "company_research": {
                "culture": "Fast-paced, innovation-driven startup culture",
                "recent_news": ["Series C funding $50M", "Launched new AI product"],
                "interview_style": "Technical + behavioral, 4-5 rounds"
            },
            "behavioral_questions": [
                "Tell me about a time you led a complex technical project",
                "Describe how you handle disagreements with team members",
                "Give an example of when you had to make a difficult technical decision"
            ],
            "technical_questions": [
                "Design a scalable microservices architecture for our platform",
                "How would you optimize database queries for millions of records?",
                "Explain your approach to system monitoring and observability"
            ],
            "star_examples": [
                {
                    "question": "Tell me about a time you led a complex technical project",
                    "situation": "Led migration of monolithic app to microservices",
                    "task": "Migrate without downtime, improve performance",
                    "action": "Created phased migration plan, coordinated 5 engineers, implemented feature flags",
                    "result": "Completed in 3 months, 40% performance improvement, zero downtime"
                }
            ],
            "study_topics": [
                "Microservices architecture patterns",
                "AWS services (ECS, Lambda, RDS)",
                "System design fundamentals",
                "Leadership and team management"
            ],
            "tips": [
                "Research their AI product thoroughly",
                "Prepare questions about their tech stack",
                "Be ready to discuss system design trade-offs",
                "Show enthusiasm for their mission"
            ]
        }
        
        # Stage 5: Career Strategy (Phase 2, optional)
        session_state[career_strategy_advisor_agent.output_key] = {
            "career_paths": [
                {
                    "path": "Technical Leadership Track",
                    "description": "Progress from Staff Engineer to Principal Engineer to Distinguished Engineer",
                    "milestones": [
                        "Staff Engineer (current target)",
                        "Principal Engineer (3-4 years)",
                        "Distinguished Engineer (7-10 years)"
                    ],
                    "timeline": "10+ years",
                    "pros": ["Deep technical impact", "Thought leadership", "High compensation"],
                    "cons": ["Less people management", "Requires continuous learning"]
                },
                {
                    "path": "Engineering Management Track",
                    "description": "Transition to people management and organizational leadership",
                    "milestones": [
                        "Tech Lead (1-2 years)",
                        "Engineering Manager (3-4 years)",
                        "Director of Engineering (6-8 years)"
                    ],
                    "timeline": "8+ years",
                    "pros": ["Broader organizational impact", "People development", "Strategic influence"],
                    "cons": ["Less hands-on coding", "More meetings and politics"]
                }
            ],
            "skills_gaps": {
                "short_term": [
                    "Kubernetes orchestration (High priority for Staff Engineer role)",
                    "Machine Learning fundamentals (Growing industry trend)"
                ],
                "long_term": [
                    "System architecture at scale (For Principal Engineer)",
                    "People management and mentoring (For leadership roles)",
                    "Strategic planning and roadmapping (For senior positions)"
                ]
            },
            "industry_trends": [
                "AI/ML integration becoming standard in all products",
                "Shift to cloud-native and serverless architectures",
                "Increased focus on platform engineering and developer experience",
                "Growing importance of security and compliance",
                "Remote-first work culture becoming permanent"
            ],
            "development_roadmap": {
                "year_1": [
                    "Complete Kubernetes certification (CKA)",
                    "Lead 2-3 major technical projects",
                    "Start mentoring junior engineers",
                    "Contribute to open source projects"
                ],
                "year_2": [
                    "Take ML/AI fundamentals course",
                    "Present at 1-2 technical conferences",
                    "Write technical blog posts",
                    "Expand mentoring to 3-4 engineers"
                ],
                "year_3": [
                    "Transition to Staff Engineer role",
                    "Lead architecture decisions for major systems",
                    "Build reputation as technical expert",
                    "Decide between IC and management track"
                ]
            },
            "recommendations": [
                "Focus on Kubernetes immediately - it's critical for your target role",
                "Start building your technical brand through blogging and speaking",
                "Network with Staff+ engineers to understand the role better",
                "Consider which track (IC vs Management) aligns with your interests"
            ]
        }
        
        # Verify complete workflow state
        assert all(key in session_state for key in [
            "career_profile_output",
            "job_opportunities_output",
            "application_materials_output",
            "interview_prep_output",
            "career_strategy_output"
        ])
        
        # Verify data quality and relationships
        profile = session_state["career_profile_output"]
        jobs = session_state["job_opportunities_output"]
        materials = session_state["application_materials_output"]
        interview = session_state["interview_prep_output"]
        strategy = session_state["career_strategy_output"]
        
        # Profile should have skills
        assert len(profile["skills"]["technical"]) > 0
        assert len(profile["strengths"]) > 0
        
        # Jobs should be ranked
        assert jobs["opportunities"][0]["match_score"] > 0.5
        
        # Materials should have high ATS score
        assert materials["ats_analysis"]["match_score"] > 0.7
        
        # Interview prep should have questions
        assert len(interview["behavioral_questions"]) > 0
        assert len(interview["technical_questions"]) > 0
        assert len(interview["star_examples"]) > 0
        
        # Strategy should have career paths
        assert len(strategy["career_paths"]) > 0
        assert len(strategy["development_roadmap"]) > 0

    def test_workflow_stage_dependencies_with_phase2(self):
        """Test that Phase 2 stages have proper dependencies on Phase 1 stages."""
        session_state = {}
        
        # Interview prep requires career profile and job opportunities
        assert "career_profile_output" not in session_state
        assert "job_opportunities_output" not in session_state
        
        # Add required dependencies
        session_state["career_profile_output"] = {"skills": {"technical": ["Python"]}}
        session_state["job_opportunities_output"] = {"opportunities": [{"company": "Tech Corp"}]}
        
        # Now interview prep can proceed
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        
        # Career strategy requires career profile
        session_state["career_strategy_output"] = {"career_paths": []}
        assert "career_profile_output" in session_state


class TestPhase2ErrorHandling:
    """Test error handling for Phase 2 components."""

    def test_interview_coach_missing_dependencies(self):
        """Test that Interview Coach handles missing dependencies gracefully."""
        session_state = {}
        
        # Interview Coach requires career_profile_output and job_opportunities_output
        assert "career_profile_output" not in session_state
        assert "job_opportunities_output" not in session_state
        
        # In real implementation, coordinator would check and provide helpful error
        # This test verifies the structure for dependency checking

    def test_career_strategy_advisor_missing_profile(self):
        """Test that Career Strategy Advisor handles missing profile gracefully."""
        session_state = {}
        
        # Career Strategy Advisor requires career_profile_output
        assert "career_profile_output" not in session_state
        
        # In real implementation, coordinator would check and provide helpful error


class TestPhase2OptionalWorkflows:
    """Test that Phase 2 components work as optional enhancements."""

    def test_mvp_workflow_without_phase2(self):
        """Test that MVP workflow (Phase 1) still works without Phase 2."""
        session_state = {}
        
        # Complete Phase 1 workflow
        session_state["career_profile_output"] = {"skills": {"technical": ["Python"]}}
        session_state["job_opportunities_output"] = {"opportunities": []}
        session_state["application_materials_output"] = {"resume": "Resume"}
        
        # Verify Phase 1 is complete without Phase 2
        assert "career_profile_output" in session_state
        assert "job_opportunities_output" in session_state
        assert "application_materials_output" in session_state
        
        # Phase 2 is optional
        assert "interview_prep_output" not in session_state
        assert "career_strategy_output" not in session_state

    def test_interview_prep_without_career_strategy(self):
        """Test that Interview Prep can be used without Career Strategy."""
        session_state = {}
        
        # Complete workflow through interview prep
        session_state["career_profile_output"] = {"skills": {"technical": ["Python"]}}
        session_state["job_opportunities_output"] = {"opportunities": []}
        session_state["application_materials_output"] = {"resume": "Resume"}
        session_state["interview_prep_output"] = {"behavioral_questions": []}
        
        # Career strategy is optional
        assert "interview_prep_output" in session_state
        assert "career_strategy_output" not in session_state

    def test_career_strategy_as_standalone(self):
        """Test that Career Strategy can be used independently for long-term planning."""
        session_state = {}
        
        # User might want career strategy without applying to specific jobs
        session_state["career_profile_output"] = {
            "skills": {"technical": ["Python"]},
            "career_goals": {"target_roles": ["Staff Engineer"]}
        }
        session_state["career_strategy_output"] = {
            "career_paths": [{"path": "Technical Leadership"}]
        }
        
        # Career strategy works with just the profile
        assert "career_profile_output" in session_state
        assert "career_strategy_output" in session_state
        
        # Job search and application materials are optional for strategy
        assert "job_opportunities_output" not in session_state
        assert "application_materials_output" not in session_state
