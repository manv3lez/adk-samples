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

"""Example demonstrating state management integration with Job Hunter Agent.

This module shows how the state management system integrates with the agent workflow.
It's provided as documentation and for testing purposes.
"""

try:
    from .state_manager import StateManager, get_state_manager
except ImportError:
    from state_manager import StateManager, get_state_manager


def example_workflow():
    """Example workflow demonstrating state management across sub-agents."""
    
    # Get the state manager
    state_manager = get_state_manager()
    
    # Simulate Career Profile Analyst output
    career_profile = {
        "skills": {
            "technical": ["Python", "Java", "SQL"],
            "soft": ["Communication", "Leadership"],
            "domain": ["Software Development", "Data Analysis"]
        },
        "experience": {
            "years": 5,
            "roles": ["Software Engineer", "Senior Developer"],
            "industries": ["Tech", "Finance"]
        },
        "strengths": ["Full-stack development", "Problem solving"],
        "gaps": ["Cloud architecture", "Machine learning"],
        "recommendations": ["Learn AWS", "Take ML course"],
        "career_goals": {
            "target_role": "Senior Software Engineer",
            "target_industry": "Tech",
            "location": "Remote"
        }
    }
    
    # Store career profile (Requirement 6.1)
    state_manager.store_state(
        "career_profile_output",
        career_profile,
        metadata={"source": "career_profile_analyst"}
    )
    
    print("✓ Career profile stored")
    
    # Simulate Job Market Researcher retrieving the profile (Requirement 6.2)
    retrieved_profile = state_manager.retrieve_state("career_profile_output")
    print(f"✓ Job Market Researcher retrieved profile with {len(retrieved_profile['skills']['technical'])} technical skills")
    
    # Simulate Job Market Researcher output
    job_opportunities = {
        "opportunities": [
            {
                "job_title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "requirements": ["Python", "Java", "5+ years"],
                "match_score": 0.92,
                "salary_range": "$120k-$150k",
                "company_culture": "Innovative, collaborative",
                "url": "https://example.com/job1"
            },
            {
                "job_title": "Lead Developer",
                "company": "StartupXYZ",
                "location": "Remote",
                "requirements": ["Python", "SQL", "Leadership"],
                "match_score": 0.88,
                "salary_range": "$130k-$160k",
                "company_culture": "Fast-paced, entrepreneurial",
                "url": "https://example.com/job2"
            }
        ]
    }
    
    state_manager.store_state(
        "job_opportunities_output",
        job_opportunities,
        metadata={"source": "job_market_researcher"}
    )
    
    print(f"✓ Found {len(job_opportunities['opportunities'])} job opportunities")
    
    # Demonstrate multi-application state isolation (Requirement 6.4)
    # User decides to apply to both jobs
    
    # Application 1: Tech Corp
    app1_materials = {
        "resume": "Tailored resume for Tech Corp...",
        "cover_letter": "Dear Tech Corp hiring manager...",
        "ats_analysis": {
            "match_score": 0.92,
            "required_keywords": ["Python", "Java", "Agile"],
            "found_keywords": ["Python", "Java", "Agile"],
            "missing_keywords": [],
            "recommendations": ["Great match!"]
        }
    }
    
    state_manager.store_state(
        "application_materials_output",
        app1_materials,
        application_id="tech_corp_senior_engineer",
        metadata={"company": "Tech Corp", "position": "Senior Software Engineer"}
    )
    
    # Application 2: StartupXYZ
    app2_materials = {
        "resume": "Tailored resume for StartupXYZ...",
        "cover_letter": "Dear StartupXYZ team...",
        "ats_analysis": {
            "match_score": 0.88,
            "required_keywords": ["Python", "SQL", "Leadership"],
            "found_keywords": ["Python", "SQL", "Leadership"],
            "missing_keywords": [],
            "recommendations": ["Excellent fit!"]
        }
    }
    
    state_manager.store_state(
        "application_materials_output",
        app2_materials,
        application_id="startupxyz_lead_developer",
        metadata={"company": "StartupXYZ", "position": "Lead Developer"}
    )
    
    print("✓ Created application materials for 2 positions")
    
    # Verify state isolation
    app1_retrieved = state_manager.retrieve_state(
        "application_materials_output",
        application_id="tech_corp_senior_engineer"
    )
    app2_retrieved = state_manager.retrieve_state(
        "application_materials_output",
        application_id="startupxyz_lead_developer"
    )
    
    assert app1_retrieved["ats_analysis"]["match_score"] == 0.92
    assert app2_retrieved["ats_analysis"]["match_score"] == 0.88
    print("✓ Verified state isolation between applications")
    
    # List all applications (Requirement 6.4)
    applications = state_manager.list_applications()
    print(f"✓ Managing {len(applications)} concurrent applications")
    
    # Demonstrate state update with notification (Requirement 6.3)
    notifications_received = []
    
    def profile_update_listener(key, value, application_id):
        notifications_received.append({
            "key": key,
            "updated_skills": len(value.get("skills", {}).get("technical", []))
        })
    
    state_manager.register_listener("career_profile_output", profile_update_listener)
    
    # User adds a new skill
    updated_profile = career_profile.copy()
    updated_profile["skills"]["technical"].append("AWS")
    updated_profile["gaps"].remove("Cloud architecture")
    
    state_manager.update_state("career_profile_output", updated_profile)
    
    assert len(notifications_received) == 1
    print("✓ Profile updated and listeners notified")
    
    # Demonstrate session persistence (Requirement 6.5)
    session_data = state_manager.save_session()
    print(f"✓ Session saved with {len(session_data['application_states'])} applications")
    
    # Simulate restoring session
    new_manager = StateManager()
    new_manager.restore_session(session_data)
    
    restored_profile = new_manager.retrieve_state("career_profile_output")
    assert "AWS" in restored_profile["skills"]["technical"]
    print("✓ Session restored successfully")
    
    print("\n✅ All state management requirements demonstrated successfully!")


if __name__ == "__main__":
    example_workflow()
