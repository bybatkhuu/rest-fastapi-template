#!/bin/bash
set -euo pipefail


## --- Base --- ##
# Getting path of this script file:
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2


# Loading .env file (if exists):
if [ -f ".env" ]; then
	# shellcheck disable=SC1091
	source .env
fi


if ! command -v yq >/dev/null 2>&1; then
	echo "[ERROR]: 'yq' not found or not installed!"
	exit 1
fi
## --- Base --- ##


## --- Variables --- ##
# Load from envrionment variables:
VERSION_FILE_PATH="${VERSION_FILE_PATH:-./src/api/__version__.py}"
COMPOSE_FILE_PATH="${COMPOSE_FILE_PATH:-./templates/compose/compose.override.prod.yml}"
COMPOSE_GPU_FILE_PATH="${COMPOSE_GPU_FILE_PATH:-./templates/compose/compose.override.prod.gpu.yml}"
SERVICE_NAME="${SERVICE_NAME:-api}"
IMG_NAME="${IMG_NAME:-bybatkhuu/rest.fastapi-template}"

# Flags:
_IS_ADD=false
## --- Variables --- ##


## --- Main --- ##
main()
{
	## --- Menu arguments --- ##
	if [ -n "${1:-}" ]; then
		for _input in "${@:-}"; do
			case ${_input} in
				-a | --add)
					_IS_ADD=true
					shift;;
				*)
					echo "[ERROR]: Failed to parse input -> ${_input}!"
					echo "[INFO]: USAGE: ${0}  -a, --git-add"
					exit 1;;
			esac
		done
	fi
	## --- Menu arguments --- ##


	if [ ! -f "${VERSION_FILE_PATH:-}" ]; then
		echo "[ERROR]: Not found version file: ${VERSION_FILE_PATH}!"
		exit 1
	fi

	if [ ! -f "${COMPOSE_FILE_PATH:-}" ]; then
		echo "[ERROR]: Not found compose file: ${COMPOSE_FILE_PATH}!"
		exit 1
	fi

	if [ "${_IS_ADD}" == true ]; then
		if ! command -v git >/dev/null 2>&1; then
			echo "[ERROR]: 'git' not found or not installed!"
			exit 1
		fi
	fi

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

main "${@:-}"
## --- Main --- ##
