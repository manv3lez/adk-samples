"""ATS Keyword Analyzer utility for optimizing resumes against job descriptions.

This module provides functionality to:
- Extract keywords from job descriptions
- Categorize keywords (required, preferred, technical)
- Match resume content against job requirements
- Calculate ATS match scores
- Identify missing keywords
- Generate optimization recommendations
"""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter


class ATSKeywordAnalyzer:
    """Analyzes job descriptions and resumes for ATS optimization."""
    
    # Common technical skill patterns
    TECHNICAL_PATTERNS = [
        r'\b[A-Z][a-z]+(?:\.[a-z]+)+\b',  # e.g., Node.js, React.js
        r'\b[A-Z]{2,}\b',  # Acronyms like SQL, AWS, API
        r'\b\w+\+\+\b',  # C++, etc.
        r'\b[A-Z][a-z]+[A-Z]\w*\b',  # CamelCase like JavaScript, TypeScript
    ]
    
    # Keywords that indicate requirements
    REQUIRED_INDICATORS = [
        'required', 'must have', 'must be', 'essential', 'mandatory',
        'necessary', 'need', 'needs', 'require', 'requires'
    ]
    
    # Keywords that indicate preferences
    PREFERRED_INDICATORS = [
        'preferred', 'nice to have', 'bonus', 'plus', 'desirable',
        'ideal', 'advantage', 'beneficial', 'would be great'
    ]
    
    # Common stop words to exclude
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them',
        'their', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
    }
    
    def extract_keywords(self, job_description: str) -> Dict[str, List[str]]:
        """Extract and categorize keywords from a job description.
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary with 'required_keywords', 'preferred_keywords', and 'technical_terms'
        """
        if not job_description or not job_description.strip():
            return {
                'required_keywords': [],
                'preferred_keywords': [],
                'technical_terms': []
            }
        
        # Extract technical terms first
        technical_terms = self._extract_technical_terms(job_description)
        
        # Split into sections based on requirement indicators
        required_keywords = self._extract_keywords_by_context(
            job_description, self.REQUIRED_INDICATORS
        )
        
        preferred_keywords = self._extract_keywords_by_context(
            job_description, self.PREFERRED_INDICATORS
        )
        
        # Remove duplicates and clean up
        required_keywords = list(set(required_keywords) - set(technical_terms))
        preferred_keywords = list(set(preferred_keywords) - set(technical_terms) - set(required_keywords))
        
        return {
            'required_keywords': sorted(required_keywords),
            'preferred_keywords': sorted(preferred_keywords),
            'technical_terms': sorted(list(technical_terms))
        }
    
    def _extract_technical_terms(self, text: str) -> Set[str]:
        """Extract technical terms using pattern matching."""
        technical_terms = set()
        
        for pattern in self.TECHNICAL_PATTERNS:
            matches = re.findall(pattern, text)
            technical_terms.update(matches)
        
        # Also look for common technical terms in word boundaries
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            # Check if it's a known technical term (has numbers, special chars, or is all caps)
            if (re.search(r'\d', word) or 
                word.isupper() and len(word) > 1 or
                any(c in word for c in ['+', '#', '.'])):
                technical_terms.add(word)
        
        return technical_terms
    
    def _extract_keywords_by_context(self, text: str, indicators: List[str]) -> List[str]:
        """Extract keywords that appear near context indicators."""
        keywords = []
        text_lower = text.lower()
        
        for indicator in indicators:
            # Find sentences containing the indicator
            pattern = r'[^.!?]*' + re.escape(indicator) + r'[^.!?]*[.!?]'
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            
            for match in matches:
                # Extract meaningful words from the sentence
                words = re.findall(r'\b[a-z]+\b', match.lower())
                keywords.extend([w for w in words if w not in self.STOP_WORDS and len(w) > 2])
        
        return keywords
    
    def calculate_match_score(self, resume: str, job_description: str) -> Dict[str, any]:
        """Calculate how well a resume matches a job description.
        
        Args:
            resume: The resume text
            job_description: The job description text
            
        Returns:
            Dictionary containing match score and detailed analysis
        """
        if not resume or not resume.strip():
            return {
                'match_percentage': 0.0,
                'found_keywords': [],
                'missing_keywords': [],
                'total_keywords': 0
            }
        
        # Extract keywords from job description
        keywords = self.extract_keywords(job_description)
        
        # Combine all keywords for matching
        all_keywords = (
            keywords['required_keywords'] + 
            keywords['preferred_keywords'] + 
            keywords['technical_terms']
        )
        
        if not all_keywords:
            return {
                'match_percentage': 0.0,
                'found_keywords': [],
                'missing_keywords': [],
                'total_keywords': 0
            }
        
        # Find which keywords appear in the resume
        resume_lower = resume.lower()
        found_keywords = []
        missing_keywords = []
        
        for keyword in all_keywords:
            if keyword.lower() in resume_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate match percentage
        match_percentage = (len(found_keywords) / len(all_keywords)) * 100 if all_keywords else 0.0
        
        return {
            'match_percentage': round(match_percentage, 2),
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords,
            'total_keywords': len(all_keywords)
        }
    
    def identify_missing_keywords(self, resume: str, job_description: str) -> Dict[str, List[str]]:
        """Identify keywords missing from the resume.
        
        Args:
            resume: The resume text
            job_description: The job description text
            
        Returns:
            Dictionary categorizing missing keywords by type
        """
        keywords = self.extract_keywords(job_description)
        resume_lower = resume.lower()
        
        missing_required = [
            kw for kw in keywords['required_keywords'] 
            if kw.lower() not in resume_lower
        ]
        
        missing_preferred = [
            kw for kw in keywords['preferred_keywords']
            if kw.lower() not in resume_lower
        ]
        
        missing_technical = [
            kw for kw in keywords['technical_terms']
            if kw.lower() not in resume_lower
        ]
        
        return {
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'missing_technical': missing_technical
        }
    
    def generate_recommendations(self, resume: str, job_description: str) -> List[str]:
        """Generate optimization recommendations for the resume.
        
        Args:
            resume: The resume text
            job_description: The job description text
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        # Get missing keywords
        missing = self.identify_missing_keywords(resume, job_description)
        
        # Get match score
        match_info = self.calculate_match_score(resume, job_description)
        match_percentage = match_info['match_percentage']
        
        # Overall score recommendation
        if match_percentage < 50:
            recommendations.append(
                f"Your resume has a {match_percentage}% keyword match. "
                "Consider significantly revising your resume to better align with the job requirements."
            )
        elif match_percentage < 75:
            recommendations.append(
                f"Your resume has a {match_percentage}% keyword match. "
                "Adding more relevant keywords could improve your ATS score."
            )
        else:
            recommendations.append(
                f"Your resume has a strong {match_percentage}% keyword match. "
                "Minor optimizations could further improve your ATS score."
            )
        
        # Missing required keywords
        if missing['missing_required']:
            recommendations.append(
                f"Add these required keywords if you have relevant experience: "
                f"{', '.join(missing['missing_required'][:5])}"
            )
        
        # Missing technical terms
        if missing['missing_technical']:
            recommendations.append(
                f"Include these technical terms where applicable: "
                f"{', '.join(missing['missing_technical'][:5])}"
            )
        
        # Missing preferred keywords
        if missing['missing_preferred'] and match_percentage > 60:
            recommendations.append(
                f"Consider adding these preferred qualifications if relevant: "
                f"{', '.join(missing['missing_preferred'][:3])}"
            )
        
        # Keyword variation recommendation
        if match_percentage < 80:
            recommendations.append(
                "Use exact terms from the job description rather than synonyms to improve ATS matching."
            )
        
        # Formatting recommendation
        recommendations.append(
            "Ensure your resume uses standard section headings (Experience, Education, Skills) "
            "and avoid complex formatting that ATS systems may not parse correctly."
        )
        
        return recommendations
    
    def analyze(self, resume: str, job_description: str) -> Dict[str, any]:
        """Perform complete ATS analysis.
        
        Args:
            resume: The resume text
            job_description: The job description text
            
        Returns:
            Complete analysis including keywords, match score, and recommendations
        """
        keywords = self.extract_keywords(job_description)
        match_info = self.calculate_match_score(resume, job_description)
        missing = self.identify_missing_keywords(resume, job_description)
        recommendations = self.generate_recommendations(resume, job_description)
        
        return {
            'keywords': keywords,
            'match_score': match_info['match_percentage'],
            'found_keywords': match_info['found_keywords'],
            'missing_keywords': missing,
            'total_keywords': match_info['total_keywords'],
            'recommendations': recommendations
        }
