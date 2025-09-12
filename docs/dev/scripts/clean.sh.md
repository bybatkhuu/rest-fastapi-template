---
title: clean.sh
---

# 🧹 clean.sh

This script is designed to clean up the build environment by removing artifacts and other temporary or unwanted files and directories. It also includes additional safeguards to ensure Docker is not running before performing certain cleanup operations.

---

## Operations

The script performs the following operations:

- **Environment variables**: Loads environment variables from a `.env` file if it exists.
- **Delete system files**: Finds and deletes all `.DS_Store`, `.Thumbs.db`, and `.coverage*` files in the project directory and its subdirectories.
- **Delete cache directories**: Finds and deletes all `__pycache__`, `.benchmarks`, and `.pytest_cache` directories in the project directory and its subdirectories.
- **Delete logs**: Removes directories named `logs` unless they are part of a `.git` directory.
- **Delete project directories**: Removes the project-related directory specified by the `PROJECT_SLUG` environment variable (default: `rest.fastapi-template`).
- **Docker safeguards**:
    - Checks if Docker is installed and running.
    - Stops execution if Docker containers are active.
- **Extended cleanup (optional)**: If the `--all` flag is used, it performs additional cleanup:
    - Removes Docker containers, volumes, and orphaned containers (if Docker is running).

---

## Usage

To execute the clean script, run the following command:

```sh
./clean.sh [-a|--all]
```

## Examples

- To clean just non-essential files: `./clean.sh`
- To clean all files: `./clean.sh -a`

This will clean up the project directory, removing any unnecessary files and directories and ensuring a clean environment for a fresh build.
