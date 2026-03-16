"""Tests for git_utils module."""

import pytest
from pathlib import Path
from claude_code.git_utils import GitManager


def test_git_manager_initialization(temp_repo):
    """Test GitManager initialization."""
    git_manager = GitManager(temp_repo)
    assert git_manager.repo_path == temp_repo
    assert git_manager.repo is not None


def test_git_manager_invalid_repo():
    """Test GitManager with invalid repository."""
    with pytest.raises(ValueError, match="Not a git repository"):
        GitManager("/nonexistent/path")


def test_get_current_branch(temp_repo):
    """Test getting current branch name."""
    git_manager = GitManager(temp_repo)
    branch = git_manager.get_current_branch()
    assert branch in ["master", "main"]


def test_get_modified_files(temp_repo):
    """Test getting modified files."""
    git_manager = GitManager(temp_repo)

    # Modify a file
    test_file = Path(temp_repo) / "README.md"
    test_file.write_text("# Modified")

    modified = git_manager.get_modified_files()
    assert "README.md" in modified


def test_get_untracked_files(temp_repo):
    """Test getting untracked files."""
    git_manager = GitManager(temp_repo)

    # Create a new file
    new_file = Path(temp_repo) / "new_file.txt"
    new_file.write_text("New content")

    untracked = git_manager.get_untracked_files()
    assert "new_file.txt" in untracked


def test_stage_and_commit(temp_repo):
    """Test staging and committing files."""
    git_manager = GitManager(temp_repo)

    # Create a new file
    new_file = Path(temp_repo) / "test.txt"
    new_file.write_text("Test content")

    # Stage and commit
    git_manager.stage_files(["test.txt"])
    sha = git_manager.commit("Test commit")

    assert sha is not None
    assert len(sha) == 40  # Full SHA length


def test_create_branch(temp_repo):
    """Test creating a new branch."""
    git_manager = GitManager(temp_repo)

    git_manager.create_branch("test-branch", checkout=True)
    assert git_manager.get_current_branch() == "test-branch"


def test_get_status(temp_repo):
    """Test getting repository status."""
    git_manager = GitManager(temp_repo)

    # Create and modify files
    new_file = Path(temp_repo) / "new.txt"
    new_file.write_text("New")

    test_file = Path(temp_repo) / "README.md"
    test_file.write_text("# Modified")

    status = git_manager.get_status()

    assert "branch" in status
    assert "modified" in status
    assert "staged" in status
    assert "untracked" in status
    assert "new.txt" in status["untracked"]
    assert "README.md" in status["modified"]


def test_is_clean(temp_repo):
    """Test checking if working directory is clean."""
    git_manager = GitManager(temp_repo)

    # Should be clean initially
    assert git_manager.is_clean() is True

    # Create a new file
    new_file = Path(temp_repo) / "test.txt"
    new_file.write_text("Test")

    # Should not be clean
    assert git_manager.is_clean() is False


def test_get_commit_history(temp_repo):
    """Test getting commit history."""
    git_manager = GitManager(temp_repo)

    history = git_manager.get_commit_history(max_count=5)

    assert len(history) >= 1
    assert "sha" in history[0]
    assert "message" in history[0]
    assert "author" in history[0]
    assert "date" in history[0]


def test_get_diff(temp_repo):
    """Test getting diff."""
    git_manager = GitManager(temp_repo)

    # Modify a file
    test_file = Path(temp_repo) / "README.md"
    test_file.write_text("# Modified content")

    diff = git_manager.get_diff(staged=False)
    assert "README.md" in diff
    assert "Modified content" in diff
