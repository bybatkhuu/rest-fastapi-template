---
title: "File Structure"
---

# 📂 File Structure

```txt
project/
├── .github/                 # GitHub specific files
│   ├── workflows/               # GitHub Actions workflows
│   ├── CODEOWNERS               # GitHub code owners file for automatic review assignment
│   ├── dependabot.yml           # Dependabot configuration
│   └── release.yml              # Categories and labels for release notes
├── .vscode/                 # VSCode specific files
│   ├── extensions.json          # Recommended extensions for the workspace
│   └── settings.json            # Common VSCode settings for the workspace
├── docs/                    # Documentation of this project
│   ├── assets/                  # Assets for documentation (images, videos, styles, etc.)
│   ├── .../                     # Other documentation files and directories
│   ├── README.md                # README documentation
│   └── release-notes.md         # Release notes documentation
├── examples/                # Example source codes
├── requirements/            # Dependency requirements for different environments
├── scripts/                 # Helpful scripts
├── src/                     # Main codebase directory
│   ├── api/                     # Main API directory
│   │   ├── .../                    # Submodules and subpackages for the API (e.g. routers, services, etc...)
│   │   ├── __init__.py             # Initialize the API module
│   │   ├── __main__.py             # Main entry point for the API as a module
│   │   ├── __version__.py          # Version of the API
│   │   ├── bootstrap.py            # Bootstrap for FastAPI application
│   │   ├── config.py               # Main configuration
│   │   ├── exception.py            # All exception handlers will be registered here
│   │   ├── lifespan.py             # Lifespan events (startup, shutdown)
│   │   ├── logger.py               # Logging and logger related file
│   │   ├── main.py                 # Main function to run the FastAPI application
│   │   ├── middleware.py           # All middlewares will be registered here
│   │   ├── mount.py                # All mount points will be registered here
│   │   └── router.py               # All routers will be registered here
│   ├── modules/                 # Third-party modules and libraries
│   └── __init__.py              # Initialize and add src to the module path
├── templates/               # Template files
├── tests/                   # Tests for the project
│   ├── __init__.py          # Initialize the test module
│   ├── conftest.py          # Presets for pytest (e.g. fixtures, plugins, pre/post test hooks, etc...)
│   ├── test_main.py         # Test case files
│   └── ...
├── volumes/                 # Persistent storage volumes
├── .dockerignore            # Docker ignore file
├── .editorconfig            # Editor configuration
├── .env.example             # Example environment variables file
├── .gitignore               # Git ignore file
├── .markdownlint.json       # Markdown linting rules
├── .python-version          # Python version for project
├── CHANGELOG.md             # Project changelog
├── compose.sh               # Docker compose script
├── compose.yml              # Docker compose configuration
├── Dockerfile               # Docker image definition
├── LICENSE.txt              # Project license
├── Makefile                 # Make commands for common tasks
├── mkdocs.yml               # MkDocs configuration
├── pm2-process.json.example # PM2 process file example
├── pytest.ini               # Pytest configuration
├── README.md                # Main README
└── requirements.txt         # Python requirements
```
