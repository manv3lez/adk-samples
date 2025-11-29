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

"""Example demonstrating user interaction features in the Job Hunter Agent.

This module provides examples of how the Career Coordinator implements
user interaction features including:
- Workflow stage explanations (Requirement 9.1)
- Sub-agent activity notifications (Requirement 9.2)
- Markdown formatting for results (Requirement 9.3)
- Help/explanation system (Requirement 9.4)
- AI disclaimer inclusion (Requirement 10.4)
"""

from typing import Dict, Any

try:
    from .utils.markdown_formatter import (
        format_career_profile,
        format_job_opportunities,
        format_application_materials,
        add_ai_disclaimer,
    )
except ImportError:
    # For running as a standalone script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from utils.markdown_formatter import (
        format_career_profile,
        format_job_opportunities,
        format_application_materials,
        add_ai_disclaimer,
    )


# Example 1: Workflow Stage Explanation (Requirement 9.1)
def example_workflow_stage_explanation():
    """Demonstrate how to explain workflow stages to users."""
    
    # At the start of Career Profile Analysis stage
    stage_explanation = """
    📋 **Entering: Career Profile Analysis Stage**
    
    **What will happen**: I'll work with the Career Profile Analyst to analyze your 
    background, skills, and experience to create a comprehensive career profile.
    
    **What I need from you**: 
    - Your resume or work history
    - Skills and qualifications
    - Education background
    - Career goals and preferences (target roles, industries, locations)
    
    **Time estimate**: 2-3 minutes
    
    **Why this matters**: This analysis will help us identify your strengths, find skills 
    gaps, and discover the best job opportunities that match your profile.
    
    Ready to begin? Please share your background information.
    """
    
    return stage_explanation


# Example 2: Sub-Agent Activity Notifications (Requirement 9.2)
def example_sub_agent_notifications():
    """Demonstrate how to notify users about sub-agent activities."""
    
    notifications = {
        "before_activation": """
        🔄 **Activating: Career Profile Analyst**
        
        This specialized agent will analyze your background and create a comprehensive 
        career profile including your strengths, skills categorization, and development 
        recommendations.
        """,
        
        "during_processing": """
        ⏳ **In Progress**: The Career Profile Analyst is currently:
        - Extracting and categorizing your skills
        - Analyzing your experience and achievements
        - Identifying your top strengths
        - Finding skills gaps and opportunities
        - Generating personalized recommendations
        
        This may take a moment...
        """,
        
        "after_completion": """
        ✅ **Completed**: Career Profile Analysis
        
        Great news! I've completed your career profile analysis. Here's what I found:
        
        - **Top Strengths**: Leadership, Cloud Architecture, Agile Methodologies
        - **Skills Gaps**: Kubernetes, Machine Learning (recommendations provided)
        - **Career Fit**: Strong match for Senior Engineering roles
        
        Would you like me to show you the detailed results as markdown?
        """
    }
    
    return notifications


# Example 3: Markdown Formatting (Requirement 9.3)
def example_markdown_formatting():
    """Demonstrate markdown formatting for different types of results."""
    
    # Example career profile data
    sample_profile = {
        "profile_summary": {
            "name": "John Doe",
            "professional_summary": "Experienced software engineer with 8+ years in cloud architecture",
            "years_of_experience": 8,
            "current_level": "Senior"
        },
        "skills": {
            "technical": [
                {"skill": "Python", "proficiency": "Expert"},
                {"skill": "AWS", "proficiency": "Advanced"},
                {"skill": "Docker", "proficiency": "Advanced"}
            ],
            "soft": [
                {"skill": "Leadership", "proficiency": "Advanced"},
                {"skill": "Communication", "proficiency": "Expert"}
            ]
        },
        "strengths": [
            {
                "strength": "Technical Leadership",
                "description": "Proven ability to lead engineering teams",
                "evidence": "Led team of 10 engineers for 3 years"
            }
        ]
    }
    
    # Format as markdown
    formatted_profile = format_career_profile(sample_profile)
    
    return formatted_profile


# Example 4: Help and Explanation System (Requirement 9.4)
def example_help_system():
    """Demonstrate the help and explanation system."""
    
    help_responses = {
        "what_is_ats": """
        **What is ATS?**
        
        ATS stands for Applicant Tracking System. It's software that companies use to 
        automatically screen and filter resumes before a human recruiter sees them.
        
        **Why it matters**: Many qualified candidates get rejected because their resume 
        doesn't have the right keywords or formatting, even though they have the skills!
        
        **How we help**: We optimize your resume to include the right keywords from the 
        job description and use ATS-friendly formatting so your application gets through 
        to human reviewers.
        """,
        
        "how_match_scores_work": """
        **How Match Scores Work**
        
        We calculate a match score (0-100%) for each job opportunity based on:
        
        1. **Skills Alignment (40%)**: How many required skills you have
        2. **Experience Match (25%)**: Does your experience level fit the role?
        3. **Career Goals (20%)**: Does this match your target role/industry?
        4. **Location/Work (10%)**: Does it match your preferences?
        5. **Salary Fit (5%)**: Does it meet your expectations?
        
        A score of 80%+ means you're a strong match. 60-79% is moderate. Below 60% 
        might be a stretch but could still be worth applying if you're interested!
        """,
        
        "workflow_stages": """
        **Job Hunting Workflow Stages**
        
        I guide you through these stages:
        
        1. **Career Profile Analysis**: Analyze your background and skills
        2. **Job Market Research**: Find relevant job opportunities
        3. **Application Materials**: Create tailored resumes and cover letters
        4. **Interview Preparation**: Prepare for interviews with practice questions
        5. **Career Strategy** (Optional): Long-term career planning
        
        We can move through these in order, or jump to a specific stage if you prefer!
        """
    }
    
    return help_responses


# Example 5: AI Disclaimer Inclusion (Requirement 10.4)
def example_ai_disclaimers():
    """Demonstrate AI disclaimer inclusion in various contexts."""
    
    disclaimers = {
        "session_start": """
        ⚠️ **Important Disclaimer: For Guidance and Informational Purposes Only**
        
        The career guidance, application materials, and interview preparation provided 
        by this tool are generated by an AI model and are for informational purposes only. 
        They do not constitute professional career counseling or guarantee job placement.
        
        All generated materials should be reviewed, personalized, and verified by you 
        before use. You should ensure all application materials authentically represent 
        your actual experience and qualifications.
        
        By using this tool, you acknowledge that the developers and contributors are not 
        liable for any outcomes arising from your use of this information.
        """,
        
        "after_resume_generation": """
        ⚠️ **Important Reminder**: This resume is AI-generated based on your information. 
        Please review carefully, personalize the content, and ensure everything accurately 
        represents your actual experience and qualifications before submitting any applications.
        """,
        
        "after_interview_prep": """
        ⚠️ **Remember**: These interview responses are AI-generated examples. Personalize 
        them with your own experiences and ensure they authentically represent your work 
        and achievements.
        """,
        
        "general_guidance": """
        💡 **Tip**: Always review and customize AI-generated content to match your authentic 
        voice and experience. Recruiters can tell when content is generic or not personalized!
        """
    }
    
    return disclaimers


# Example 6: Complete User Interaction Flow
def example_complete_interaction_flow():
    """Demonstrate a complete user interaction flow with all features."""
    
    flow = """
    # Complete User Interaction Example
    
    ## 1. Session Start
    
    **Career Coordinator**: Hello! I'm your Career Coordinator, here to guide you through 
    your job hunting journey. My goal is to provide comprehensive career assistance by 
    working with you step-by-step.
    
    Together, we'll analyze your background and skills, research relevant job opportunities,
    create tailored application materials optimized for ATS systems, and prepare you for 
    interviews.
    
    At each step, you can ask to 'show me the detailed result as markdown' for better readability.
    
    Ready to get started?
    
    ⚠️ **Important Disclaimer**: [Full disclaimer text...]
    
    ---
    
    ## 2. Workflow Stage Explanation
    
    **Career Coordinator**: Great! Let's begin with the Career Profile Analysis stage.
    
    📋 **Entering: Career Profile Analysis Stage**
    
    **What will happen**: I'll analyze your background, skills, and experience.
    **What I need**: Your resume, skills, and career goals.
    **Time estimate**: 2-3 minutes
    **Why this matters**: This helps us find the best job opportunities for you.
    
    Please share your background information.
    
    ---
    
    ## 3. Sub-Agent Activation Notification
    
    **User**: [Provides background information]
    
    **Career Coordinator**: Thank you! 
    
    🔄 **Activating: Career Profile Analyst**
    
    This specialized agent will analyze your background and create a comprehensive career 
    profile including your strengths, skills categorization, and development recommendations.
    
    ⏳ **In Progress**: Analyzing your profile...
    
    ---
    
    ## 4. Completion and Results Offer
    
    **Career Coordinator**: 
    
    ✅ **Completed**: Career Profile Analysis
    
    Great news! I've completed your career profile analysis. Here's a quick summary:
    
    - **Top Strengths**: Technical Leadership, Cloud Architecture, Agile Methodologies
    - **Skills Gaps**: Kubernetes, Machine Learning (recommendations provided)
    - **Career Fit**: Strong match for Senior Engineering roles
    
    Would you like me to show you the detailed results as markdown?
    
    ---
    
    ## 5. Markdown Formatted Results
    
    **User**: Yes, show me the detailed results as markdown
    
    **Career Coordinator**: Here's your complete career profile analysis:
    
    [Formatted markdown output with proper headings, bullets, and structure]
    
    ⚠️ **Remember**: Review these insights and let me know if anything needs adjustment.
    
    ---
    
    ## 6. Help Request
    
    **User**: What is ATS and why does it matter?
    
    **Career Coordinator**: Great question! Let me explain:
    
    **What is ATS?**
    
    ATS stands for Applicant Tracking System. It's software that companies use to 
    automatically screen resumes before a human sees them.
    
    [Full explanation...]
    
    Does that help clarify? Feel free to ask if you have more questions!
    
    ---
    
    ## 7. Next Stage Transition
    
    **Career Coordinator**: Now that we have your career profile, would you like to move 
    to the next stage: Job Market Research?
    
    In this stage, I'll search multiple job boards and company sites to find opportunities 
    that match your profile. This typically takes 3-5 minutes.
    
    Ready to proceed?
    """
    
    return flow


# Example 7: Error Handling with User-Friendly Messages
def example_error_handling():
    """Demonstrate user-friendly error handling."""
    
    error_examples = {
        "missing_profile": """
        ⚠️ **Oops! Missing Information**
        
        I need your career profile before I can search for job opportunities. 
        
        **What to do next**:
        1. Let's start with the Career Profile Analysis
        2. Share your resume or background information
        3. Tell me about your career goals
        
        Once we have your profile, I can find the perfect job opportunities for you!
        """,
        
        "search_service_down": """
        ⚠️ **Temporary Service Issue**
        
        I'm having trouble connecting to the job search service right now. This is 
        usually temporary and should be resolved soon.
        
        **What you can do**:
        1. Wait a few minutes and try again
        2. Manually search on LinkedIn or Indeed in the meantime
        3. Let me know when you'd like to retry
        
        I was able to find 3 opportunities before the connection issue. Would you like 
        to see those while we wait?
        """,
        
        "incomplete_job_description": """
        ⚠️ **Need More Information**
        
        The job description you provided is missing some key details I need to create 
        the best application materials.
        
        **What's missing**:
        - Required qualifications
        - Key responsibilities
        - Company information
        
        **What to do**:
        1. Check the job posting for these details
        2. Provide the complete job description
        3. Or, I can create a general resume with what we have
        
        Which would you prefer?
        """
    }
    
    return error_examples


if __name__ == "__main__":
    # Print examples
    print("=" * 80)
    print("USER INTERACTION FEATURES EXAMPLES")
    print("=" * 80)
    
    print("\n1. WORKFLOW STAGE EXPLANATION")
    print("-" * 80)
    print(example_workflow_stage_explanation())
    
    print("\n2. SUB-AGENT NOTIFICATIONS")
    print("-" * 80)
    notifications = example_sub_agent_notifications()
    for key, value in notifications.items():
        print(f"\n{key.upper()}:")
        print(value)
    
    print("\n3. MARKDOWN FORMATTING")
    print("-" * 80)
    print(example_markdown_formatting())
    
    print("\n4. HELP SYSTEM")
    print("-" * 80)
    help_responses = example_help_system()
    for key, value in help_responses.items():
        print(f"\n{key.upper()}:")
        print(value)
    
    print("\n5. AI DISCLAIMERS")
    print("-" * 80)
    disclaimers = example_ai_disclaimers()
    for key, value in disclaimers.items():
        print(f"\n{key.upper()}:")
        print(value)
