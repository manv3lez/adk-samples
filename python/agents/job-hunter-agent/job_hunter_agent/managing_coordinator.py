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

"""Managing Coordinator: Flexible routing agent for career advisory service.

This module implements the Managing Coordinator agent that uses LLM-based routing
to intelligently direct user questions to relevant specialist agents. Unlike the
Phase 1 Career Coordinator which enforced a rigid pipeline, the Managing Coordinator
listens to user questions and routes flexibly based on intent.

Key Features:
- LLM-based intent understanding (no hardcoded keywords)
- Flexible routing to 1-3 specialists based on question
- Response synthesis from multiple specialists
- Conversation history management
- Context-aware routing decisions

Requirements Addressed:
- 1.1, 1.2: Flexible conversation routing
- 2.1-2.8: Intelligent intent detection
- 3.1-3.5: Conversational response synthesis
- 5.1-5.6: Conversation history management
- 9.1-9.3: Model upgrade to Gemini 3 Pro
- 10.1-10.7: Context-aware specialist selection
"""

from typing import Any, Dict, List, Optional

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import managing_coordinator_prompt
from .sub_agents.career_profile_analyst import career_profile_analyst_agent
from .sub_agents.job_market_researcher import job_market_researcher_agent
from .sub_agents.application_strategist import application_strategist_agent
from .sub_agents.interview_coach import interview_coach_agent
from .sub_agents.career_strategy_advisor import career_strategy_advisor_agent


# Gemini 3 Pro model with thinking level configuration
MODEL = "gemini-3-pro-preview"


def build_coordinator_context(
    conversation_history: Optional[List[Dict[str, str]]] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    cached_analyses: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build context string for the Managing Coordinator.

    Args:
        conversation_history: List of previous messages with role and content
        user_profile: User's career profile data
        cached_analyses: Previously cached analysis results

    Returns:
        Formatted context string for the coordinator prompt
    """
    context_parts = []

    # Format conversation history
    if conversation_history:
        history_text = "\n".join(
            [f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" 
             for msg in conversation_history[-10:]]  # Last 10 messages
        )
        context_parts.append(f"Recent Conversation:\n{history_text}")
    else:
        context_parts.append("Recent Conversation: (No previous messages)")

    # Format user profile
    if user_profile:
        profile_summary = []
        if user_profile.get("background"):
            profile_summary.append(f"Background: {user_profile['background']}")
        if user_profile.get("career_goals"):
            profile_summary.append(f"Career Goals: {user_profile['career_goals']}")
        if user_profile.get("target_roles"):
            profile_summary.append(f"Target Roles: {', '.join(user_profile['target_roles'])}")
        
        if profile_summary:
            context_parts.append(f"User Profile:\n" + "\n".join(profile_summary))
        else:
            context_parts.append("User Profile: (Not yet created)")
    else:
        context_parts.append("User Profile: (Not yet created)")

    # Format cached analyses
    if cached_analyses:
        analyses_summary = []
        for analysis_type, data in cached_analyses.items():
            analyses_summary.append(f"- {analysis_type}: Available")
        
        if analyses_summary:
            context_parts.append(f"Cached Analyses:\n" + "\n".join(analyses_summary))
        else:
            context_parts.append("Cached Analyses: (None)")
    else:
        context_parts.append("Cached Analyses: (None)")

    return "\n\n".join(context_parts)


# Create the Managing Coordinator agent
# Note: Gemini 3 Pro with thinking_level configuration will be available in future ADK versions
# For now, we use the standard model configuration
managing_coordinator = LlmAgent(
    name="managing_coordinator",
    model=MODEL,
    description=(
        "Intelligent career advisor that listens to user questions and routes to "
        "relevant specialist agents. Provides flexible, conversational career guidance "
        "without forcing users through a fixed pipeline."
    ),
    instruction=managing_coordinator_prompt.MANAGING_COORDINATOR_INSTRUCTION,
    output_key="managing_coordinator_output",
    tools=[
        # All specialist agents available for flexible routing
        AgentTool(agent=career_profile_analyst_agent),
        AgentTool(agent=job_market_researcher_agent),
        AgentTool(agent=application_strategist_agent),
        AgentTool(agent=interview_coach_agent),
        AgentTool(agent=career_strategy_advisor_agent),
    ],
)


# Export as root agent for Phase 2
root_agent = managing_coordinator
