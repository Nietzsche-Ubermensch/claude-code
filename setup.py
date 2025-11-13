"""Setup configuration for Claude Code Desktop."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-code-desktop",
    version="0.1.0",
    author="Lolavice9019",
    description="Claude code integration to Git repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lolavice9019/Claude-Code-Desktop",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "GitPython>=3.1.0",
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-git=claude_code.cli:main",
        ],
    },
)
