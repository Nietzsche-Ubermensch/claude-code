# API Reference

## Modules

### git_utils.GitManager

Git operations manager for Claude Code Desktop.

#### Constructor

```python
GitManager(repo_path: Optional[str] = None)
```

**Parameters:**
- `repo_path`: Path to git repository. If None, uses current directory.

**Raises:**
- `ValueError`: If the path is not a valid git repository.

#### Methods

##### get_current_branch()
```python
def get_current_branch() -> str
```
Get the name of the current branch.

**Returns:** Branch name as string.

##### get_modified_files()
```python
def get_modified_files() -> List[str]
```
Get list of modified files in the working directory.

**Returns:** List of file paths.

##### get_staged_files()
```python
def get_staged_files() -> List[str]
```
Get list of staged files.

**Returns:** List of file paths.

##### get_untracked_files()
```python
def get_untracked_files() -> List[str]
```
Get list of untracked files.

**Returns:** List of file paths.

##### stage_files()
```python
def stage_files(files: List[str]) -> None
```
Stage files for commit.

**Parameters:**
- `files`: List of file paths to stage.

##### commit()
```python
def commit(message: str, files: Optional[List[str]] = None) -> str
```
Commit changes.

**Parameters:**
- `message`: Commit message.
- `files`: Optional list of files to commit.

**Returns:** Commit SHA.

##### create_branch()
```python
def create_branch(branch_name: str, checkout: bool = True) -> None
```
Create a new branch.

**Parameters:**
- `branch_name`: Name of the new branch.
- `checkout`: Whether to checkout the new branch.

##### get_diff()
```python
def get_diff(staged: bool = False) -> str
```
Get diff of changes.

**Parameters:**
- `staged`: If True, get diff of staged changes.

**Returns:** Diff as string.

##### get_status()
```python
def get_status() -> Dict[str, List[str]]
```
Get repository status.

**Returns:** Dictionary with status information containing:
- `branch`: Current branch name
- `modified`: List of modified files
- `staged`: List of staged files
- `untracked`: List of untracked files

##### is_clean()
```python
def is_clean() -> bool
```
Check if working directory is clean.

**Returns:** True if clean, False otherwise.

---

### integration.ClaudeCodeIntegration

Main integration class for Claude Code with Git.

#### Constructor

```python
ClaudeCodeIntegration(repo_path: Optional[str] = None)
```

**Parameters:**
- `repo_path`: Path to git repository.

#### Methods

##### prepare_context()
```python
def prepare_context() -> Dict[str, Any]
```
Prepare context information for Claude Code.

**Returns:** Dictionary with context information.

##### generate_commit_message()
```python
def generate_commit_message(diff: Optional[str] = None) -> str
```
Generate a suggested commit message based on changes.

**Parameters:**
- `diff`: Optional diff string. If None, uses staged changes.

**Returns:** Suggested commit message.

##### create_feature_branch()
```python
def create_feature_branch(feature_name: str) -> str
```
Create a feature branch for Claude Code assisted development.

**Parameters:**
- `feature_name`: Name of the feature.

**Returns:** Name of created branch.

##### assist_commit()
```python
def assist_commit(
    files: Optional[List[str]] = None,
    message: Optional[str] = None
) -> Dict[str, str]
```
Assist with committing changes using Claude Code suggestions.

**Parameters:**
- `files`: Optional list of files to commit.
- `message`: Optional commit message.

**Returns:** Dictionary with commit information.

##### get_code_context()
```python
def get_code_context(file_path: str) -> Dict[str, Any]
```
Get context information for a specific file.

**Parameters:**
- `file_path`: Path to file.

**Returns:** Dictionary with file context.

---

### config.Config

Configuration management for Claude Code Desktop.

#### Constructor

```python
Config(config_path: Optional[str] = None)
```

**Parameters:**
- `config_path`: Path to configuration file. If None, uses default location.

#### Methods

##### get()
```python
def get(key: str, default: Any = None) -> Any
```
Get configuration value.

**Parameters:**
- `key`: Configuration key (supports nested keys with dots).
- `default`: Default value if key not found.

**Returns:** Configuration value.

##### set()
```python
def set(key: str, value: Any) -> None
```
Set configuration value.

**Parameters:**
- `key`: Configuration key (supports nested keys with dots).
- `value`: Value to set.

##### save()
```python
def save() -> None
```
Save configuration to file.

---

## CLI Commands

### claude-git status
Show repository status with Claude Code context.

**Options:**
- `--repo PATH`: Path to git repository (default: current directory)

### claude-git branch
Create a new feature branch.

**Arguments:**
- `feature_name`: Name of the feature

**Options:**
- `--repo PATH`: Path to git repository

### claude-git commit
Commit changes with Claude Code assistance.

**Options:**
- `--files, -f`: Files to commit (multiple allowed)
- `--message, -m`: Commit message
- `--repo PATH`: Path to git repository

### claude-git diff
Show git diff with syntax highlighting.

**Options:**
- `--repo PATH`: Path to git repository
- `--staged`: Show diff of staged changes

### claude-git context
Get Claude Code context for a specific file.

**Arguments:**
- `file_path`: Path to file

**Options:**
- `--repo PATH`: Path to git repository

### claude-git suggest
Generate commit message suggestion.

**Options:**
- `--repo PATH`: Path to git repository
