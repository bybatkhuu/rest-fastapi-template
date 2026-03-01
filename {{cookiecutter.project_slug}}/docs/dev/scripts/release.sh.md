---
title: release.sh
---

# 🚀 release.sh

This script automates the creation of GitHub Releases for the project.

The script performs the following operations:

- **Environment setup**:  
  Ensures it runs from the project root and sources environment variables from `.env` if available.
- **Dependency checks**:  
  Verifies that `git` and `gh` (GitHub CLI) are installed, and that the user is authenticated with `gh auth login`.
- **Versioning**:  
  Uses `./scripts/get-version.sh` to determine the release version.
- **Release creation**:  
  Runs `gh release create v<version> --generate-notes` to publish a new GitHub Release with attached artifacts.

**Usage**:

To execute the release script, use the following command in the terminal:

```sh
./release.sh
```

**Examples**:

- To create a release: `./release.sh`

**Notes**:

- A .env file is optional but will be loaded if present.
- The release tag will be prefixed with v (e.g., v1.2.3-250101).
