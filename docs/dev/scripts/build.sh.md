---
title: build.sh
---

# 🏗️ build.sh

This script automates the process of building, pushing, and cleaning Docker images for your project. It supports cross-compilation for multiple platforms, registry management, and advanced configuration options.

---

## Operations

- **Initialization**:
    - Sets up project and script paths.
    - Loads environment variables from a `.env` file if available.
    - Ensures Docker is installed and running.

- **Flexible configuration**:
    - Allows customization of the image registry, repository, version, and platform through flags or environment variables.

- **Build process**:
    - Builds Docker images for the specified platform.
    - Supports cross-compilation for `amd64` and `arm64` platforms using Docker Buildx.

- **Push process** (optional):
    - Pushes built images to the specified container registry.

- **Clean-Up** (optional):
    - Cleans up dangling images and optionally removes built images after pushing.

- **Advanced features**:
    - Supports specifying a base image, custom tags, and additional build arguments.

---

## Usage

To execute the script, use the following command:

```sh
./build.sh [options]
```

## Examples

```sh
# Run build script:
./scripts/build.sh

# -p=PLATFORM, --platform=PLATFORM              Build image type [amd64 | arm64]. Default is current platform.
# -u, --push-images                             Enable pushing built images to Docker Registry.
# -c, --clean-images                            Enable clearning leftover images.
# -x, --cross-compile                           Enable cross compiling.
# -b=BASE_IMAGE, --base-image=BASE_IMAGE        Base image name. Default is "ubuntu:24.04".
# -g=REGISTRY, --registry=REGISTRY              Docker image registry (docker registry and username). Default is "bybatkhuu".
# -r=REPO, --repo=REPO                          Docker image repository. Default is "rest-fastapi-template".
# -v=VERSION, --version=VERSION                 Docker image version. Default read from "./src/api/__version__.py" file.
# -s=SUBTAG, --subtag=SUBTAG                    Docker image subtag. Default is "".
# -d=DOCKERFILE, --dockerfile=DOCKERFILE        Dockerfile path. Default is "./Dockerfile".
# -t=CONTEXT_PATH, --context-path=CONTEXT_PATH  Docker build context path. Default is ".".


# For example:
./scripts/build.sh -p=arm64 -u -c

# Or:
./scripts/build.sh -x

# Or:
./scripts/build.sh -p=arm64 -b=ubuntu:24.04 -g=bybatkhuu -r=rest-fastapi-template -v=1.0.0 -s=-arm64 -d=./Dockerfile -t=. -u -c
```
