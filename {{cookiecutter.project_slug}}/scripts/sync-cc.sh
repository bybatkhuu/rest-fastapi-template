#!/bin/bash
set -euo pipefail


## --- Base --- ##
# Getting path of this script file:
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
_PROJECT_DIR="$(cd "${_SCRIPT_DIR}/.." >/dev/null 2>&1 && pwd)"
cd "${_PROJECT_DIR}" || exit 2

# Loading base script:
# shellcheck disable=SC1091
source ./scripts/base.sh

# Checking 'rsync' is installed or not:
if [ -z "$(which rsync)" ]; then
	echoError "'rsync' not found or not installed."
	exit 1
fi

# Loading .env file (if exists):
if [ -f ".env" ]; then
	# shellcheck disable=SC1091
	source .env
fi
## --- Base --- ##


## --- Variables --- ##
# Load from environment variables:
PROJECT_SLUG="${PROJECT_SLUG:-{{cookiecutter.project_slug}}}"
## --- Variables --- ##


## --- Main --- ##
main()
{
	## --- Menu arguments --- ##
	if [ -n "${1:-}" ]; then
		for _input in "${@:-}"; do
			case ${_input} in
				-p=* | --project-slug=*)
					PROJECT_SLUG="${_input#*=}"
					shift;;
				*)
					echoError "Failed to parsing input -> ${_input}"
					echoInfo "USAGE: ${0}  -p=*, --project-slug=*"
					exit 1;;
			esac
		done
	fi
	## --- Menu arguments --- ##


	if [ ! -d "${PROJECT_SLUG}" ]; then
		echoError "Not found '${PROJECT_SLUG}' directory!"
		exit 1
	fi

	echoInfo "Syncing files..."
	rsync -av "./${PROJECT_SLUG}/" ./
	echoOk "Done."
}

main "${@:-}"
## --- Main --- ##
