"""Tests for config module."""

import pytest
from pathlib import Path
from claude_code.config import Config


def test_config_initialization(temp_config):
    """Test Config initialization."""
    config = Config(str(temp_config))
    assert config.config is not None


def test_config_default_values():
    """Test default configuration values."""
    config = Config("/nonexistent/config.yml")

    assert config.get("git.auto_stage") is False
    assert config.get("git.branch_prefix") == "claude"
    assert config.get("claude.context_lines") == 50
    assert config.get("display.color") is True


def test_config_get(temp_config):
    """Test getting configuration values."""
    config = Config(str(temp_config))

    # Test nested key access
    value = config.get("git.branch_prefix")
    assert value == "claude"

    # Test default value
    value = config.get("nonexistent.key", "default")
    assert value == "default"


def test_config_set(temp_config):
    """Test setting configuration values."""
    config = Config(str(temp_config))

    config.set("git.branch_prefix", "feature")
    assert config.get("git.branch_prefix") == "feature"

    # Test nested key creation
    config.set("new.nested.key", "value")
    assert config.get("new.nested.key") == "value"


def test_config_save_and_load(temp_config):
    """Test saving and loading configuration."""
    config1 = Config(str(temp_config))
    config1.set("git.branch_prefix", "custom")
    config1.save()

    # Load in new instance
    config2 = Config(str(temp_config))
    assert config2.get("git.branch_prefix") == "custom"
