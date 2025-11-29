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

"""Markdown formatting utilities for user-friendly output presentation.

This module provides utilities to format various types of job hunting data
into readable markdown format for better user experience.
"""

from typing import Any, Dict, List


def format_career_profile(profile: Dict[str, Any]) -> str:
    """Format career profile analysis as markdown.
    
    Args:
        profile: Career profile dictionary from Career Profile Analyst
        
    Returns:
        Formatted markdown string
    """
    md = "# Career Profile Analysis\n\n"
    
    # Profile Summary
    if "profile_summary" in profile:
        summary = profile["profile_summary"]
        md += "## Professional Summary\n\n"
        md += f"**Name**: {summary.get('name', 'Job Seeker')}\n\n"
        md += f"{summary.get('professional_summary', '')}\n\n"
        md += f"- **Experience Level**: {summary.get('current_level', 'N/A')}\n"
        md += f"- **Years of Experience**: {summary.get('years_of_experience', 'N/A')}\n\n"
    
    # Skills
    if "skills" in profile:
        md += "## Skills\n\n"
        skills = profile["skills"]
        
        if "technical" in skills and skills["technical"]:
            md += "### Technical Skills\n"
            for skill in skills["technical"][:10]:  # Limit to top 10
                if isinstance(skill, dict):
                    md += f"- **{skill.get('skill', '')}** ({skill.get('proficiency', 'N/A')})\n"
                else:
                    md += f"- {skill}\n"
            md += "\n"
        
        if "soft" in skills and skills["soft"]:
            md += "### Soft Skills\n"
            for skill in skills["soft"][:10]:
                if isinstance(skill, dict):
                    md += f"- **{skill.get('skill', '')}** ({skill.get('proficiency', 'N/A')})\n"
                else:
                    md += f"- {skill}\n"
            md += "\n"
    
    # Strengths
    if "strengths" in profile and profile["strengths"]:
        md += "## Top Strengths\n\n"
        for i, strength in enumerate(profile["strengths"][:5], 1):
            if isinstance(strength, dict):
                md += f"{i}. **{strength.get('strength', '')}**\n"
                md += f"   - {strength.get('description', '')}\n\n"
            else:
                md += f"{i}. {strength}\n\n"
    
    # Skills Gaps
    if "skills_gaps" in profile:
        gaps = profile["skills_gaps"]
        md += "## Skills Development Opportunities\n\n"
        
        if "critical_gaps" in gaps and gaps["critical_gaps"]:
            md += "### High Priority\n"
            for gap in gaps["critical_gaps"][:5]:
                if isinstance(gap, dict):
                    md += f"- **{gap.get('skill', '')}**: {gap.get('importance', '')}\n"
                else:
                    md += f"- {gap}\n"
            md += "\n"
    
    # Recommendations
    if "recommendations" in profile and profile["recommendations"]:
        md += "## Recommendations\n\n"
        for rec in profile["recommendations"][:5]:
            if isinstance(rec, dict):
                priority = rec.get('priority', 'Medium')
                md += f"### {priority} Priority: {rec.get('recommendation', '')}\n"
                md += f"{rec.get('rationale', '')}\n\n"
            else:
                md += f"- {rec}\n\n"
    
    return md


def format_job_opportunities(opportunities: Dict[str, Any]) -> str:
    """Format job opportunities list as markdown.
    
    Args:
        opportunities: Job opportunities dictionary from Job Market Researcher
        
    Returns:
        Formatted markdown string
    """
    md = "# Job Opportunities\n\n"
    
    # Search Summary
    if "search_summary" in opportunities:
        summary = opportunities["search_summary"]
        md += "## Search Summary\n\n"
        md += f"- **Total Opportunities Found**: {summary.get('total_opportunities_found', 0)}\n"
        md += f"- **Sources Searched**: {', '.join(summary.get('sources_searched', []))}\n"
        md += f"- **Search Date**: {summary.get('search_date', 'N/A')}\n\n"
    
    # Top Opportunities
    if "top_opportunities" in opportunities and opportunities["top_opportunities"]:
        md += "## Top Matches\n\n"
        for opp in opportunities["top_opportunities"][:10]:
            md += f"### {opp.get('rank', '')}. {opp.get('job_title', 'N/A')} at {opp.get('company', 'N/A')}\n\n"
            md += f"**Match Score**: {opp.get('match_analysis', {}).get('overall_match_score', 0):.1f}%\n\n"
            md += f"- **Location**: {opp.get('location', 'N/A')}\n"
            md += f"- **Work Arrangement**: {opp.get('work_arrangement', 'N/A')}\n"
            
            if "compensation" in opp:
                comp = opp["compensation"]
                md += f"- **Salary Range**: {comp.get('salary_range', 'Not disclosed')}\n"
            
            md += f"- **Job URL**: {opp.get('job_url', 'N/A')}\n\n"
            
            # Job Summary
            if "job_summary" in opp:
                md += f"**About the Role**: {opp['job_summary']}\n\n"
            
            # Match Analysis
            if "match_analysis" in opp:
                match = opp["match_analysis"]
                md += "**Why This Matches**:\n"
                if "matching_skills" in match and match["matching_skills"]:
                    md += f"- Matching Skills: {', '.join(match['matching_skills'][:5])}\n"
                if "strengths_for_role" in match and match["strengths_for_role"]:
                    md += f"- Your Strengths: {', '.join(match['strengths_for_role'][:3])}\n"
                md += "\n"
            
            md += "---\n\n"
    
    return md


def format_application_materials(materials: Dict[str, Any]) -> str:
    """Format application materials as markdown.
    
    Args:
        materials: Application materials dictionary from Application Strategist
        
    Returns:
        Formatted markdown string
    """
    md = "# Application Materials\n\n"
    
    # Job Info
    if "job_info" in materials:
        job = materials["job_info"]
        md += f"**Position**: {job.get('job_title', 'N/A')} at {job.get('company', 'N/A')}\n\n"
    
    # ATS Analysis
    if "ats_analysis" in materials:
        ats = materials["ats_analysis"]
        md += "## ATS Match Analysis\n\n"
        md += f"**Overall Match Score**: {ats.get('overall_match_score', 0):.1f}%\n\n"
        
        if "keyword_analysis" in ats:
            ka = ats["keyword_analysis"]
            md += "### Keyword Coverage\n\n"
            
            if "required_keywords" in ka:
                req = ka["required_keywords"]
                md += f"- **Required Keywords**: {req.get('found', 0)}/{req.get('total', 0)} found\n"
            
            if "preferred_keywords" in ka:
                pref = ka["preferred_keywords"]
                md += f"- **Preferred Keywords**: {pref.get('found', 0)}/{pref.get('total', 0)} found\n"
            
            md += "\n"
    
    # Resume
    if "resume" in materials and "content" in materials["resume"]:
        md += "## Resume\n\n"
        md += "```\n"
        md += materials["resume"]["content"]
        md += "\n```\n\n"
    
    # Cover Letter
    if "cover_letter" in materials and "content" in materials["cover_letter"]:
        md += "## Cover Letter\n\n"
        md += "```\n"
        md += materials["cover_letter"]["content"]
        md += "\n```\n\n"
    
    # Optimization Recommendations
    if "optimization_recommendations" in materials and materials["optimization_recommendations"]:
        md += "## Optimization Recommendations\n\n"
        for rec in materials["optimization_recommendations"][:5]:
            if isinstance(rec, dict):
                md += f"### {rec.get('priority', 'Medium')} Priority\n"
                md += f"**{rec.get('recommendation', '')}**\n\n"
                md += f"{rec.get('rationale', '')}\n\n"
                if "example" in rec:
                    md += f"*Example*: {rec['example']}\n\n"
    
    # AI Disclaimer
    md += "\n---\n\n"
    md += "⚠️ **Important Reminder**: These materials are AI-generated based on your information. "
    md += "Please review carefully, personalize the content, and ensure everything accurately represents "
    md += "your actual experience and qualifications before submitting any applications.\n"
    
    return md


def format_interview_prep(prep: Dict[str, Any]) -> str:
    """Format interview preparation guide as markdown.
    
    Args:
        prep: Interview prep dictionary from Interview Coach
        
    Returns:
        Formatted markdown string
    """
    md = "# Interview Preparation Guide\n\n"
    
    # Company Research
    if "company_research" in prep:
        md += "## Company Research\n\n"
        research = prep["company_research"]
        for key, value in research.items():
            if isinstance(value, str):
                md += f"**{key.replace('_', ' ').title()}**: {value}\n\n"
    
    # Behavioral Questions
    if "behavioral_questions" in prep and prep["behavioral_questions"]:
        md += "## Behavioral Interview Questions\n\n"
        for i, q in enumerate(prep["behavioral_questions"][:10], 1):
            md += f"{i}. {q}\n"
        md += "\n"
    
    # Technical Questions
    if "technical_questions" in prep and prep["technical_questions"]:
        md += "## Technical Interview Questions\n\n"
        for i, q in enumerate(prep["technical_questions"][:10], 1):
            md += f"{i}. {q}\n"
        md += "\n"
    
    # STAR Examples
    if "star_examples" in prep and prep["star_examples"]:
        md += "## STAR Method Examples\n\n"
        for example in prep["star_examples"][:5]:
            if isinstance(example, dict):
                md += f"### {example.get('situation', 'Example')}\n\n"
                md += f"- **Situation**: {example.get('situation', '')}\n"
                md += f"- **Task**: {example.get('task', '')}\n"
                md += f"- **Action**: {example.get('action', '')}\n"
                md += f"- **Result**: {example.get('result', '')}\n\n"
    
    # Study Topics
    if "study_topics" in prep and prep["study_topics"]:
        md += "## Study Topics\n\n"
        for topic in prep["study_topics"][:10]:
            md += f"- {topic}\n"
        md += "\n"
    
    # Tips
    if "tips" in prep and prep["tips"]:
        md += "## Interview Tips\n\n"
        for tip in prep["tips"][:10]:
            md += f"- {tip}\n"
        md += "\n"
    
    return md


def add_ai_disclaimer(content: str) -> str:
    """Add AI disclaimer to any content.
    
    Args:
        content: The content to add disclaimer to
        
    Returns:
        Content with disclaimer appended
    """
    disclaimer = (
        "\n\n---\n\n"
        "⚠️ **Important Reminder**: This content is AI-generated. "
        "Please review carefully, personalize it, and ensure it accurately represents "
        "your actual experience and qualifications.\n"
    )
    return content + disclaimer
