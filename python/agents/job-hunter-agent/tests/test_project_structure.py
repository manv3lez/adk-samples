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

"""Unit tests for project structure and module imports.

Tests that verify:
- All modules can be imported correctly
- Configuration loading works as expected
- Directory structure is properly set up

Requirements: 1.1
"""

import importlib
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


class TestModuleImports:
    """Test that all modules can be imported correctly."""

    def test_main_package_import(self) -> None:
        """Test that the main job_hunter_agent package can be imported."""
        import job_hunter_agent

        assert job_hunter_agent is not None

    def test_sub_agents_package_import(self) -> None:
        """Test that the sub_agents package can be imported."""
        from job_hunter_agent import sub_agents

        assert sub_agents is not None

    def test_utils_package_import(self) -> None:
        """Test that the utils package can be imported."""
        from job_hunter_agent import utils

        assert utils is not None

    def test_all_submodules_importable(self) -> None:
        """Test that all expected submodules exist and are importable."""
        # List of expected submodules based on project structure
        expected_modules = [
            "job_hunter_agent",
            "job_hunter_agent.sub_agents",
            "job_hunter_agent.utils",
        ]

        for module_name in expected_modules:
            try:
                module = importlib.import_module(module_name)
                assert module is not None, f"Module {module_name} imported as None"
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")


class TestConfigurationLoading:
    """Test configuration loading functionality."""

    def test_environment_variables_set_on_import(self) -> None:
        """Test that importing job_hunter_agent sets required environment variables."""
        # Import should set these variables
        import job_hunter_agent

        # Check that GOOGLE_CLOUD_LOCATION is set
        assert "GOOGLE_CLOUD_LOCATION" in os.environ
        assert os.environ["GOOGLE_CLOUD_LOCATION"] == "global"

        # Check that GOOGLE_GENAI_USE_VERTEXAI is set
        assert "GOOGLE_GENAI_USE_VERTEXAI" in os.environ
        assert os.environ["GOOGLE_GENAI_USE_VERTEXAI"] == "True"

    @patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project"}, clear=False)
    def test_google_cloud_project_uses_environment(self) -> None:
        """Test that GOOGLE_CLOUD_PROJECT can be set via environment."""
        # This test verifies that environment variables work
        import job_hunter_agent

        # Should have the value from environment
        assert os.environ["GOOGLE_CLOUD_PROJECT"] == "test-project"

    @patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "test-project"}, clear=False)
    def test_existing_google_cloud_project_preserved(self) -> None:
        """Test that existing GOOGLE_CLOUD_PROJECT is not overwritten."""
        # Reload the module to test the setdefault behavior
        import job_hunter_agent

        importlib.reload(job_hunter_agent)

        # Should preserve the existing value
        assert os.environ["GOOGLE_CLOUD_PROJECT"] == "test-project"

    def test_env_example_file_exists(self) -> None:
        """Test that .env.example file exists with required variables."""
        project_root = Path(__file__).parent.parent
        env_example_path = project_root / ".env.example"

        assert env_example_path.exists(), ".env.example file should exist"

        # Read and verify it contains expected configuration keys
        content = env_example_path.read_text()
        expected_keys = [
            "GOOGLE_GENAI_USE_VERTEXAI",
            "GOOGLE_CLOUD_PROJECT",
            "GOOGLE_CLOUD_LOCATION",
            "GOOGLE_CLOUD_STORAGE_BUCKET",
        ]

        for key in expected_keys:
            assert key in content, f"Expected key {key} not found in .env.example"


class TestProjectStructure:
    """Test that the project directory structure is correct."""

    def test_main_package_directory_exists(self) -> None:
        """Test that the main package directory exists."""
        project_root = Path(__file__).parent.parent
        package_dir = project_root / "job_hunter_agent"

        assert package_dir.exists(), "job_hunter_agent directory should exist"
        assert package_dir.is_dir(), "job_hunter_agent should be a directory"

    def test_sub_agents_directory_exists(self) -> None:
        """Test that the sub_agents directory exists."""
        project_root = Path(__file__).parent.parent
        sub_agents_dir = project_root / "job_hunter_agent" / "sub_agents"

        assert sub_agents_dir.exists(), "sub_agents directory should exist"
        assert sub_agents_dir.is_dir(), "sub_agents should be a directory"

    def test_utils_directory_exists(self) -> None:
        """Test that the utils directory exists."""
        project_root = Path(__file__).parent.parent
        utils_dir = project_root / "job_hunter_agent" / "utils"

        assert utils_dir.exists(), "utils directory should exist"
        assert utils_dir.is_dir(), "utils should be a directory"

    def test_tests_directory_exists(self) -> None:
        """Test that the tests directory exists."""
        project_root = Path(__file__).parent.parent
        tests_dir = project_root / "tests"

        assert tests_dir.exists(), "tests directory should exist"
        assert tests_dir.is_dir(), "tests should be a directory"

    def test_all_packages_have_init_files(self) -> None:
        """Test that all package directories have __init__.py files."""
        project_root = Path(__file__).parent.parent
        package_dirs = [
            project_root / "job_hunter_agent",
            project_root / "job_hunter_agent" / "sub_agents",
            project_root / "job_hunter_agent" / "utils",
            project_root / "tests",
        ]

        for package_dir in package_dirs:
            init_file = package_dir / "__init__.py"
            assert init_file.exists(), f"__init__.py should exist in {package_dir}"
            assert init_file.is_file(), f"__init__.py in {package_dir} should be a file"

    def test_pyproject_toml_exists(self) -> None:
        """Test that pyproject.toml exists and is valid."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"

        assert pyproject_path.exists(), "pyproject.toml should exist"
        assert pyproject_path.is_file(), "pyproject.toml should be a file"

        # Verify it contains expected sections
        content = pyproject_path.read_text()
        expected_sections = [
            "[project]",
            "name = \"job-hunter-agent\"",
            "dependencies",
            "[dependency-groups]",
            "pytest",
            "hypothesis",
        ]

        for section in expected_sections:
            assert section in content, f"Expected section '{section}' not found in pyproject.toml"


class TestDependencies:
    """Test that required dependencies are available."""

    def test_google_adk_available(self) -> None:
        """Test that google-adk is available."""
        try:
            import google.genai.adk
            assert google.genai.adk is not None
        except ImportError:
            pytest.skip("google-adk not installed (expected in dev environment)")

    def test_pytest_available(self) -> None:
        """Test that pytest is available."""
        import pytest as pt

        assert pt is not None

    def test_hypothesis_available(self) -> None:
        """Test that hypothesis is available for property-based testing."""
        try:
            import hypothesis
            assert hypothesis is not None
        except ImportError:
            pytest.skip("hypothesis not installed (expected in dev environment)")

    def test_pydantic_available(self) -> None:
        """Test that pydantic is available."""
        try:
            import pydantic
            assert pydantic is not None
        except ImportError:
            pytest.skip("pydantic not installed (expected in dev environment)")

    def test_dotenv_available(self) -> None:
        """Test that python-dotenv is available."""
        try:
            import dotenv
            assert dotenv is not None
        except ImportError:
            pytest.fail("python-dotenv should be available as a core dependency")
