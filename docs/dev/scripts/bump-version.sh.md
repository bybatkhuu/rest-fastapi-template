---
title: bump-version.sh
---

# 🏷 bump-version.sh

This script automates the process of managing project versioning. It allows you to increment the **major**, **minor**, or **patch** part of the version according to [Semantic Versioning](https://semver.org) principles. Additionally, it provides options for committing changes, tagging the repository, and pushing updates to a remote Git repository.

---

## Operations

The script performs the following tasks:

- **Base initialization**:
    - Determines the script and project root directories.
    - Sources the `base.sh` script for utilities and loads environment variables from a `.env` file if available.
- **Variable setup**:
    - Uses the `VERSION_FILE_PATH` variable to locate the version file (default: `./src/api/__version__.py`).
    - Defines flags for version bump type, commit, tag, and push operations.
- **Parse input arguments**:
    - `-b=*, --bump-type=*` specifies the type of version bump:
        - **major**, **minor**, or **patch**.
    - `-c, --commit`: Commits the updated version file.
    - `-t, --tag`: Creates a new Git tag for the updated version.
    - `-p, --push`: Pushes the changes and the tag to the remote Git repository.
- **Validate input**:
    - Ensures a valid bump type is provided.
    - Verifies the existence of a Git repository if commit/tag/push flags are used.
- **Version management**:
    - Retrieves the current version using the `get-version.sh` script.
    - Splits the version into its components (**major**, **minor**, **patch**) and increments the appropriate part based on the bump type.
    - Updates the version file with the new version.
- **Git operations** (Optional):
    - If the `-c` flag is used, commits the changes.
    - If the `-t` flag is used, creates a Git tag for the new version (avoids duplicates).
    - If the `-p` flag is used, pushes the changes and tag to the remote repository.

---

## Usage

To execute the script, use the following command:

```sh
./bump-version.sh -b=<bump_type> [options]
```

Replace **`<bump_type>`** with either **`major`**, **`minor`**, or **`patch`** to indicate which part of the version to increment. The `-p` or `--push-tag` flag tells the script to commit the changes and push the tag to the Git repository.

## Examples

To bump the **`minor`** version and push the **new tag**, run:

```sh
./bump-version.sh -b=minor -p
```

This script streamlines the versioning process, reducing the chances of errors and ensuring consistency in versioning.

---

## References

- <https://semver.org>
