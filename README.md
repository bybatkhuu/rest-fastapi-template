# FastAPI Template

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bybatkhuu/rest-fastapi-template/3.create-release.yml?logo=GitHub)](https://github.com/bybatkhuu/rest-fastapi-template/actions/workflows/3.create-release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/bybatkhuu/rest-fastapi-template?logo=GitHub)](https://github.com/bybatkhuu/rest-fastapi-template/releases)

This is a template repository for FastAPI web service projects.

## ✨ Features

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

## 🧩 Template

- You can use this template repository as reference to create a new repository with the same structure or clone the repository to start a new project. It will help you to organize your project structure and files. It works out of the box for most REST API service projects.
- You can customize (remove, modify or add) the files and directories as needed to meet your project requirements.
- If you want to use the template repository directly, just click the **[Use this template](https://github.com/new?template_name=rest-fastapi-template&template_owner=bybatkhuu)** button and follow the instructions.
- You can use **cookiecutter** to generate a new project from **[cookiecutter](https://github.com/bybatkhuu/rest-fastapi-template/tree/cookiecutter)** branch:

    ```sh
    # Clone the cookiecutter branch:
    git clone -b cookiecutter https://github.com/bybatkhuu/rest-fastapi-template.git

    # Install cookiecutter:
    pip install cookiecutter

    # Generate a new project from the cookiecutter template:
    cookiecutter -f ./rest-fastapi-template
    ```

---

## 🐤 Getting Started

### 1. 🚧 Prerequisites

<!-- *[OPTIONAL]* For **GPU (NVIDIA)**:

- Install **NVIDIA GPU driver (>= v453)** -->

[RECOMMENDED] For **docker** runtime:

- Install [**docker** and **docker compose**](https://docs.docker.com/engine/install)
    - Docker image: [**bybatkhuu/rest-fastapi-template**](https://hub.docker.com/r/bybatkhuu/rest-fastapi-template)
<!-- - *[OPTIONAL]* For **GPU (NVIDIA)**:
    - Install **[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (>= v1)** -->

For **standalone** runtime:

- Install **Python (>= v3.10)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64] [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virutal environment] [venv](https://docs.python.org/3/library/venv.html)*
<!-- - *[OPTIONAL]* For **GPU (NVIDIA)**:
    - Install **NVIDIA CUDA (>= v11)** and **cuDNN (>= v8)** -->

[OPTIONAL] For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

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
git clone https://github.com/bybatkhuu/rest-fastapi-template.git && \
    cd rest-fastapi-template
```

**OPTION B.** Clone the repository (for **DEVELOPMENT**: git + ssh key):

```sh
git clone git@github.com:bybatkhuu/rest-fastapi-template.git && \
    cd rest-fastapi-template
```

**OPTION C.** Download source code:

1. Download archived **zip** or **tar.gz** file from [**releases**](https://github.com/bybatkhuu/rest-fastapi-template/releases).
2. Extract it into the projects directory.
3. Enter into the project directory.

### 3. 📦 Install dependencies

[TIP] Skip this step, if you're going to use **docker** runtime

<!-- #### 3.1. Install base/common dependencies -->

```sh
pip install -r ./requirements.txt

# For DEVELOPMENT:
pip install -r ./requirements/requirements.dev.txt
```

<!-- #### 3.2. Install hardware specific dependencies

Follow the one of below instructions based on your environment (A is recommended for most cases):

**OPTION A.** For Intel/AMD **x86_64** CPU:

```sh
pip install -r ./requirements/requirements.amd64.txt
```

**OPTION B.** For **arm64/aarch64** CPU:

```sh
pip install -r ./requirements/requirements.arm64.txt
```

**OPTION C.** For **NVIDIA GPU** and **x86_64** CPU:

```sh
pip install -r ./requirements/requirements.gpu.txt
``` -->

### 4. 🌎 Configure environment variables

[NOTE] Please, check **[environment variables](#-environment-variables)** section for more details.

#### **OPTION A.** **[RECOMMENDED]** For **docker** runtime **[5.A]**

```sh
# Copy '.env.example' file to '.env' file:
cp -v ./.env.example ./.env

# Edit environment variables to fit in your environment:
nano ./.env
```

#### **OPTION B.** For **standalone** runtime **[5.B ~ 5.F]**

```sh
# Copy '.env.example' file to '.env' file:
cp -v ./.env.example ./src/.env

# Edit environment variables to fit in your environment:
nano ./src/.env
```

### 5. 🏁 Start the server

[NOTE] Follow the one of below instructions based on your environment **[A, B, C, D, E, F]**:

#### Docker runtime

**OPTION A.** **[RECOMMENDED]** Run with **docker compose**:

```sh
## 1. Configure 'compose.override.yml' file.

# Copy 'compose.override.[ENV].yml' file to 'compose.override.yml' file:
cp -v ./templates/compose/compose.override.[ENV].yml ./compose.override.yml
# For example, DEVELOPMENT environment:
cp -v ./templates/compose/compose.override.dev.yml ./compose.override.yml
# For example, STATGING or PRODUCTION environment:
cp -v ./templates/compose/compose.override.prod.yml ./compose.override.yml

# Edit 'compose.override.yml' file to fit in your environment:
nano ./compose.override.yml


## 2. Check docker compose configuration is valid:
./compose.sh validate
# Or:
docker compose config


## 3. Start docker compose:
./compose.sh start -l
# Or:
docker compose up -d --remove-orphans --force-recreate && \
    docker compose logs -f -n 100
```

#### Standalone runtime (PM2)

**OPTION B.** Run with **PM2**:

[**IMPORTANT**] Before running, need to install [**PM2**](https://pm2.keymetrics.io/docs/usage/quick-start):

```sh
## 1. Configure PM2 configuration file.

# Copy example PM2 configuration file:
cp -v ./pm2-process.json.example ./pm2-process.json

# Edit PM2 configuration file to fit in your environment:
nano ./pm2-process.json


## 2. Start PM2 process:
pm2 start ./pm2-process.json && \
    pm2 logs --lines 50 ft
```

#### Standalone runtime (Python)

**OPTION C.** Run server as **python module**:

```sh
python -u -m src.api

# Or:
cd src
python -u -m api
```

**OPTION D.** Run with **uvicorn** cli:

```sh
uvicorn src.api.__main__:app --host=[BIND_HOST] --port=[PORT] --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"
# For example:
uvicorn src.api.__main__:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"

# For DEVELOPMENT:
uvicorn src.api.__main__:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*" --reload --reload-dir=./src


# Or:
cd src
uvicorn api.__main__:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"

# For DEVELOPMENT:
uvicorn src.api.__main__:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*" --reload
```

**OPTION E.** Run with **fastapi** cli:

```sh
fastapi run src/api/__main__.py --host=[BIND_HOST] --port=[PORT] --forwarded-allow-ips="*"
# For example:
fastapi run src/api/__main__.py --port=8000 --forwarded-allow-ips="*"

# For DEVELOPMENT:
fastapi dev src/api/__main__.py --host="0.0.0.0" --port=8000 --forwarded-allow-ips="*"


# Or:
cd src
fastapi run api/__main__.py --port=8000 --forwarded-allow-ips="*"

# For DEVELOPMENT:
fastapi dev api/__main__.py --host="0.0.0.0" --port=8000 --forwarded-allow-ips="*"
```

### 6. ✅ Check server is running

Check with CLI (curl):

```sh
# Send a ping request with 'curl' to REST API server and parse JSON response with 'jq':
curl -s http://localhost:8000/api/v1/ping | jq
```

Check with web browser:

- Health check: <http://localhost:8000/api/v1/health>
- Swagger: <http://localhost:8000/docs>
- Redoc: <http://localhost:8000/redoc>
- OpenAPI JSON: <http://localhost:8000/openapi.json>

### 7. 🛑 Stop the server

Docker runtime:

```sh
# Stop docker compose:
./compose.sh stop
# Or:
docker compose down --remove-orphans
```

Standalone runtime (Only for **PM2**):

```sh
pm2 stop ./pm2-process.json && \
    pm2 flush ft && \
    pm2 delete ./pm2-process.json
```

👍

---

## ⚙️ Configuration

### 🌎 Environment Variables

[**`.env.example`**](./.env.example):

```sh
## --- Environment variable --- ##
ENV=LOCAL
DEBUG=false
# TZ=UTC
# PYTHONDONTWRITEBYTECODE=1


## -- API configs -- ##
FT_API_PORT=8000
# FT_API_LOGS_DIR="/var/log/rest-fastapi-template"
# FT_API_DATA_DIR="/var/lib/rest-fastapi-template"
# FT_API_VERSION="1"
# FT_API_PREFIX="/api/v{api_version}"
# FT_API_DOCS_ENABLED=true
# FT_API_DOCS_OPENAPI_URL="{api_prefix}/openapi.json"
# FT_API_DOCS_DOCS_URL="{api_prefix}/docs"
# FT_API_DOCS_REDOC_URL="{api_prefix}/redoc"
```

---

## 🧪 Running Tests

To run tests, run the following command:

```sh
# Install python test dependencies:
pip install -r ./requirements/requirements.test.txt

# Run tests:
./scripts/test.sh -l -v -c
# Or:
python -m pytest -sv -o log_cli=true
```

## 🏗️ Build Docker Image

Before building the docker image, make sure you have installed **docker** and **docker compose**.

To build the docker image, run the following command:

```sh
# Build docker image:
./scripts/build.sh
# Or:
docker compose build
```

## 📝 Generate Docs

To build the documentation, run the following command:

```sh
# Install python documentation dependencies:
pip install -r ./requirements/requirements.docs.txt

# Serve documentation locally (for development):
./scripts/docs.sh
# Or:
mkdocs serve -a 0.0.0.0:8000 --livereload

# Or build documentation:
./scripts/docs.sh -b
# Or:
mkdocs build
```

## 📚 Documentation

- [Docs](./docs)

---

## 📑 References

- FastAPI - <https://fastapi.tiangolo.com>
- Docker - <https://docs.docker.com>
- Docker Compose - <https://docs.docker.com/compose>
