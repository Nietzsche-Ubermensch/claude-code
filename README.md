# Claude-Code-Desktop

[![Claude Code](https://github.com/Nietzsche-Ubermensch/claude-code/actions/workflows/claude.yml/badge.svg)](https://github.com/Nietzsche-Ubermensch/claude-code/actions/workflows/claude.yml)

Claude Code integration for Git repositories - A powerful tool to enhance your Git workflow with AI-assisted coding.

## Overview

Claude-Code-Desktop provides seamless integration between Claude Code (AI coding assistant) and Git version control. It helps developers streamline their workflow by providing intelligent context awareness, automated commit message generation, and enhanced Git operations.

## Features

- 🔄 **Smart Git Operations**: Enhanced Git commands with AI context
- 🌿 **Branch Management**: Easy creation of feature branches with Claude prefix
- 💬 **Commit Assistance**: Auto-generate commit messages based on changes
- 📊 **Rich Status Display**: Beautiful, colorful status information
- 🔍 **File Context**: Get detailed context about files in your repository
- 📝 **Diff Visualization**: Syntax-highlighted diffs for better readability

## Installation

### From Source

```bash
git clone https://github.com/Lolavice9019/Claude-Code-Desktop.git
cd Claude-Code-Desktop
pip install -e .
```

### Using pip (when published)

```bash
pip install claude-code-desktop
```

## Requirements

- Python 3.8 or higher
- Git installed and configured
- A Git repository to work with

## Quick Start

1. Navigate to your Git repository:

```bash
cd your-project
```

2. Check status with Claude context:

```bash
claude-git status
```

3. Create a new feature branch:

```bash
claude-git branch my-feature
```

4. Make your changes, then commit with assistance:

```bash
claude-git commit -m "Your commit message"
```

Or let Claude suggest a message:

```bash
claude-git suggest
claude-git commit
```

## Commands

### `status`

Show repository status with Claude Code context including modified files, staged files, and recent commits.

```bash
claude-git status [--repo PATH]
```

### `branch`

Create a new feature branch with the `claude/` prefix for AI-assisted development.

```bash
claude-git branch <feature_name> [--repo PATH]
```

### `commit`

Commit changes with Claude Code assistance. Auto-generates commit messages if not provided.

```bash
claude-git commit [--files FILE ...] [--message MESSAGE] [--repo PATH]
```

### `diff`

Show git diff with beautiful syntax highlighting.

```bash
claude-git diff [--repo PATH] [--staged]
```

### `context`

Get Claude Code context information for a specific file.

```bash
claude-git context <file_path> [--repo PATH]
```

### `suggest`

Generate a commit message suggestion based on staged changes.

```bash
claude-git suggest [--repo PATH]
```

## Configuration

Create a configuration file at `~/.claude-code/config.yml`:

```yaml
git:
  auto_stage: false
  branch_prefix: "claude"
  default_commit_template: "{type}: {description}"

claude:
  context_lines: 50
  max_file_size: 1048576 # 1MB

display:
  color: true
  verbose: false
```

## Examples

### Example 1: Start a new feature with Claude assistance

```bash
# Create and checkout a new feature branch
claude-git branch user-authentication

# Check status
claude-git status

# Make your changes...

# Stage files and commit with auto-generated message
claude-git commit -f src/auth.py -f src/user.py
```

### Example 2: Review changes before committing

```bash
# View your changes with syntax highlighting
claude-git diff

# Stage changes
git add .

# Get suggested commit message
claude-git suggest

# Commit with the suggested message
claude-git commit -m "Add user authentication module"
```

### Example 3: Get context about a file

```bash
# Check file status and context
claude-git context src/main.py
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Lolavice9019/Claude-Code-Desktop.git
cd Claude-Code-Desktop

# Install development dependencies
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Code Style

This project uses:

- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

```bash
# Format code
black src/

# Run linter
flake8 src/

# Type check
mypy src/
```

## Architecture

```
Claude-Code-Desktop/
├── src/claude_code/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── git_utils.py         # Git operations wrapper
│   ├── integration.py       # Claude Code integration logic
│   └── config.py            # Configuration management
├── tests/                   # Test files
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`claude-git branch my-feature`)
3. Commit your changes (`claude-git commit -m "Add some feature"`)
4. Push to the branch (`git push origin claude/my-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Lolavice9019**

## Acknowledgments

- Built with [GitPython](https://github.com/gitpython-developers/GitPython)
- CLI powered by [Click](https://click.palletsprojects.com/)
- Beautiful output using [Rich](https://github.com/Textualize/rich)
