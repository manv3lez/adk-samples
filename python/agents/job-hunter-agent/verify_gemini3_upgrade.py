#!/usr/bin/env python3
"""Verification script for Gemini 3 Pro upgrade.

This script verifies that the Career Profile Analyst has been successfully
upgraded to use Gemini 3 Pro with the appropriate configuration.
"""

from job_hunter_agent.sub_agents.career_profile_analyst import career_profile_analyst_agent
from job_hunter_agent.managing_coordinator import managing_coordinator


def verify_career_profile_analyst():
    """Verify Career Profile Analyst configuration."""
    print("=" * 70)
    print("Career Profile Analyst - Gemini 3 Pro Upgrade Verification")
    print("=" * 70)
    print()
    
    print("✓ Agent Name:", career_profile_analyst_agent.name)
    print("✓ Model:", career_profile_analyst_agent.model)
    print("✓ Output Key:", career_profile_analyst_agent.output_key)
    print("✓ Description:", career_profile_analyst_agent.description[:100] + "...")
    print()
    
    # Verify model upgrade
    expected_model = "gemini-3-pro-preview"
    if career_profile_analyst_agent.model == expected_model:
        print(f"✅ SUCCESS: Model upgraded to {expected_model}")
    else:
        print(f"❌ FAILED: Expected {expected_model}, got {career_profile_analyst_agent.model}")
        return False
    
    # Verify output key
    if career_profile_analyst_agent.output_key == "career_profile_output":
        print("✅ SUCCESS: Output key correctly configured")
    else:
        print(f"❌ FAILED: Output key is {career_profile_analyst_agent.output_key}")
        return False
    
    # Verify description mentions Gemini 3 Pro
    if "gemini 3 pro" in career_profile_analyst_agent.description.lower():
        print("✅ SUCCESS: Description mentions Gemini 3 Pro capabilities")
    else:
        print("⚠️  WARNING: Description doesn't mention Gemini 3 Pro")
    
    print()
    return True


def verify_managing_coordinator_integration():
    """Verify Managing Coordinator has access to upgraded Career Profile Analyst."""
    print("=" * 70)
    print("Managing Coordinator Integration Verification")
    print("=" * 70)
    print()
    
    print("✓ Coordinator Model:", managing_coordinator.model)
    print("✓ Number of Specialist Tools:", len(managing_coordinator.tools))
    print()
    
    # Check if Career Profile Analyst is in the tools
    specialist_names = []
    for tool in managing_coordinator.tools:
        if hasattr(tool, 'agent'):
            specialist_names.append(tool.agent.name)
    
    print("✓ Available Specialists:")
    for name in specialist_names:
        print(f"  - {name}")
    print()
    
    if "career_profile_analyst" in specialist_names:
        print("✅ SUCCESS: Career Profile Analyst is available to Managing Coordinator")
    else:
        print("❌ FAILED: Career Profile Analyst not found in Managing Coordinator tools")
        return False
    
    # Verify coordinator is also using Gemini 3 Pro
    if managing_coordinator.model == "gemini-3-pro-preview":
        print("✅ SUCCESS: Managing Coordinator also using Gemini 3 Pro")
    else:
        print(f"⚠️  INFO: Managing Coordinator using {managing_coordinator.model}")
    
    print()
    return True


def main():
    """Run all verification checks."""
    print()
    print("🔍 Starting Gemini 3 Pro Upgrade Verification")
    print()
    
    analyst_ok = verify_career_profile_analyst()
    coordinator_ok = verify_managing_coordinator_integration()
    
    print("=" * 70)
    print("Verification Summary")
    print("=" * 70)
    print()
    
    if analyst_ok and coordinator_ok:
        print("✅ ALL CHECKS PASSED")
        print()
        print("The Career Profile Analyst has been successfully upgraded to")
        print("Gemini 3 Pro (gemini-3-pro-preview) and is properly integrated")
        print("with the Managing Coordinator.")
        print()
        print("Key Features:")
        print("  • Advanced reasoning capabilities for deep career analysis")
        print("  • Configured for high thinking level (when ADK supports it)")
        print("  • Automatic Thought Signature handling via ADK")
        print("  • Compatible with Managing Coordinator interface")
        print()
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print()
        print("Please review the errors above and ensure the upgrade was")
        print("completed correctly.")
        print()
        return 1


if __name__ == "__main__":
    exit(main())
