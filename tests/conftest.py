"""Test configuration for Claude Code Desktop."""

import pytest
from pathlib import Path
import tempfile
import shutil
from git import Repo


@pytest.fixture
def temp_repo():
    """Create a temporary git repository for testing."""
    temp_dir = tempfile.mkdtemp()
    repo = Repo.init(temp_dir)
    
    # Configure git user for the test repo
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Create an initial commit
    test_file = Path(temp_dir) / "README.md"
    test_file.write_text("# Test Repository")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_config():
    """Create a temporary config file."""
    temp_dir = tempfile.mkdtemp()
    config_path = Path(temp_dir) / "config.yml"
    
    yield config_path
    
    # Cleanup
    shutil.rmtree(temp_dir)
