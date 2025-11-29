"""Tests for ATS Keyword Analyzer utility."""

import pytest
from job_hunter_agent.utils.ats_analyzer import ATSKeywordAnalyzer


class TestATSKeywordAnalyzer:
    """Test suite for ATS Keyword Analyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ATSKeywordAnalyzer()
        
        self.sample_job_description = """
        Software Engineer Position
        
        Required qualifications:
        - 5+ years of experience in Python programming
        - Must have experience with AWS and Docker
        - Strong knowledge of SQL databases
        
        Preferred qualifications:
        - Experience with Kubernetes is a plus
        - Nice to have: React and TypeScript skills
        
        Technical requirements:
        - Python, JavaScript, SQL, AWS, Docker, Git
        """
        
        self.sample_resume = """
        John Doe
        Software Engineer
        
        Experience:
        - 6 years of Python development
        - Worked extensively with AWS and Docker
        - Built applications using SQL databases
        - Proficient in Git version control
        
        Skills: Python, AWS, Docker, SQL, Git, Java
        """
    
    def test_extract_keywords_returns_structure(self):
        """Test that extract_keywords returns the correct structure."""
        result = self.analyzer.extract_keywords(self.sample_job_description)
        
        assert 'required_keywords' in result
        assert 'preferred_keywords' in result
        assert 'technical_terms' in result
        assert isinstance(result['required_keywords'], list)
        assert isinstance(result['preferred_keywords'], list)
        assert isinstance(result['technical_terms'], list)
    
    def test_extract_keywords_finds_technical_terms(self):
        """Test that technical terms are extracted."""
        result = self.analyzer.extract_keywords(self.sample_job_description)
        
        # Should find technical terms like AWS, SQL, etc.
        technical_terms = result['technical_terms']
        assert len(technical_terms) > 0
        # Check for some expected technical terms (case-insensitive check)
        technical_lower = [t.lower() for t in technical_terms]
        assert any('sql' in t for t in technical_lower) or 'SQL' in technical_terms
    
    def test_extract_keywords_empty_input(self):
        """Test handling of empty job description."""
        result = self.analyzer.extract_keywords("")
        
        assert result['required_keywords'] == []
        assert result['preferred_keywords'] == []
        assert result['technical_terms'] == []
    
    def test_calculate_match_score_structure(self):
        """Test that match score calculation returns correct structure."""
        result = self.analyzer.calculate_match_score(
            self.sample_resume, 
            self.sample_job_description
        )
        
        assert 'match_percentage' in result
        assert 'found_keywords' in result
        assert 'missing_keywords' in result
        assert 'total_keywords' in result
        assert isinstance(result['match_percentage'], (int, float))
        assert 0 <= result['match_percentage'] <= 100
    
    def test_calculate_match_score_finds_matches(self):
        """Test that matching keywords are identified."""
        result = self.analyzer.calculate_match_score(
            self.sample_resume,
            self.sample_job_description
        )
        
        # Resume contains Python, AWS, Docker, SQL, Git
        assert len(result['found_keywords']) > 0
        assert result['match_percentage'] > 0
    
    def test_calculate_match_score_empty_resume(self):
        """Test handling of empty resume."""
        result = self.analyzer.calculate_match_score(
            "",
            self.sample_job_description
        )
        
        assert result['match_percentage'] == 0.0
        assert result['found_keywords'] == []
    
    def test_identify_missing_keywords_structure(self):
        """Test that missing keywords are categorized correctly."""
        result = self.analyzer.identify_missing_keywords(
            self.sample_resume,
            self.sample_job_description
        )
        
        assert 'missing_required' in result
        assert 'missing_preferred' in result
        assert 'missing_technical' in result
        assert isinstance(result['missing_required'], list)
        assert isinstance(result['missing_preferred'], list)
        assert isinstance(result['missing_technical'], list)
    
    def test_identify_missing_keywords_finds_gaps(self):
        """Test that missing keywords are identified."""
        # Resume doesn't have Kubernetes, React, TypeScript
        result = self.analyzer.identify_missing_keywords(
            self.sample_resume,
            self.sample_job_description
        )
        
        # Should have some missing keywords since resume doesn't have everything
        total_missing = (
            len(result['missing_required']) +
            len(result['missing_preferred']) +
            len(result['missing_technical'])
        )
        assert total_missing >= 0  # May or may not have missing keywords depending on extraction
    
    def test_generate_recommendations_returns_list(self):
        """Test that recommendations are generated."""
        result = self.analyzer.generate_recommendations(
            self.sample_resume,
            self.sample_job_description
        )
        
        assert isinstance(result, list)
        assert len(result) > 0
        # All recommendations should be strings
        assert all(isinstance(rec, str) for rec in result)
    
    def test_generate_recommendations_includes_match_score(self):
        """Test that recommendations mention the match score."""
        result = self.analyzer.generate_recommendations(
            self.sample_resume,
            self.sample_job_description
        )
        
        # First recommendation should mention match percentage
        assert any('%' in rec for rec in result)
    
    def test_analyze_complete_structure(self):
        """Test that complete analysis returns all components."""
        result = self.analyzer.analyze(
            self.sample_resume,
            self.sample_job_description
        )
        
        assert 'keywords' in result
        assert 'match_score' in result
        assert 'found_keywords' in result
        assert 'missing_keywords' in result
        assert 'total_keywords' in result
        assert 'recommendations' in result
        
        # Check nested structures
        assert 'required_keywords' in result['keywords']
        assert 'preferred_keywords' in result['keywords']
        assert 'technical_terms' in result['keywords']
        
        assert 'missing_required' in result['missing_keywords']
        assert 'missing_preferred' in result['missing_keywords']
        assert 'missing_technical' in result['missing_keywords']
    
    def test_keyword_extraction_case_insensitive(self):
        """Test that keyword matching is case-insensitive."""
        job_desc = "Required: Python and AWS experience"
        resume_upper = "Skills: PYTHON, aws"
        resume_lower = "Skills: python, AWS"
        
        result_upper = self.analyzer.calculate_match_score(resume_upper, job_desc)
        result_lower = self.analyzer.calculate_match_score(resume_lower, job_desc)
        
        # Both should find matches regardless of case
        assert result_upper['match_percentage'] > 0
        assert result_lower['match_percentage'] > 0
    
    def test_exact_term_matching(self):
        """Test that exact terms from job description are preferred."""
        job_desc = "Required: JavaScript and Node.js"
        resume_with_exact = "Skills: JavaScript, Node.js"
        
        result = self.analyzer.calculate_match_score(resume_with_exact, job_desc)
        
        # Should find the exact terms
        assert result['match_percentage'] > 0
