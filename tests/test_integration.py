"""Tests for integration module."""

import pytest
from pathlib import Path
from claude_code.integration import ClaudeCodeIntegration


def test_integration_initialization(temp_repo):
    """Test ClaudeCodeIntegration initialization."""
    integration = ClaudeCodeIntegration(temp_repo)
    assert integration.repo_path == temp_repo
    assert integration.git is not None


def test_prepare_context(temp_repo):
    """Test preparing context information."""
    integration = ClaudeCodeIntegration(temp_repo)
    context = integration.prepare_context()

    assert "repository" in context
    assert "branch" in context
    assert "status" in context
    assert "recent_commits" in context
    assert "is_clean" in context


def test_generate_commit_message(temp_repo):
    """Test generating commit message."""
    integration = ClaudeCodeIntegration(temp_repo)

    # Create and stage a file
    new_file = Path(temp_repo) / "test.txt"
    new_file.write_text("Test content")
    integration.git.stage_files(["test.txt"])

    message = integration.generate_commit_message()
    assert message is not None
    assert len(message) > 0


def test_create_feature_branch(temp_repo):
    """Test creating feature branch."""
    integration = ClaudeCodeIntegration(temp_repo)

    branch_name = integration.create_feature_branch("my-feature")
    assert branch_name == "claude/my-feature"
    assert integration.git.get_current_branch() == "claude/my-feature"


def test_assist_commit(temp_repo):
    """Test assisted commit."""
    integration = ClaudeCodeIntegration(temp_repo)

    # Create a new file
    new_file = Path(temp_repo) / "test.txt"
    new_file.write_text("Test content")

    result = integration.assist_commit(["test.txt"], "Test commit")

    assert "sha" in result
    assert "message" in result
    assert "branch" in result
    assert result["message"] == "Test commit"


def test_get_files_for_review(temp_repo):
    """Test getting files for review."""
    integration = ClaudeCodeIntegration(temp_repo)

    # Modify a file
    test_file = Path(temp_repo) / "README.md"
    test_file.write_text("# Modified")

    files = integration.get_files_for_review()
    assert "README.md" in files


def test_get_code_context(temp_repo):
    """Test getting code context for a file."""
    integration = ClaudeCodeIntegration(temp_repo)

    context = integration.get_code_context("README.md")

    assert "path" in context
    assert "exists" in context
    assert context["exists"] is True
    assert "size" in context
    assert "extension" in context


def test_get_code_context_nonexistent_file(temp_repo):
    """Test getting code context for nonexistent file."""
    integration = ClaudeCodeIntegration(temp_repo)

    context = integration.get_code_context("nonexistent.txt")

    assert "error" in context
    assert context["error"] == "File not found"
