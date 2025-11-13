"""Command-line interface for Claude Code Desktop."""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from .integration import ClaudeCodeIntegration
from .git_utils import GitManager

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Claude Code Desktop - Git integration for AI-assisted coding."""
    pass


@main.command()
@click.option("--repo", default=".", help="Path to git repository")
def status(repo):
    """Show repository status with Claude Code context."""
    try:
        integration = ClaudeCodeIntegration(repo)
        context = integration.prepare_context()

        console.print(Panel(
            f"[bold cyan]Repository:[/bold cyan] {context['repository']}\n"
            f"[bold cyan]Branch:[/bold cyan] {context['branch']}\n"
            f"[bold cyan]Status:[/bold cyan] {'Clean' if context['is_clean'] else 'Modified'}",
            title="Claude Code Status",
            border_style="cyan"
        ))

        # Show modified files
        if context['status']['modified']:
            console.print("\n[bold yellow]Modified Files:[/bold yellow]")
            for file in context['status']['modified']:
                console.print(f"  [yellow]M[/yellow] {file}")

        # Show staged files
        if context['status']['staged']:
            console.print("\n[bold green]Staged Files:[/bold green]")
            for file in context['status']['staged']:
                console.print(f"  [green]A[/green] {file}")

        # Show untracked files
        if context['status']['untracked']:
            console.print("\n[bold red]Untracked Files:[/bold red]")
            for file in context['status']['untracked']:
                console.print(f"  [red]?[/red] {file}")

        # Show recent commits
        if context['recent_commits']:
            console.print("\n[bold]Recent Commits:[/bold]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("SHA", style="dim")
            table.add_column("Message")
            table.add_column("Author", style="cyan")

            for commit in context['recent_commits']:
                table.add_row(
                    commit['sha'],
                    commit['message'][:50] + "..." if len(commit['message']) > 50 else commit['message'],
                    commit['author']
                )

            console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@main.command()
@click.argument("feature_name")
@click.option("--repo", default=".", help="Path to git repository")
def branch(feature_name, repo):
    """Create a new feature branch for Claude Code assisted development."""
    try:
        integration = ClaudeCodeIntegration(repo)
        branch_name = integration.create_feature_branch(feature_name)
        console.print(f"[bold green]✓[/bold green] Created and checked out branch: [cyan]{branch_name}[/cyan]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@main.command()
@click.option("--files", "-f", multiple=True, help="Files to commit")
@click.option("--message", "-m", help="Commit message (auto-generated if not provided)")
@click.option("--repo", default=".", help="Path to git repository")
def commit(files, message, repo):
    """Commit changes with Claude Code assistance."""
    try:
        integration = ClaudeCodeIntegration(repo)
        
        if not files:
            # Get all modified and staged files
            files = integration.get_files_for_review()
            if not files:
                console.print("[yellow]No changes to commit[/yellow]")
                return

        result = integration.assist_commit(list(files) if files else None, message)
        
        console.print(Panel(
            f"[bold green]Commit:[/bold green] {result['sha']}\n"
            f"[bold green]Branch:[/bold green] {result['branch']}\n"
            f"[bold green]Message:[/bold green] {result['message']}",
            title="✓ Committed Successfully",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@main.command()
@click.option("--repo", default=".", help="Path to git repository")
@click.option("--staged", is_flag=True, help="Show diff of staged changes")
def diff(repo, staged):
    """Show git diff with syntax highlighting."""
    try:
        git_manager = GitManager(repo)
        diff_text = git_manager.get_diff(staged=staged)

        if not diff_text:
            console.print("[yellow]No changes to show[/yellow]")
            return

        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
        console.print(syntax)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@main.command()
@click.argument("file_path")
@click.option("--repo", default=".", help="Path to git repository")
def context(file_path, repo):
    """Get Claude Code context for a specific file."""
    try:
        integration = ClaudeCodeIntegration(repo)
        ctx = integration.get_code_context(file_path)

        if "error" in ctx:
            console.print(f"[bold red]Error:[/bold red] {ctx['error']}", style="red")
            sys.exit(1)

        status_parts = []
        if ctx.get("modified"):
            status_parts.append("[yellow]modified[/yellow]")
        if ctx.get("staged"):
            status_parts.append("[green]staged[/green]")
        if ctx.get("untracked"):
            status_parts.append("[red]untracked[/red]")
        
        status_str = ", ".join(status_parts) if status_parts else "[cyan]unchanged[/cyan]"

        console.print(Panel(
            f"[bold cyan]Path:[/bold cyan] {ctx['path']}\n"
            f"[bold cyan]Size:[/bold cyan] {ctx['size']} bytes\n"
            f"[bold cyan]Extension:[/bold cyan] {ctx['extension']}\n"
            f"[bold cyan]Status:[/bold cyan] {status_str}",
            title="File Context",
            border_style="cyan"
        ))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


@main.command()
@click.option("--repo", default=".", help="Path to git repository")
def suggest(repo):
    """Generate commit message suggestion based on staged changes."""
    try:
        integration = ClaudeCodeIntegration(repo)
        message = integration.generate_commit_message()
        
        console.print(Panel(
            message,
            title="Suggested Commit Message",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
