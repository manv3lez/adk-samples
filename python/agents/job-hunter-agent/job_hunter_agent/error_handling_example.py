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

"""Examples of using the error handling system in Job Hunter Agent.

This module demonstrates how to integrate error handling into agent workflows.
"""

from job_hunter_agent import error_handler
from job_hunter_agent.state_manager import get_state_manager


def example_agent_with_error_handling():
    """Example of wrapping an agent operation with error handling."""
    
    try:
        # Simulate agent operation
        state_manager = get_state_manager()
        
        # Check if required state exists
        career_profile = state_manager.retrieve_state("career_profile_output")
        if not career_profile:
            # Use convenience function for missing state
            return error_handler.handle_state_not_found("career_profile_output")
        
        # Perform agent operation
        result = process_career_profile(career_profile)
        
        return {
            "success": True,
            "result": result
        }
        
    except ValueError as e:
        # Handle input validation errors
        return error_handler.handle_error(
            error_handler.InputValidationError(
                message="The career profile information is incomplete",
                details=str(e),
                next_steps=[
                    "Please provide your complete work history",
                    "Include all relevant skills and experience",
                    "Try the career profile analysis again"
                ]
            ),
            context={"agent": "example_agent", "operation": "process_profile"}
        )
        
    except ConnectionError as e:
        # Handle external service errors
        return error_handler.handle_service_unavailable("Job Search API")
        
    except Exception as e:
        # Handle unexpected errors
        return error_handler.handle_error(
            e,
            context={"agent": "example_agent", "operation": "process_profile"}
        )


def example_sub_agent_invocation():
    """Example of invoking a sub-agent with error handling."""
    
    try:
        # Check prerequisites
        state_manager = get_state_manager()
        if not state_manager.retrieve_state("career_profile_output"):
            return error_handler.handle_state_not_found("career_profile_output")
        
        # Invoke sub-agent (simulated)
        # In real code: result = sub_agent.run(input_data)
        result = invoke_sub_agent("job_market_researcher", {})
        
        # Store result
        state_manager.store_state("job_opportunities_output", result)
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        return error_handler.handle_agent_failure(
            agent_name="Job Market Researcher",
            details=str(e)
        )


def example_input_validation():
    """Example of validating user input with error handling."""
    
    user_input = get_user_input()  # Simulated
    
    # Validate required fields
    if not user_input.get("resume"):
        return error_handler.handle_missing_input("resume")
    
    # Validate format
    if not is_valid_resume_format(user_input["resume"]):
        return error_handler.handle_invalid_format(
            field_name="resume",
            expected_format="PDF, DOCX, or plain text"
        )
    
    # Process valid input
    return process_resume(user_input["resume"])


def example_custom_error():
    """Example of creating a custom error with specific guidance."""
    
    try:
        # Some operation that might fail
        result = risky_operation()
        return result
        
    except SpecificError as e:
        # Create custom error with tailored guidance
        error = error_handler.JobHunterError(
            message="We couldn't complete your job search due to an unusual issue",
            category=error_handler.ErrorCategory.AGENT_EXECUTION,
            details=f"SpecificError: {str(e)}",
            next_steps=[
                "Try simplifying your search criteria",
                "Focus on one job board at a time",
                "Contact support if this continues",
                "We can help you search manually in the meantime"
            ]
        )
        return error_handler.handle_error(error)


def example_partial_results():
    """Example of returning partial results when an error occurs."""
    
    results = []
    errors = []
    
    for job_board in ["LinkedIn", "Indeed", "Glassdoor"]:
        try:
            # Search each job board
            jobs = search_job_board(job_board)
            results.extend(jobs)
        except Exception as e:
            # Log error but continue with other sources
            errors.append({
                "source": job_board,
                "error": str(e)
            })
    
    if not results and errors:
        # All searches failed
        return error_handler.handle_service_unavailable("Job Search Services")
    
    if errors:
        # Some searches failed, return partial results with warning
        return {
            "success": True,
            "results": results,
            "warnings": [
                f"Unable to search {err['source']}: {err['error']}"
                for err in errors
            ],
            "message": f"Found {len(results)} opportunities from available sources. Some job boards were temporarily unavailable.",
            "next_steps": [
                "Review the opportunities we found",
                "Try searching the unavailable sources later",
                "Let me know if you'd like to proceed with these results"
            ]
        }
    
    # All searches succeeded
    return {
        "success": True,
        "results": results
    }


# Simulated helper functions for examples
def process_career_profile(profile):
    """Simulated profile processing."""
    return {"processed": True}


def invoke_sub_agent(agent_name, input_data):
    """Simulated sub-agent invocation."""
    return {"agent": agent_name, "result": "success"}


def get_user_input():
    """Simulated user input."""
    return {"resume": "sample_resume.pdf"}


def is_valid_resume_format(resume):
    """Simulated format validation."""
    return resume.endswith((".pdf", ".docx", ".txt"))


def process_resume(resume):
    """Simulated resume processing."""
    return {"processed": True}


def risky_operation():
    """Simulated risky operation."""
    return {"result": "success"}


class SpecificError(Exception):
    """Simulated specific error type."""
    pass


def search_job_board(board_name):
    """Simulated job board search."""
    return [{"job": f"Job from {board_name}"}]


if __name__ == "__main__":
    # Run examples
    print("Example 1: Agent with error handling")
    print(example_agent_with_error_handling())
    
    print("\nExample 2: Sub-agent invocation")
    print(example_sub_agent_invocation())
    
    print("\nExample 3: Input validation")
    print(example_input_validation())
    
    print("\nExample 4: Custom error")
    print(example_custom_error())
    
    print("\nExample 5: Partial results")
    print(example_partial_results())
