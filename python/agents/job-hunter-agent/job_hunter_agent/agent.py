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

"""Career Coordinator: orchestrate specialized sub-agents for comprehensive job hunting assistance.

State Management:
-----------------
The Job Hunter Agent uses a state management system to maintain data flow between sub-agents.
Each sub-agent stores its output in a designated state key (via the output_key parameter).

For advanced state management features like multi-application isolation and session persistence,
use the state_manager module:

    from job_hunter_agent.state_manager import get_state_manager
    
    state_manager = get_state_manager()
    state_manager.store_state("key", value, application_id="app1")
    value = state_manager.retrieve_state("key", application_id="app1")

See state_manager.py for full documentation and state_integration_example.py for usage examples.

Error Handling:
---------------
The Job Hunter Agent includes comprehensive error handling to provide user-friendly error messages
and suggested next steps. Use the error_handler module for consistent error handling:

    from job_hunter_agent.error_handler import handle_error, handle_agent_failure
    
    try:
        # Agent operation
        result = agent.run(input)
    except Exception as e:
        error_response = handle_error(e, context={"agent": "agent_name"})
        # Return error_response to user

See error_handler.py for full documentation and available error handling functions.

User Interaction Features:
--------------------------
The Job Hunter Agent implements comprehensive user interaction features to provide clear
guidance and explanations throughout the job hunting process:

1. **Workflow Stage Explanations (Requirement 9.1)**:
   - At the start of each stage, the coordinator explains what will happen, what information
     is needed, and how long it will take
   - Transitions between stages include explanations of next steps

2. **Sub-Agent Activity Notifications (Requirement 9.2)**:
   - Before calling a sub-agent, users are informed which agent is being activated
   - During processing, status updates are provided
   - After completion, results are summarized

3. **Markdown Formatting (Requirement 9.3)**:
   - Results can be formatted as markdown for better readability
   - Use the markdown_formatter utilities to format different types of output:
   
    from job_hunter_agent.utils import (
        format_career_profile,
        format_job_opportunities,
        format_application_materials,
    )
    
    formatted_output = format_career_profile(profile_data)

4. **Help and Explanation System (Requirement 9.4)**:
   - The coordinator provides clear explanations without technical jargon
   - Users can ask questions about any stage or concept
   - Help is offered proactively when users seem confused

5. **AI Disclaimer Inclusion (Requirement 10.4)**:
   - AI disclaimers are shown at session start
   - Reminders to review and personalize content are included with all generated materials
   - Users are encouraged to verify that content represents their authentic experience

See user_interaction_example.py for detailed examples of all user interaction features.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from . import error_handler

# Sub-agents will be imported as they are implemented
from .sub_agents.career_profile_analyst import career_profile_analyst_agent
from .sub_agents.job_market_researcher import job_market_researcher_agent
from .sub_agents.application_strategist import application_strategist_agent
from .sub_agents.interview_coach import interview_coach_agent
from .sub_agents.career_strategy_advisor import career_strategy_advisor_agent

# Phase 2: Import Managing Coordinator for flexible routing
from .managing_coordinator import managing_coordinator


MODEL = "gemini-2.5-pro"


# Phase 1: Career Coordinator (rigid pipeline - kept for backward compatibility)
career_coordinator = LlmAgent(
    name="career_coordinator",
    model=MODEL,
    description=(
        "Guide job seekers through a structured job hunting process by orchestrating "
        "specialized sub-agents. Help them analyze their career profile, research job "
        "opportunities, create tailored application materials, prepare for interviews, "
        "and provide long-term career strategy guidance."
    ),
    instruction=prompt.CAREER_COORDINATOR_PROMPT,
    output_key="career_coordinator_output",
    tools=[
        # All Phase 1 and Phase 2 sub-agents
        AgentTool(agent=career_profile_analyst_agent),
        AgentTool(agent=job_market_researcher_agent),
        AgentTool(agent=application_strategist_agent),
        AgentTool(agent=interview_coach_agent),
        AgentTool(agent=career_strategy_advisor_agent),
    ],
)

# Phase 2: Use Managing Coordinator as root agent (flexible routing)
# This provides a better user experience with LLM-based intent understanding
root_agent = managing_coordinator
