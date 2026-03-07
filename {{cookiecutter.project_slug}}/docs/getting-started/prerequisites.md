---
title: Prerequisites
---

# 🚧 Prerequisites

<!-- *[OPTIONAL]* For **GPU (NVIDIA)**:

- Install **NVIDIA GPU driver (>= v453)** -->

[RECOMMENDED] For **docker** runtime:

- Install [**docker** and **docker compose**](https://docs.docker.com/engine/install)
    - Docker image: [**{{cookiecutter.docker_registry}}/{{cookiecutter.docker_repo_name}}**](https://hub.docker.com/r/{{cookiecutter.docker_registry}}/{{cookiecutter.docker_repo_name}})
<!-- - *[OPTIONAL]* For **GPU (NVIDIA)**:
    - Install **[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) (>= v1)** -->

For **standalone** runtime:

- Install **Python (>= v3.10)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64]  [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virtual environment]  [venv](https://docs.python.org/3/library/venv.html)*
<!-- - *[OPTIONAL]* For **GPU (NVIDIA)**:
    - Install **NVIDIA CUDA (>= v11)** and **cuDNN (>= v8)** -->

[OPTIONAL] For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)
