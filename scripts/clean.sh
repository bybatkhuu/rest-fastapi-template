#!/usr/bin/env bash
set -euo pipefail


## --- Base --- ##
_SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-"$0"}")" >/dev/null 2>&1 && pwd -P)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2


# shellcheck disable=SC1091
[ -f .env ] && . .env
## --- Base --- ##


## --- Variables --- ##
# Flags:
_IS_ALL=false
## --- Variables --- ##


## --- Menu arguments --- ##
_usage_help() {
	cat <<EOF
USAGE: ${0} [options]

OPTIONS:
    -a, --all     Enable all mode. Default: false
    -h, --help    Show this help message.

EXAMPLES:
    ${0} -a
    ${0} --all
EOF
}

while [ $# -gt 0 ]; do
	case "${1}" in
		-a | --all)
			_IS_ALL=true
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


## --- Main --- ##
main()
{
	echo "[INFO]: Cleaning..."

	find . -path "./volumes/storage" -prune -o -type f -name ".DS_Store" -print -exec rm -f {} + || exit 2
	find . -path "./volumes/storage" -prune -o -type f -name ".Thumbs.db" -print -exec rm -f {} + || exit 2
	find . -path "./volumes/storage" -prune -o -type f -name ".coverage*" -print -exec rm -f {} + || exit 2

	find . -path "./volumes/storage" -prune -o -type d -name ".benchmarks" -exec rm -rfv {} + || exit 2
	find . -path "./volumes/storage" -prune -o -type d -name ".pytest_cache" -exec rm -rfv {} + || exit 2
	find . -path "./volumes/storage" -prune -o -type d -name "__pycache__" -exec rm -rfv {} + || exit 2


	local _is_docker_running=false
	if command -v docker >/dev/null 2>&1 && docker info > /dev/null 2>&1; then
		_is_docker_running=true
	fi

	if [ "${_is_docker_running}" == true ]; then
		if docker compose ps | grep 'Up' > /dev/null 2>&1; then
			echo "[WARN]: Docker container is running, please stop it before cleaning." >&2
			exit 1
		fi
	fi


	if [ "${_IS_ALL}" == true ]; then
		if [ "${_is_docker_running}" == true ]; then
			docker compose down -v --remove-orphans || exit 2
		fi

		rm -rf ./volumes/.vscode-server/* || {
			sudo rm -rf ./volumes/.vscode-server/* || exit 2
		}

		rm -rfv ./data || {
			sudo rm -rfv ./data || exit 2
		}
		find ./volumes/storage -type d -name "data" -exec rm -rfv {} + || {
			sudo find ./volumes/storage -type d -name "data" -exec rm -rfv {} + || exit 2
		}

		rm -rfv ./logs || {
			sudo rm -rfv ./logs || exit 2
		}
		find ./volumes/storage -type d -name "logs" -exec rm -rfv {} + || {
			sudo find ./volumes/storage -type d -name "logs" -exec rm -rfv {} + || exit 2
		}
	fi

	echo "[OK]: Done."
}

main
## --- Main --- ##
