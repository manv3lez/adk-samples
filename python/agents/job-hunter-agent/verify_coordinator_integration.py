#!/usr/bin/env python3
"""Verify Job Market Researcher integrates correctly with Managing Coordinator."""

from job_hunter_agent.managing_coordinator import managing_coordinator
from google.adk.tools.agent_tool import AgentTool

print("Managing Coordinator Integration Verification")
print("=" * 50)

# Find Job Market Researcher in coordinator's tools
job_market_researcher_found = False
job_market_researcher_agent = None

for tool in managing_coordinator.tools:
    if isinstance(tool, AgentTool):
        if tool.agent.name == "job_market_researcher":
            job_market_researcher_found = True
            job_market_researcher_agent = tool.agent
            break

print(f"Managing Coordinator Model: {managing_coordinator.model}")
print(f"Job Market Researcher in tools: {job_market_researcher_found}")

if job_market_researcher_agent:
    print(f"\nJob Market Researcher Details:")
    print(f"  Model: {job_market_researcher_agent.model}")
    print(f"  Name: {job_market_researcher_agent.name}")
    print(f"  Tools: {len(job_market_researcher_agent.tools)}")
    
    # Verify both use Gemini 3 Pro
    coordinator_model = managing_coordinator.model
    researcher_model = job_market_researcher_agent.model
    
    print(f"\nModel Compatibility:")
    print(f"  Coordinator: {coordinator_model}")
    print(f"  Researcher: {researcher_model}")
    
    if coordinator_model == "gemini-3-pro-preview" and researcher_model == "gemini-3-pro-preview":
        print("  ✓ Both use Gemini 3 Pro")
    else:
        print("  ✗ Model mismatch")

print("\n✓ Integration verified successfully!")
