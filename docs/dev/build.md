---
title: Build
---

# 🐳 Build and publish docker image

## Prerequisites

- Install **Docker** and **Docker Compose**.

## Build and push image

**A.** **[RECOMMENDED]** Run **`build.sh`** script to build images:

```sh
# Run build script:
./scripts/build.sh

# -p=PLATFORM, --platform=PLATFORM              Build image type [amd64 | arm64]. Default is current platform.
# -u, --push-images                             Enable pushing built images to Docker Registry.
# -c, --clean-images                            Enable clearning leftover images.
# -x, --cross-compile                           Enable cross compiling.
# -b=BASE_IMAGE, --base-image=BASE_IMAGE        Base image name. Default is "ubuntu:24.04".
# -g=REGISTRY, --registry=REGISTRY              Docker image registry (docker registry and username). Default is "bybatkhuu".
# -r=REPO, --repo=REPO                          Docker image repository. Default is "rest.fastapi-template".
# -v=VERSION, --version=VERSION                 Docker image version. Default read from "./src/api/__version__.py" file.
# -s=SUBTAG, --subtag=SUBTAG                    Docker image subtag. Default is "".
# -d=DOCKERFILE, --dockerfile=DOCKERFILE        Dockerfile path. Default is "./Dockerfile".
# -t=CONTEXT_PATH, --context-path=CONTEXT_PATH  Docker build context path. Default is ".".


# For example:
./scripts/build.sh -p=arm64 -u -c

# Or:
./scripts/build.sh -x

# Or:
./scripts/build.sh -p=arm64 -b=ubuntu:24.04 -n=bybatkhuu -r=rest.fastapi-template -v=1.0.0 -s=-arm64 -d=./Dockerfile -t=. -u -c
```

**B.** Docker build command:

```sh
# Build image:
docker build \
    [IMG_ARGS] \
    --progress plain \
    --platform [PLATFORM] \
    -t $[IMG_FULLNAME] \
    .

# For example:
docker build \
    --progress plain \
    -t bybatkhuu/rest.fastapi-template:latest \
    .

# Push image to Docker Registry:
docker push [IMG_FULLNAME]
# For example:
docker push bybatkhuu/rest.fastapi-template:latest
```

**C.** Docker buildx command (**cross-compile**):

```sh
# Create new builder:
docker buildx create --driver docker-container --bootstrap --use --name new_builder

# Build images and push to Docker Registry:
docker buildx build \
    [IMG_ARGS] \
    --progress plain \
    --platform linux/amd64,linux/arm64 \
    --cache-from=type=registry,ref=[IMG_NAME]:cache-latest \
    --cache-to=type=registry,ref=[IMG_NAME]:cache-latest,mode=max \
    -t [IMG_FULLNAME] \
    --push \
    .

# For example:
docker buildx build \
    --progress plain \
    --platform linux/amd64,linux/arm64 \
    --cache-from=type=registry,ref=bybatkhuu/rest.fastapi-template:cache-latest \
    --cache-to=type=registry,ref=bybatkhuu/rest.fastapi-template:cache-latest,mode=max \
    -t bybatkhuu/rest.fastapi-template:latest \
    --push \
    .

# Remove builder:
docker buildx rm -f new_builder
```

**D.** Docker compose build command:

```sh
# Build image:
docker compose build

# Push image to Docker Registry:
docker compose push
```

👍

---

## References

- <https://docs.docker.com/engine/reference/commandline/build>
- <https://docs.docker.com/get-started/02_our_app>
- <https://docs.docker.com/develop/develop-images/dockerfile_best-practices>
- <https://docs.docker.com/language/python/build-images>
- <https://codefresh.io/docker-tutorial/build-docker-image-dockerfiles>
- <https://learnk8s.io/blog/smaller-docker-images>
- <https://phoenixnap.com/kb/docker-image-size>
- <https://semaphoreci.com/blog/2016/12/13/lightweight-docker-images-in-5-steps.html>
- <https://medium.com/@gdiener/how-to-build-a-smaller-docker-image-76779e18d48a>
