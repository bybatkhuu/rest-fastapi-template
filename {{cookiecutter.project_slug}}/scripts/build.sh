#!/usr/bin/env bash
set -euo pipefail


## --- Base --- ##
_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-"$0"}")" >/dev/null 2>&1 && pwd -P)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2


# shellcheck disable=SC1091
[ -f .env ] && . .env


# Checking docker and docker-compose installed:
if ! command -v docker >/dev/null 2>&1; then
	echo "[ERROR]: Not found 'docker' command, please install it first!" >&2
	exit 1
fi

if ! docker info > /dev/null 2>&1; then
	echo "[ERROR]: Unable to communicate with the docker daemon. Check docker is running or check your account added to docker group!" >&2
	exit 1
fi

if ! docker compose > /dev/null 2>&1; then
	echo "[ERROR]: 'docker compose' not found or not installed!" >&2
	exit 1
fi
## --- Base --- ##


## --- Variables --- ##
# Load from environment variables:
BASE_IMAGE=${BASE_IMAGE:-}
IMG_REGISTRY=${IMG_REGISTRY:-{{cookiecutter.docker_registry}}}
IMG_REPO=${PROJECT_SLUG:-{{cookiecutter.docker_repo_name}}}
IMG_VERSION=${IMG_VERSION:-$(./scripts/get-version.sh)}
IMG_SUBTAG=${IMG_SUBTAG:-}
IMG_PLATFORM=${IMG_PLATFORM:-$(uname -m)}
DOCKERFILE_PATH=${DOCKERFILE_PATH:-./Dockerfile}
CONTEXT_PATH=${CONTEXT_PATH:-.}

HASH_PASSWORD="${HASH_PASSWORD:-}"
IMG_ARGS="${IMG_ARGS:-}"

# Flags:
_IS_CROSS_COMPILE=false
_IS_PUSH_IMAGES=false
_IS_CLEAN_IMAGES=false

# Calculated variables:
_IMG_NAME=""
if [ -n "${IMG_REGISTRY}" ]; then
	_IMG_NAME="${IMG_REGISTRY}/${IMG_REPO}"
else
	_IMG_NAME="${IMG_REPO}"
fi
_IMG_FULLNAME=${_IMG_NAME}:${IMG_VERSION}${IMG_SUBTAG}
_IMG_LATEST_FULLNAME=${_IMG_NAME}:latest${IMG_SUBTAG}
## --- Variables --- ##


## --- Menu arguments --- ##
_usage_help() {
	cat <<EOF
USAGE: ${0} [options]

OPTIONS:
    -p, --platform [PLATFORM]    Target platform [amd64 | arm64]. Default: Host architecture
    -u, --push-images            Push built images to registry. Default: false
    -c, --clean-images           Remove built images after completion. Default: false
    -x, --cross-compile          Enable cross compilation. Default: false
    -b, --base-image [IMAGE]     Base image to use.
    -g, --registry [REGISTRY]    Container registry. Default: {{cookiecutter.docker_registry}}
    -r, --repo [REPO]            Image repository. Default: {{cookiecutter.docker_repo_name}}
    -v, --version [VERSION]      Image version tag.
    -s, --subtag [SUBTAG]        Additional image subtag.
    -d, --dockerfile [PATH]      Path to Dockerfile. Default: ./Dockerfile
    -t, --context-path [PATH]    Build context path. Default: .
    -h, --help                   Show this help message.

EXAMPLES:
    ${0} -p amd64 -b ubuntu:24.04 -v 1.0.0
    ${0} --cross-compile --clean-images
EOF
}

while [ $# -gt 0 ]; do
	case "${1}" in
		-p | --platform)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			IMG_PLATFORM="${2}"
			shift 2;;
		-p=* | --platform=*)
			IMG_PLATFORM="${1#*=}"
			shift;;
		-u | --push-images)
			_IS_PUSH_IMAGES=true
			shift;;
		-c | --clean-images)
			_IS_CLEAN_IMAGES=true
			shift;;
		-x | --cross-compile)
			_IS_CROSS_COMPILE=true
			shift;;
		-b | --base-image)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			BASE_IMAGE="${2}"
			shift 2;;
		-b=* | --base-image=*)
			BASE_IMAGE="${1#*=}"
			shift;;
		-g | --registry)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			IMG_REGISTRY="${2}"
			shift 2;;
		-g=* | --registry=*)
			IMG_REGISTRY="${1#*=}"
			shift;;
		-r | --repo)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			IMG_REPO="${2}"
			shift 2;;
		-r=* | --repo=*)
			IMG_REPO="${1#*=}"
			shift;;
		-v | --version)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			IMG_VERSION="${2}"
			shift 2;;
		-v=* | --version=*)
			IMG_VERSION="${1#*=}"
			shift;;
		-s | --subtag)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			IMG_SUBTAG="${2}"
			shift 2;;
		-s=* | --subtag=*)
			IMG_SUBTAG="${1#*=}"
			shift;;
		-d | --dockerfile)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			DOCKERFILE_PATH="${2}"
			shift 2;;
		-d=* | --dockerfile=*)
			DOCKERFILE_PATH="${1#*=}"
			shift;;
		-t | --context-path)
			[ $# -ge 2 ] || { echo "[ERROR]: ${1} requires a value!" >&2; exit 1; }
			CONTEXT_PATH="${2}"
			shift 2;;
		-t=* | --context-path=*)
			CONTEXT_PATH="${1#*=}"
			shift;;
		-h | --help)
			_usage_help
			exit 0;;
		*)
			echo "[ERROR]: Failed to parse argument -> ${1}!" >&2
			_usage_help
			exit 1;;
	esac
done
## --- Menu arguments --- ##


## --- Validation --- ##
# if [ -z "${IMG_REGISTRY:-}" ]; then
# 	echo "[ERROR]: Required 'IMG_REGISTRY' environment variable or '--registry=' argument for image registry!" >&2
# 	exit 1
# fi

if [ -n "${BASE_IMAGE:-}" ]; then
	IMG_ARGS="${IMG_ARGS} --build-arg BASE_IMAGE=${BASE_IMAGE}"
fi

if [ -n "${HASH_PASSWORD:-}" ]; then
	IMG_ARGS="${IMG_ARGS} --secret id=HASH_PASSWORD,env=HASH_PASSWORD"
fi

if [ -n "${IMG_REGISTRY}" ]; then
	_IMG_NAME="${IMG_REGISTRY}/${IMG_REPO}"
else
	_IMG_NAME="${IMG_REPO}"
fi
_IMG_FULLNAME=${_IMG_NAME}:${IMG_VERSION}${IMG_SUBTAG}
_IMG_LATEST_FULLNAME=${_IMG_NAME}:latest${IMG_SUBTAG}

if [ "${IMG_PLATFORM}" = "x86_64" ] || [ "${IMG_PLATFORM}" = "amd64" ] || [ "${IMG_PLATFORM}" = "linux/amd64" ]; then
	IMG_PLATFORM="linux/amd64"
elif [ "${IMG_PLATFORM}" = "aarch64" ] || [ "${IMG_PLATFORM}" = "arm64" ] || [ "${IMG_PLATFORM}" = "linux/arm64" ]; then
	IMG_PLATFORM="linux/arm64"
else
	echo "[ERROR]: Unsupported platform: ${IMG_PLATFORM}!" >&2
	exit 2
fi
## --- Validation --- ##


## --- Functions --- ##
_build_images()
{
	echo "[INFO]: Building image (${IMG_PLATFORM}): ${_IMG_FULLNAME}"
	# shellcheck disable=SC2086
	DOCKER_BUILDKIT=1 docker build \
		${IMG_ARGS} \
		--progress plain \
		--platform "${IMG_PLATFORM}" \
		-t "${_IMG_FULLNAME}" \
		-t "${_IMG_LATEST_FULLNAME}" \
		-t "${_IMG_FULLNAME}-${IMG_PLATFORM#linux/*}" \
		-t "${_IMG_LATEST_FULLNAME}-${IMG_PLATFORM#linux/*}" \
		-f "${DOCKERFILE_PATH}" \
		"${CONTEXT_PATH}" || exit 2
	echo "[OK]: Done."
}

_build_cross_push()
{
	if ! docker buildx ls | grep new_builder > /dev/null 2>&1; then
		echo "[INFO]: Creating new builder..."
		docker buildx create --driver docker-container --bootstrap --use --name new_builder || exit 2
		echo "[OK]: Done."
	fi

	echo "[INFO]: Cross building images (linux/amd64, linux/arm64): ${_IMG_FULLNAME}"
	# shellcheck disable=SC2086
	docker buildx build \
		${IMG_ARGS} \
		--progress plain \
		--platform linux/amd64,linux/arm64 \
		--cache-from=type="registry,ref=${_IMG_NAME}:cache-latest" \
		--cache-to=type="registry,ref=${_IMG_NAME}:cache-latest,mode=max" \
		-t "${_IMG_FULLNAME}" \
		-t "${_IMG_LATEST_FULLNAME}" \
		-f "${DOCKERFILE_PATH}" \
		--push \
		"${CONTEXT_PATH}" || exit 2
	echo "[OK]: Done."

	echo "[INFO]: Removing new builder..."
	docker buildx rm new_builder || exit 2
	echo "[OK]: Done."
}

_remove_caches()
{
	echo "[INFO]: Removing leftover cache images..."
	# shellcheck disable=SC2046
	docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) 2> /dev/null || true
	echo "[OK]: Done."
}

_push_images()
{
	echo "[INFO]: Pushing images..."
	docker push "${_IMG_FULLNAME}" || exit 2
	docker push "${_IMG_LATEST_FULLNAME}" || exit 2
	docker push "${_IMG_FULLNAME}-${IMG_PLATFORM#linux/*}" || exit 2
	docker push "${_IMG_LATEST_FULLNAME}-${IMG_PLATFORM#linux/*}" || exit 2
	echo "[OK]: Done."
}

_clean_images()
{
	echo "[INFO]: Cleaning images..."
	docker rmi -f "${_IMG_FULLNAME}" || exit 2
	# docker rmi -f "${_IMG_LATEST_FULLNAME}" || exit 2
	docker rmi -f "${_IMG_FULLNAME}-${IMG_PLATFORM#linux/*}" || exit 2
	docker rmi -f "${_IMG_LATEST_FULLNAME}-${IMG_PLATFORM#linux/*}" || exit 2
	echo "[OK]: Done."
}
## --- Functions --- ##


## --- Main --- ##
main()
{
	if [ ${_IS_CROSS_COMPILE} == false ]; then
		_build_images
	else
		_build_cross_push
	fi

	_remove_caches

	if [ ${_IS_PUSH_IMAGES} == true ] && [ ${_IS_CROSS_COMPILE} == false ]; then
		_push_images

		if  [ ${_IS_CLEAN_IMAGES} == true ]; then
			_clean_images
		fi
	fi
}

main
## --- Main --- ##
