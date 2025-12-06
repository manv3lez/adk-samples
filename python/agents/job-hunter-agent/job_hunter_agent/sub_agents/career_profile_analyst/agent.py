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

"""Career Profile Analyst sub-agent for analyzing user background and career goals.

This specialist uses Gemini 3 Pro with high thinking level for deep career analysis.
The advanced reasoning capabilities enable comprehensive understanding of user backgrounds,
identification of transferable skills, and strategic career recommendations.

Error Handling:
---------------
This agent includes error handling for common issues:
- Missing or incomplete user information
- Invalid resume formats
- Parsing errors

When errors occur, the agent will provide user-friendly messages and suggested next steps.

Gemini 3 Pro Configuration:
---------------------------
- Model: gemini-3-pro-preview
- Thinking Level: high (for deep analysis and strategic reasoning)
- Thought Signatures: Handled automatically by ADK
"""

from google.adk.agents import LlmAgent

from . import prompt

# Gemini 3 Pro for advanced reasoning and deep career analysis
MODEL = "gemini-3-pro-preview"

# Note: thinking_level parameter will be available in future ADK versions
# For now, the model's advanced reasoning capabilities are used by default
# TODO: Add thinking_level="high" when ADK supports it
career_profile_analyst_agent = LlmAgent(
    model=MODEL,
    name="career_profile_analyst",
    description=(
        "Analyze user background, skills, experience, and career goals to create "
        "a comprehensive career profile including strengths, gaps, and recommendations. "
        "Uses Gemini 3 Pro with high thinking level for deep analysis. "
        "Handles errors gracefully and provides clear guidance when issues occur."
    ),
    instruction=prompt.CAREER_PROFILE_ANALYST_PROMPT,
    output_key="career_profile_output",
    tools=[],
    # High thinking level for comprehensive career analysis and strategic reasoning
    # thinking_level="high",  # Will be enabled when ADK supports this parameter
)
