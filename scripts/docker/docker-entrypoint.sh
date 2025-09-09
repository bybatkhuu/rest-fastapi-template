#!/bin/bash
set -euo pipefail


echo "[INFO]: Running 'rest.fastapi-template' docker-entrypoint.sh..."

_doStart()
{
	exec python -u ./main.py || exit 2
	# exec uvicorn main:app --host=0.0.0.0 --port=${FT_API_PORT:-8000} --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips='*' || exit 2
	exit 0
}


main()
{
	umask 0002 || exit 2
	find "${FT_HOME_DIR}" "${FT_API_DATA_DIR}" "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -path "*/modules" -prune -o -name ".env" -o -print0 | sudo xargs -0 chown -c "${USER}:${GROUP}" || exit 2
	find "${FT_API_DIR}" "${FT_API_DATA_DIR}" -type d -not -path "*/modules/*" -exec chmod 770 {} + || exit 2
	find "${FT_API_DIR}" "${FT_API_DATA_DIR}" -type f -not -path "*/modules/*" -exec chmod 660 {} + || exit 2
	find "${FT_API_DIR}" "${FT_API_DATA_DIR}" -type d -not -path "*/modules/*" -exec chmod ug+s {} + || exit 2
	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type d -exec chmod 775 {} + || exit 2
	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type f -exec chmod 664 {} + || exit 2
	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type d -exec chmod +s {} + || exit 2
	chmod ug+x "${FT_API_DIR}/main.py" || exit 2
	# echo "${USER} ALL=(ALL) ALL" | sudo tee -a "/etc/sudoers.d/${USER}" > /dev/null || exit 2
	echo ""

	## Parsing input:
	case ${1:-} in
		"" | -s | --start | start | --run | run)
			_doStart;;
			# shift;;
		-b | --bash | bash | /bin/bash)
			shift
			if [ -z "${*:-}" ]; then
				echo "[INFO]: Starting bash..."
				/bin/bash
			else
				echo "[INFO]: Executing command -> ${*}"
				exec /bin/bash -c "${@}" || exit 2
			fi
			exit 0;;
		*)
			echo "[ERROR]: Failed to parsing input -> ${*}!"
			echo "[INFO]: USAGE: ${0}  -s, --start, start | -b, --bash, bash, /bin/bash"
			exit 1;;
	esac
}

main "${@:-}"
