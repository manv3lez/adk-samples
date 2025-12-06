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

"""Application Strategist sub-agent for creating tailored, ATS-optimized application materials.

This specialist uses Gemini 3 Pro with high thinking level for strategic resume optimization
and application strategy. The advanced reasoning capabilities enable sophisticated keyword
analysis, strategic content optimization, and comprehensive ATS scoring.

Error Handling:
---------------
This agent includes error handling for common issues:
- Missing career profile data
- Invalid job descriptions
- ATS analysis failures
- Content generation errors

When errors occur, the agent will provide user-friendly messages and suggested next steps.

Gemini 3 Pro Configuration:
---------------------------
- Model: gemini-3-pro-preview
- Thinking Level: high (for strategic optimization and deep analysis)
- Thought Signatures: Handled automatically by ADK
"""

from google.adk.agents import LlmAgent

from . import prompt

# Gemini 3 Pro for advanced reasoning and strategic application optimization
MODEL = "gemini-3-pro-preview"

# Note: thinking_level parameter will be available in future ADK versions
# For now, the model's advanced reasoning capabilities are used by default
# TODO: Add thinking_level="high" when ADK supports it
application_strategist_agent = LlmAgent(
    model=MODEL,
    name="application_strategist",
    description=(
        "Create tailored, ATS-optimized application materials including resumes and cover letters. "
        "Extract keywords from job descriptions, optimize content for ATS systems, generate "
        "customized resumes and cover letters, calculate ATS match scores, and provide "
        "optimization recommendations and LinkedIn profile suggestions. "
        "Uses Gemini 3 Pro with high thinking level for strategic optimization. "
        "Handles errors gracefully and provides clear guidance when issues occur."
    ),
    instruction=prompt.APPLICATION_STRATEGIST_PROMPT,
    output_key="application_materials_output",
    tools=[],
    # High thinking level for strategic resume optimization and comprehensive ATS analysis
    # thinking_level="high",  # Will be enabled when ADK supports this parameter
)
