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

"""Job Market Researcher sub-agent for researching and identifying job opportunities.

Error Handling:
---------------
This agent includes error handling for common issues:
- Google Search API failures
- Network timeouts
- Rate limiting
- Missing search results

When errors occur, the agent will provide user-friendly messages and suggested next steps.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"

job_market_researcher_agent = LlmAgent(
    model=MODEL,
    name="job_market_researcher",
    description=(
        "Research and identify relevant job opportunities using Google Search. "
        "Query multiple job boards and company career pages, gather company information, "
        "collect salary data, and rank opportunities by relevance to the user's career profile. "
        "Handles external service errors gracefully and provides clear guidance when issues occur."
    ),
    instruction=prompt.JOB_MARKET_RESEARCHER_PROMPT,
    output_key="job_opportunities_output",
    tools=[google_search],
)
