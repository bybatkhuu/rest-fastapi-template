#!/usr/bin/env bash
set -euo pipefail


## --- Base --- ##
_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-"$0"}")" >/dev/null 2>&1 && pwd -P)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2


# shellcheck disable=SC1091
[ -f .env ] && . .env


if ! command -v yq >/dev/null 2>&1; then
	echo "[ERROR]: Not found 'yq' command, please install it first!" >&2
	exit 1
fi

if [ ! -f ./scripts/get-version.sh ]; then
	echo "[ERROR]: 'get-version.sh' script not found!" >&2
	exit 1
fi
## --- Base --- ##


## --- Variables --- ##
# Load from environment variables:
VERSION_FILE_PATH="${VERSION_FILE_PATH:-./src/api/__version__.py}"
COMPOSE_FILE_PATH="${COMPOSE_FILE_PATH:-./compose.yml}"
COMPOSE_GPU_FILE_PATH="${COMPOSE_GPU_FILE_PATH:-./templates/compose/compose.override.prod.gpu.yml}"
SERVICE_NAME="${SERVICE_NAME:-api}"
IMG_NAME="${IMG_NAME:-bybatkhuu/rest-fastapi-template}"

# Flags:
_IS_ADD=false
## --- Variables --- ##


## --- Menu arguments --- ##
_usage_help() {
	cat <<EOF
USAGE: ${0} [options]

OPTIONS:
    -a, --add     Stage changes using 'git add'. Default: false
    -h, --help    Show this help message.

EXAMPLES:
    ${0} -a
    ${0} --add
EOF
}

while [ $# -gt 0 ]; do
	case "${1}" in
		-a | --add)
			_IS_ADD=true
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
if [ ! -f "${VERSION_FILE_PATH:-}" ]; then
	echo "[ERROR]: Not found version file: ${VERSION_FILE_PATH}" >&2
	exit 1
fi

if [ ! -f "${COMPOSE_FILE_PATH:-}" ]; then
	echo "[ERROR]: Not found compose file: ${COMPOSE_FILE_PATH}" >&2
	exit 1
fi

if [ ! -f "${COMPOSE_GPU_FILE_PATH:-}" ]; then
	echo "[ERROR]: Not found compose GPU file: ${COMPOSE_GPU_FILE_PATH}" >&2
	exit 1
fi

if [ "${_IS_ADD}" == true ]; then
	if ! command -v git >/dev/null 2>&1; then
		echo "[ERROR]: Not found 'git' command, please install it first!" >&2
		exit 1
	fi
fi
## --- Validation --- ##


## --- Main --- ##
main()
{
	local _cuurrent_version
	_current_version="$(./scripts/get-version.sh)" || exit 2
	echo "[INFO]: Synching '${SERVICE_NAME}' service image version to: '${IMG_NAME}:${_current_version}' ..."
	yq -i ".services.${SERVICE_NAME}.image = \"${IMG_NAME}:${_current_version}\"" "${COMPOSE_FILE_PATH}"
	yq -i ".services.${SERVICE_NAME}.image = \"${IMG_NAME}:${_current_version}-gpu\"" "${COMPOSE_GPU_FILE_PATH}"
	echo "[OK]: Done."

	if [ "${_IS_ADD}" == true ]; then
		git add "${COMPOSE_FILE_PATH}" || exit 2
		git add "${COMPOSE_GPU_FILE_PATH}" || exit 2
	fi
}

main
## --- Main --- ##
