---
title: backup.sh
---

# 🗄️ backup.sh

This script is designed to create versioned, timestamped backups of the project's data (specifically the `volumes` and `storage` directories). It ensures backups are consistent with the project version and can be stored in a configurable directory.

---

## Operations

The script performs the following operations:

- **Base setup**:  
    - Loads environment variables from a `.env` file if present.  
- **Environment variables**:  
    - `BACKUPS_DIR` → backup directory (default: `./volumes/backups`)  
- **Backup creation**:  
    - Ensures the backup directory exists (creates it if needed).  
    - Fetches the current version using `./scripts/get-version.sh`.  
    - Creates a `.tar.gz` archive with filename format.  
    - Archives the `./volumes/storage` directory using `tar`.  
    - Falls back to `sudo tar` if permission is denied.  

---

## Usage

To execute the backup script, run:

```sh
./scripts/backup.sh
```

---

## Requirements

- Bash  
- tar  
- Optional: `.env` file to override `PROJECT_SLUG` and `BACKUPS_DIR`  
- Executable script: `./scripts/get-version.sh`  

---

## Notes

- Backups are compressed using **gzip** (`.tar.gz`).  
- Script retries with `sudo` if file permissions require elevated privileges.  
- Timestamps are generated in **UTC** for consistency.  
