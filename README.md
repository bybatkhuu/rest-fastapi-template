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
    - *[Python virutal environment] [venv](https://docs.python.org/3/library/venv.html)*

For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) ([video tutorial](https://www.youtube.com/watch?v=snCP3c7wXw0))

### 2. 📥 Download or clone the repository

**2.1.** Prepare projects directory (if not exists):

```sh
# Create projects directory:
mkdir -pv ~/workspaces/projects

# Enter into projects directory:
cd ~/workspaces/projects
```

**2.2.** Follow one of the below options **[A]**, **[B]** or **[C]**:

**OPTION A.** Clone the repository:

```sh
git clone https://github.com/[OWNER]/rest-fastapi-template.git && \
    cd rest-fastapi-template && \
    git checkout cookiecutter
```

**OPTION B.** Clone the repository (for **DEVELOPMENT**: git + ssh key):

```sh
git clone git@github.com:[OWNER]/rest-fastapi-template.git && \
    cd rest-fastapi-template && \
    git checkout cookiecutter
```

**OPTION C.** Download source code from cookiecutter branch.

### 3. 📦 Install cookiecutter

```sh
# Install cookiecutter:
pip install -U cookiecutter
# Or:
pip install -r ./requirements.txt
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
cd [PROJECT_NAME]
# For example:
cd rest-fastapi-template

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
