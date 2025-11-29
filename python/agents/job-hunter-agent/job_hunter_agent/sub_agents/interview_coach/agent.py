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

"""Interview Preparation Coach sub-agent for comprehensive interview preparation.

Error Handling:
---------------
This agent includes error handling for common issues:
- Missing career profile or job details
- Google Search API failures
- Insufficient information for personalized preparation
- Network timeouts

When errors occur, the agent will provide user-friendly messages and suggested next steps.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

interview_coach_agent = LlmAgent(
    model=MODEL,
    name="interview_coach",
    description=(
        "Provide comprehensive interview preparation including company culture research, "
        "behavioral and technical question generation, STAR method examples based on the "
        "user's career profile, technical study topic identification, and interview tips. "
        "Uses Google Search to research companies and organizes content by question type "
        "and difficulty level. Handles errors gracefully and provides clear guidance when issues occur."
    ),
    instruction=prompt.INTERVIEW_COACH_PROMPT,
    output_key="interview_prep_output",
    tools=[google_search],
)
