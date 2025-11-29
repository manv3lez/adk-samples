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

"""Career Strategy Advisor sub-agent for long-term career planning and strategic guidance.

This agent provides:
- Career path analysis with multiple progression options
- Skills gap identification for long-term goals
- Industry trend forecasting
- Comprehensive development roadmaps
- Strategic career planning guidance

Error Handling:
---------------
This agent includes error handling for common issues:
- Missing career profile data
- Unclear long-term goals
- Limited industry information

When errors occur, the agent will provide user-friendly messages and suggested next steps.
"""

from google.adk.agents import LlmAgent

from . import prompt

MODEL = "gemini-2.5-pro"

career_strategy_advisor_agent = LlmAgent(
    model=MODEL,
    name="career_strategy_advisor",
    description=(
        "Provide long-term career planning and strategic guidance by analyzing career paths, "
        "identifying skills gaps for future goals, forecasting industry trends, and creating "
        "comprehensive development roadmaps. Helps job seekers build sustainable, fulfilling careers "
        "beyond their immediate job search. Handles errors gracefully and provides clear guidance."
    ),
    instruction=prompt.CAREER_STRATEGY_ADVISOR_PROMPT,
    output_key="career_strategy_output",
    tools=[],
)
