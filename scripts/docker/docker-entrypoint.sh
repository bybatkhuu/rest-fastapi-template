#!/usr/bin/env bash
set -euo pipefail


echo "[INFO]: Running '${FT_API_SLUG}' docker-entrypoint.sh..."


_run()
{
	exec gosu "${USER}:${GROUP}" python -m api || exit 2
	# exec gosu "${USER}:${GROUP}" uvicorn api.main:app \
	# 	--host=0.0.0.0 \
	# 	--port=${FT_API_PORT:-8000} \
	# 	--no-access-log \
	# 	--no-server-header \
	# 	--proxy-headers \
	# 	--forwarded-allow-ips='*' || exit 2
	exit 0
}


main()
{
	umask 0002 || exit 2

	find "${FT_HOME_DIR}" \
		"${FT_API_CONFIGS_DIR}" \
		"${FT_API_DATA_DIR}" \
		"${FT_API_LOGS_DIR}" \
		"${FT_API_TMP_DIR}" \
		\( \
			-type d -name ".git" -o \
			-type d -name ".venv" -o \
			-type d -name "venv" -o \
			-type d -name "env" -o \
			-type d -name "modules" -o \
			-type d -name "volumes" -o \
			-type l -name ".env" \
		\) -prune -o -print0 | \
			xargs -0 chown -c "${USER}:${GROUP}" || exit 2

	find "${FT_API_DIR}" "${FT_API_CONFIGS_DIR}" "${FT_API_DATA_DIR}" \
		\( \
			-type d -name ".git" -o \
			-type d -name ".venv" -o \
			-type d -name "venv" -o \
			-type d -name "env" -o \
			-type d -name "scripts" -o \
			-type d -name "modules" -o \
			-type d -name "volumes" \
		 \) -prune -o -type d -exec \
			chmod 770 {} + || exit 2

	find "${FT_API_DIR}" "${FT_API_CONFIGS_DIR}" "${FT_API_DATA_DIR}" \
		\( \
			-type d -name ".git" -o \
			-type d -name ".venv" -o \
			-type d -name "venv" -o \
			-type d -name "env" -o \
			-type d -name "scripts" -o \
			-type d -name "modules" -o \
			-type d -name "volumes" -o \
			-type l -name ".env" -o \
			-type f -name "main.py" \
		\) -prune -o -type f -exec \
			chmod 660 {} + || exit 2

	find "${FT_API_DIR}" "${FT_API_CONFIGS_DIR}" "${FT_API_DATA_DIR}" \
		\( \
			-type d -name ".git" -o \
			-type d -name ".venv" -o \
			-type d -name "venv" -o \
			-type d -name "env" -o \
			-type d -name "scripts" -o \
			-type d -name "modules" -o \
			-type d -name "volumes" \
		\) -prune -o -type d -exec \
			chmod ug+s {} + || exit 2

	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type d -exec chmod 775 {} + || exit 2
	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type f -exec chmod 664 {} + || exit 2
	find "${FT_API_LOGS_DIR}" "${FT_API_TMP_DIR}" -type d -exec chmod +s {} + || exit 2

	# echo "${USER} ALL=(ALL) ALL" | tee -a "/etc/sudoers.d/${USER}" > /dev/null || exit 2
	echo ""

	## Parsing input:
	case ${1:-} in
		"" | -s | --start | start | --run | run)
			_run;;
			# shift;;
		-b | --bash | bash | /bin/bash)
			shift
			if [ -z "${*:-}" ]; then
				echo "[INFO]: Starting bash..."
				exec gosu "${USER}:${GROUP}" /bin/bash
			else
				echo "[INFO]: Executing command -> ${*}"
				exec gosu "${USER}:${GROUP}" /bin/bash -c "${@}" || exit 2
			fi
			exit 0;;
		*)
			echo "[ERROR]: Failed to parsing input -> ${*}!" >&2
			echo "[INFO]: USAGE: ${0}  -s, --start, start | -b, --bash, bash, /bin/bash"
			exit 1;;
	esac
}

main "${@:-}"
