---
title: "File Structure"
---

# 📂 File Structure

```txt
project/
├── .github/                 # GitHub specific files
│   ├── workflows/               # GitHub Actions workflows
│   └── release.yml              # Categories and labels for release notes
├── .vscode/                 # VSCode specific files
│   ├── extensions.json          # Recommended extensions for the workspace
│   └── settings.json            # Common VSCode settings for the workspace
├── docs/                    # Documentation of this project
│   ├── assets/                  # Assets for documentation (images, videos, styles, etc.)
│   ├── diagrams/                # Diagrams related to the project
│   ├── pages/                   # Markdown pages for documentation
│   ├── references/              # References related to the project
│   ├── reports/                 # Reports generated from results
│   └── README.md                # Documentation README
├── examples/                # Example source codes
├── requirements/            # Dependency requirements for different environments
├── scripts/                 # Helpful scripts
├── src/                     # Main codebase directory
│   ├── api/                        # Main API directory
│   │   ├── __init__.py             # Initialize the api module
│   │   ├── __main__.py             # Main entry point for the api
│   │   ├── __version__.py          # Version of the api
│   │   ├── config.py               # Main configuration
│   │   ├── exception.py            # All exception handlers will be registered here
│   │   ├── lifespan.py             # Lifespan events (startup, shutdown)
│   │   ├── logger.py               # Initialize the logger
│   │   ├── middleware.py           # All middlewares will be registered here
│   │   ├── router.py               # All routers will be registered here
│   │   └── server.py               # Main FastAPI application
│   ├── assets/                  # Assets for the codebase
│   ├── configs/                 # Configuration files
│   ├── locale/                  # Localization files
│   ├── __init__.py              # Initialize the codebase
│   └── main.py                  # Main entry point
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
├── CHANGELOG.md             # Project change log
├── compose.sh               # Docker compose script
├── compose.yml              # Docker compose configuration
├── Dockerfile               # Docker image definition
├── environment.yml          # Conda environment file
├── LICENSE.txt              # Project license
├── Makefile                 # Automation commands
├── mkdocs.yml               # MkDocs configuration
├── pm2-process.json.example # PM2 process file example
├── pytest.ini               # Pytest configuration
├── README.md                # Main README
└── requirements.txt         # Python requirements
```
