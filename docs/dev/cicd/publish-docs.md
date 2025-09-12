---
title: Publish Docs
---

# 📝 Publish Docs

## Overview

This GitHub Action automatically publishes project documentation using **MkDocs** whenever changes are pushed to the `main` branch.

## How It Works

The workflow is triggered when changes are pushed to the `main` branch in:

- The `docs/` directory
- The `mkdocs.yml` configuration file

## Workflow Configuration

### **Trigger**

- **`push` to `main` branch**, only when changes occur in:
    - `docs/**`
    - `mkdocs.yml`

### **Jobs**

#### **1. Publish Docs**

This job builds and deploys the MkDocs site to GitHub Pages.

- **Runs on:** `ubuntu-24.04`
- **Permissions:**
    - `contents: write`
- **Steps:**
  1. **Checkout the repository** (with full history)
  2. **Install dependencies** (from `requirements/requirements.docs.txt`)
  3. **Publish documentation** using `mkdocs gh-deploy`

## Usage

To trigger this workflow:

- Push changes to `docs/` or `mkdocs.yml` on the `main` branch.
- The workflow will automatically deploy the updated documentation.

## Required Secrets

- **`GITHUB_TOKEN`**: Required for committing the published documentation.

## Scripts and Tools Used

- **MkDocs**: Static site generator for documentation.
- **`mkdocs.yml`**: Configuration file for MkDocs.
- **`requirements/requirements.docs.txt`**: Contains dependencies for documentation generation.

## Notes

- The documentation is published using **MkDocs Material** and pushed to GitHub Pages.
- The `--force` flag ensures the latest version is always deployed.
- The workflow is **only triggered when documentation-related files change**.

## Troubleshooting

- If documentation does not update, verify that **MkDocs** is correctly configured in `mkdocs.yml`.
- If the workflow fails at **Install dependencies**, check `requirements/requirements.docs.txt` for missing or outdated packages.
- If `mkdocs gh-deploy` fails, ensure `GITHUB_TOKEN` has `contents: write` permissions.
