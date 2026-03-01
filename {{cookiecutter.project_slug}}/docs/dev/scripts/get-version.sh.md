---
title: get-version.sh
---

# 🔍 get-version.sh

This script retrieves the current version of the application from a specified version file. If the file is not found or is invalid, it provides a fallback version based on the current date.

---

## Operations

The script performs the following steps:

- **Base setup**:
    - Identifies the script's directory and the project root directory.
    - Loads environment variables from a `.env` file, if available.
- **Version file path**:
    - The `VERSION_FILE_PATH` variable is set from the environment or defaults to `./src/api/__version__.py` if not provided.
- **Retrieve version**:
    - If the file specified by `VERSION_FILE_PATH` exists:
        - Extracts the version value from the `__version__` variable in the file using `grep`, `awk`, and `tr`.
        - Exits with status code `2` if the version cannot be retrieved.
    - If the file does not exist:
        - Sets a fallback version in the format `0.0.0-YYMMDD` (current UTC date).
- **Output version**:
    - Prints the retrieved or fallback version to the console.

---

## Usage

To execute the script, run the following command:

```sh
./get-version.sh
```

This script can be used to conveniently fetch the version. It is used by the `bump-version.sh` script to retrieve the current version before incrementing it.
