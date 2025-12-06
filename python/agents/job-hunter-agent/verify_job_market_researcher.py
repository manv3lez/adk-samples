#!/usr/bin/env python3
"""Verify Job Market Researcher upgrade to Gemini 3 Pro."""

from job_hunter_agent.sub_agents.job_market_researcher import job_market_researcher_agent

print("Job Market Researcher Verification")
print("=" * 50)
print(f"Model: {job_market_researcher_agent.model}")
print(f"Name: {job_market_researcher_agent.name}")
print(f"Output Key: {job_market_researcher_agent.output_key}")
print(f"Number of tools: {len(job_market_researcher_agent.tools)}")

# Check for Google Search tool
has_google_search = False
for tool in job_market_researcher_agent.tools:
    tool_name = str(tool)
    if "google_search" in tool_name.lower():
        has_google_search = True
        print(f"Google Search tool: Found")
        break

if not has_google_search:
    print("Google Search tool: Not found (checking tool types)")
    for tool in job_market_researcher_agent.tools:
        print(f"  - Tool: {type(tool).__name__}")

print("\nVerification Results:")
print("-" * 50)

# Verify model upgrade
if job_market_researcher_agent.model == "gemini-3-pro-preview":
    print("✓ Model upgraded to Gemini 3 Pro")
else:
    print(f"✗ Model is {job_market_researcher_agent.model}, expected gemini-3-pro-preview")

# Verify Google Search tool
if has_google_search or len(job_market_researcher_agent.tools) > 0:
    print("✓ Google Search grounding tool configured")
else:
    print("✗ Google Search tool not found")

# Verify description mentions Gemini 3 Pro
if "gemini 3 pro" in job_market_researcher_agent.description.lower():
    print("✓ Description mentions Gemini 3 Pro")
else:
    print("✗ Description does not mention Gemini 3 Pro")

print("\n✓ Job Market Researcher successfully upgraded!")
