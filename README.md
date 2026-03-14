# FastAPI Template (Cookiecutter)

This is a cookiecutter template for FastAPI web service projects.

## ✨ Features

- Cookiecutter
- FastAPI
- REST API
- Web service
- Microservice
- Project structure
- Boilerplate/template
- Best practices
- Configuration
- Tests
- Build
- Scripts
- Examples
- Documentation
- CI/CD
- Docker and docker compose

---

## 🐤 Getting started

### 1. 🚧 Prerequisites

- Install **Python (>= v3.9)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64] [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virtual environment] [venv](https://docs.python.org/3/library/venv.html)*

For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

### 2. 📥 Download or clone the repository

```sh
# Create projects directory:
mkdir -pv ~/workspaces/projects

# Enter into projects directory:
cd ~/workspaces/projects

# Clone the repository:
git clone [REPOSITORY_URL]
# Or download and extract the repository from GitHub:
# 1. Go to the repository on GitHub.
# 2. Click on the "Code" button.
# 3. Select "Download ZIP" and save the file to your computer.
# 4. Extract the ZIP file in current directory.

# Enter into the repository:
cd rest-fastapi-template

# Change to cookiecutter branch:
git checkout cookiecutter
```

### 3. 📦 Install cookiecutter

```sh
# Install cookiecutter:
pip install -r ./requirements.txt
# Install pre-commit hooks:
pre-commit install
```

### 4. 🏗️ Generate project with cookiecutter

```sh
# Generate project:
cookiecutter -f .
# Or:
./scripts/build.sh
```

### 5. 🏁 Start the project

```sh
cd [PROJECT_SLUG]

# Start:
./compose.sh start -l

# Stop:
./compose.sh stop
```

👍

## 📑 References

- Cookiecutter (GitHub) - <https://github.com/cookiecutter/cookiecutter>
- Cookiecutter (Docs) - <https://cookiecutter.readthedocs.io/en/stable>
- FastAPI - <https://fastapi.tiangolo.com>
