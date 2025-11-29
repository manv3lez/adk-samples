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

Error Handling:
---------------
This agent includes error handling for common issues:
- Missing or incomplete user information
- Invalid resume formats
- Parsing errors

When errors occur, the agent will provide user-friendly messages and suggested next steps.
"""

from google.adk.agents import LlmAgent

from . import prompt

MODEL = "gemini-2.5-pro"

career_profile_analyst_agent = LlmAgent(
    model=MODEL,
    name="career_profile_analyst",
    description=(
        "Analyze user background, skills, experience, and career goals to create "
        "a comprehensive career profile including strengths, gaps, and recommendations. "
        "Handles errors gracefully and provides clear guidance when issues occur."
    ),
    instruction=prompt.CAREER_PROFILE_ANALYST_PROMPT,
    output_key="career_profile_output",
    tools=[],
)
