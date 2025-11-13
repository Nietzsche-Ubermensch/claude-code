"""Git utilities for Claude Code integration."""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path
import git
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError, NoSuchPathError


class GitManager:
    """Manages Git operations for Claude Code integration."""

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize Git manager.

        Args:
            repo_path: Path to git repository. If None, uses current directory.
        """
        self.repo_path = repo_path or os.getcwd()
        try:
            self.repo = Repo(self.repo_path, search_parent_directories=True)
        except (InvalidGitRepositoryError, NoSuchPathError):
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        return self.repo.active_branch.name

    def get_modified_files(self) -> List[str]:
        """Get list of modified files in the working directory."""
        return [item.a_path for item in self.repo.index.diff(None)]

    def get_staged_files(self) -> List[str]:
        """Get list of staged files."""
        return [item.a_path for item in self.repo.index.diff("HEAD")]

    def get_untracked_files(self) -> List[str]:
        """Get list of untracked files."""
        return self.repo.untracked_files

    def stage_files(self, files: List[str]) -> None:
        """
        Stage files for commit.

        Args:
            files: List of file paths to stage.
        """
        self.repo.index.add(files)

    def commit(self, message: str, files: Optional[List[str]] = None) -> str:
        """
        Commit changes.

        Args:
            message: Commit message.
            files: Optional list of files to commit. If None, commits all staged files.

        Returns:
            Commit SHA.
        """
        if files:
            self.stage_files(files)
        
        commit = self.repo.index.commit(message)
        return commit.hexsha

    def create_branch(self, branch_name: str, checkout: bool = True) -> None:
        """
        Create a new branch.

        Args:
            branch_name: Name of the new branch.
            checkout: Whether to checkout the new branch.
        """
        new_branch = self.repo.create_head(branch_name)
        if checkout:
            new_branch.checkout()

    def checkout_branch(self, branch_name: str) -> None:
        """
        Checkout an existing branch.

        Args:
            branch_name: Name of the branch to checkout.
        """
        self.repo.heads[branch_name].checkout()

    def get_diff(self, staged: bool = False) -> str:
        """
        Get diff of changes.

        Args:
            staged: If True, get diff of staged changes. Otherwise, working directory.

        Returns:
            Diff as string.
        """
        if staged:
            return self.repo.git.diff("--cached")
        return self.repo.git.diff()

    def get_commit_history(self, max_count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent commit history.

        Args:
            max_count: Maximum number of commits to retrieve.

        Returns:
            List of commit information dictionaries.
        """
        commits = []
        for commit in self.repo.iter_commits(max_count=max_count):
            commits.append({
                "sha": commit.hexsha[:7],
                "message": commit.message.strip(),
                "author": str(commit.author),
                "date": commit.committed_datetime.isoformat(),
            })
        return commits

    def get_status(self) -> Dict[str, List[str]]:
        """
        Get repository status.

        Returns:
            Dictionary with status information.
        """
        return {
            "branch": self.get_current_branch(),
            "modified": self.get_modified_files(),
            "staged": self.get_staged_files(),
            "untracked": self.get_untracked_files(),
        }

    def is_clean(self) -> bool:
        """Check if working directory is clean."""
        return not self.repo.is_dirty() and not self.repo.untracked_files
