"""Claude Code integration module."""

import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from .git_utils import GitManager


class ClaudeCodeIntegration:
    """Integrates Claude Code with Git workflows."""

    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize Claude Code integration.

        Args:
            repo_path: Path to git repository.
        """
        self.git = GitManager(repo_path)
        self.repo_path = self.git.repo_path

    def prepare_context(self) -> Dict[str, Any]:
        """
        Prepare context information for Claude Code.

        Returns:
            Dictionary with context information.
        """
        status = self.git.get_status()
        history = self.git.get_commit_history(max_count=5)

        context = {
            "repository": os.path.basename(self.repo_path),
            "branch": status["branch"],
            "status": status,
            "recent_commits": history,
            "is_clean": self.git.is_clean(),
        }

        return context

    def generate_commit_message(self, diff: Optional[str] = None) -> str:
        """
        Generate a suggested commit message based on changes.

        Args:
            diff: Optional diff string. If None, uses staged changes.

        Returns:
            Suggested commit message.
        """
        if diff is None:
            diff = self.git.get_diff(staged=True)

        if not diff:
            return "No changes to commit"

        # Simple heuristic-based commit message generation
        # In a real implementation, this would use Claude's API
        lines = diff.split("\n")
        added = sum(1 for line in lines if line.startswith("+") and not line.startswith("+++"))
        removed = sum(1 for line in lines if line.startswith("-") and not line.startswith("---"))

        if added > removed:
            return f"Add changes ({added} additions, {removed} deletions)"
        elif removed > added:
            return f"Remove changes ({added} additions, {removed} deletions)"
        else:
            return f"Update changes ({added} additions, {removed} deletions)"

    def create_feature_branch(self, feature_name: str) -> str:
        """
        Create a feature branch for Claude Code assisted development.

        Args:
            feature_name: Name of the feature.

        Returns:
            Name of created branch.
        """
        branch_name = f"claude/{feature_name}"
        self.git.create_branch(branch_name, checkout=True)
        return branch_name

    def assist_commit(
        self, files: Optional[List[str]] = None, message: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Assist with committing changes using Claude Code suggestions.

        Args:
            files: Optional list of files to commit.
            message: Optional commit message. If None, generates one.

        Returns:
            Dictionary with commit information.
        """
        # Stage files if provided
        if files:
            self.git.stage_files(files)

        # Generate message if not provided
        if message is None:
            message = self.generate_commit_message()

        # Commit
        sha = self.git.commit(message)

        return {
            "sha": sha[:7],
            "message": message,
            "branch": self.git.get_current_branch(),
        }

    def get_files_for_review(self) -> List[str]:
        """
        Get list of files that have changes for review.

        Returns:
            List of file paths.
        """
        status = self.git.get_status()
        return status["modified"] + status["staged"]

    def get_code_context(self, file_path: str) -> Dict[str, Any]:
        """
        Get context information for a specific file.

        Args:
            file_path: Path to file.

        Returns:
            Dictionary with file context.
        """
        full_path = Path(self.repo_path) / file_path

        if not full_path.exists():
            return {"error": "File not found"}

        context = {
            "path": file_path,
            "exists": True,
            "size": full_path.stat().st_size,
            "extension": full_path.suffix,
        }

        # Check if file is modified
        status = self.git.get_status()
        context["modified"] = file_path in status["modified"]
        context["staged"] = file_path in status["staged"]
        context["untracked"] = file_path in status["untracked"]

        return context
