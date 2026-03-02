# syntax=docker/dockerfile:1
# check=skip=SecretsUsedInArgOrEnv

# ARG BASE_IMAGE=ubuntu:22.04
ARG BASE_IMAGE=ubuntu:24.04
# ARG BASE_IMAGE=nvidia/cuda:11.0.3-cudnn8-runtime-ubuntu20.04
# ARG BASE_IMAGE=nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04
# ARG BASE_IMAGE=nvidia/cuda:12.0.1-cudnn8-runtime-ubuntu22.04
# ARG BASE_IMAGE=nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04
# ARG BASE_IMAGE=nvidia/cuda:13.0.0-cudnn-runtime-ubuntu24.04
# ARG BASE_IMAGE=nvidia/cuda:13.0.0-tensorrt-runtime-ubuntu24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG {{cookiecutter.env_prefix}}API_SLUG="{{cookiecutter.project_slug}}"


## Here is the builder image:
FROM ${BASE_IMAGE} AS builder

ARG BASE_IMAGE
ARG DEBIAN_FRONTEND
ARG {{cookiecutter.env_prefix}}API_SLUG

ARG PYTHON_VERSION={{cookiecutter.python_version}}

ENV	UV_LINK_MODE=copy

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR "/usr/src/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"

RUN --mount=type=cache,target=/opt/conda/pkgs,sharing=private \
	--mount=type=cache,target=/root/.cache,sharing=locked \
	_BUILD_TARGET_ARCH=$(uname -m) && \
    echo "BUILDING TARGET ARCHITECTURE: ${_BUILD_TARGET_ARCH}" && \
	rm -rfv /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* && \
	apt-get clean -y && \
	# echo "Acquire::http::Pipeline-Depth 0;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	# echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	# echo "Acquire::BrokenProxy true;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	apt-get update --fix-missing -o Acquire::CompressionTypes::Order::=gz && \
	apt-get install -y --no-install-recommends \
		ca-certificates \
		build-essential \
		wget && \
	_MINICONDA_VERSION=py310_25.11.1-1 && \
	if [ "${_BUILD_TARGET_ARCH}" == "x86_64" ]; then \
		_MINICONDA_FILENAME=Miniconda3-${_MINICONDA_VERSION}-Linux-x86_64.sh && \
		export _MINICONDA_URL=https://repo.anaconda.com/miniconda/${_MINICONDA_FILENAME}; \
	elif [ "${_BUILD_TARGET_ARCH}" == "aarch64" ]; then \
		_MINICONDA_FILENAME=Miniconda3-${_MINICONDA_VERSION}-Linux-aarch64.sh && \
		export _MINICONDA_URL=https://repo.anaconda.com/miniconda/${_MINICONDA_FILENAME}; \
	else \
		echo "Unsupported platform: ${_BUILD_TARGET_ARCH}" && \
		exit 1; \
	fi && \
	if [ ! -f "/root/.cache/${_MINICONDA_FILENAME}" ]; then \
		wget -nv --show-progress --progress=bar:force:noscroll "${_MINICONDA_URL}" -O "/root/.cache/${_MINICONDA_FILENAME}"; \
	fi && \
	/bin/bash "/root/.cache/${_MINICONDA_FILENAME}" -bu -p /opt/conda && \
	/opt/conda/condabin/conda tos accept --override-channels \
		-c https://repo.anaconda.com/pkgs/main \
		-c https://repo.anaconda.com/pkgs/r && \
	/opt/conda/condabin/conda config --append channels conda-forge && \
	/opt/conda/condabin/conda update -y conda && \
	/opt/conda/condabin/conda install -y python=${PYTHON_VERSION} pip && \
	/opt/conda/bin/pip install --timeout 60 -U pip uv

COPY ./requirements* ./
RUN	--mount=type=cache,target=/root/.cache,sharing=locked \
	# _BUILD_TARGET_ARCH=$(uname -m) && \
	# if [ "${_BUILD_TARGET_ARCH}" == "x86_64" ] && [[ "${BASE_IMAGE}" == nvidia/cuda* ]]; then \
	# 	export _REQUIRE_FILE_PATH=./requirements.gpu.txt; \
	# elif [ "${_BUILD_TARGET_ARCH}" == "x86_64" ]; then \
	# 	export _REQUIRE_FILE_PATH=./requirements.amd64.txt; \
	# elif [ "${_BUILD_TARGET_ARCH}" == "aarch64" ]; then \
	# 	export _REQUIRE_FILE_PATH=./requirements.arm64.txt; \
	# fi && \
	# if [ -n "${_REQUIRE_FILE_PATH:-}" ] && [ -f "${_REQUIRE_FILE_PATH}" ]; then \
	# 	/opt/conda/bin/python -m uv pip install -r "${_REQUIRE_FILE_PATH}"; \
	# fi && \
	/opt/conda/bin/python -m uv pip install -r ./requirements.txt


## Here is the base image:
FROM ${BASE_IMAGE} AS base

ARG DEBIAN_FRONTEND
ARG {{cookiecutter.env_prefix}}API_SLUG

ARG {{cookiecutter.env_prefix}}HOME_DIR="/app"
ARG {{cookiecutter.env_prefix}}API_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}HOME_DIR}/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"
ARG {{cookiecutter.env_prefix}}API_CONFIGS_DIR="/etc/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"
ARG {{cookiecutter.env_prefix}}API_DATA_DIR="/var/lib/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"
ARG {{cookiecutter.env_prefix}}API_LOGS_DIR="/var/log/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"
ARG {{cookiecutter.env_prefix}}API_TMP_DIR="/tmp/{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}"
# ARG {{cookiecutter.env_prefix}}API_MODELS_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}/models"
ARG {{cookiecutter.env_prefix}}API_PORT=8000
ARG {{cookiecutter.env_prefix}}API_DOCS_ENABLED=false
## echo "{{cookiecutter.env_prefix}}USER_PASSWORD123" | openssl passwd -6 -stdin
ARG HASH_PASSWORD="\$6\$eSagViAo6pFQdS4Z\$j4shoN7RMcC/n1U4AO4TcQmDYQJjvoy4LnUcs/kPY8kg59BNSsoUXRI6w2U1yIq0/Mst0plVRBnAxdZ47w.73/"
ARG UID=1000
ARG GID=11000
ARG USER={{cookiecutter.project_abbr}}-user
ARG GROUP={{cookiecutter.project_abbr}}-group

# ENV {{cookiecutter.env_prefix}}API_MODELS_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_MODELS_DIR}"
ENV {{cookiecutter.env_prefix}}API_SLUG="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_SLUG}" \
	{{cookiecutter.env_prefix}}HOME_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}HOME_DIR}" \
	{{cookiecutter.env_prefix}}API_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" \
	{{cookiecutter.env_prefix}}API_CONFIGS_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_CONFIGS_DIR}" \
	{{cookiecutter.env_prefix}}API_DATA_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" \
	{{cookiecutter.env_prefix}}API_LOGS_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" \
	{{cookiecutter.env_prefix}}API_TMP_DIR="{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" \
	{{cookiecutter.env_prefix}}API_PORT={% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT} \
	{{cookiecutter.env_prefix}}API_DOCS_ENABLED={% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DOCS_ENABLED} \
	UID=${UID} \
	GID=${GID} \
	USER=${USER} \
	GROUP=${GROUP} \
	PYTHONIOENCODING=utf-8 \
	PYTHONUNBUFFERED=1 \
	PATH="/opt/conda/bin:${PATH}"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN --mount=type=secret,id=HASH_PASSWORD \
	rm -vrf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* /root/.cache/* && \
	apt-get clean -y && \
	# echo "Acquire::http::Pipeline-Depth 0;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	# echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	# echo "Acquire::BrokenProxy true;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
	apt-get update --fix-missing -o Acquire::CompressionTypes::Order::=gz && \
	apt-get install -y --no-install-recommends \
		sudo \
		gosu \
		locales \
		tzdata \
		procps \
		iputils-ping \
		iproute2 \
		curl \
		nano && \
	apt-get clean -y && \
	sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
	sed -i -e 's/# en_AU.UTF-8 UTF-8/en_AU.UTF-8 UTF-8/' /etc/locale.gen && \
	sed -i -e 's/# ko_KR.UTF-8 UTF-8/ko_KR.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales && \
	update-locale LANG=en_US.UTF-8 && \
	echo "LANGUAGE=en_US.UTF-8" >> /etc/default/locale && \
	echo "LC_ALL=en_AU.UTF-8" >> /etc/default/locale && \
	# addgroup --gid ${GID} ${GROUP} && \
	# useradd -lmN -d "/home/${USER}" -s /bin/bash -g ${GROUP} -G sudo -u ${UID} ${USER} && \
	groupadd --gid ${GID} ${GROUP} && \
	usermod -l ${USER} -m -d /home/${USER} -s /bin/bash -g ${GROUP} -aG sudo ubuntu && \
	# echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
	# chmod 0440 "/etc/sudoers.d/${USER}" && \
	if [ -f "/run/secrets/HASH_PASSWORD" ]; then \
		echo "Using hashed password from secret: /run/secrets/HASH_PASSWORD"; \
		echo -e "${USER}:$(cat /run/secrets/HASH_PASSWORD)" | chpasswd -e; \
	else \
		echo "Using hashed password from build argument: HASH_PASSWORD"; \
		echo -e "${USER}:${HASH_PASSWORD}" | chpasswd -e; \
	fi && \
	echo -e "\nalias ls='ls -aF --group-directories-first --color=auto'" >> /root/.bashrc && \
	echo -e "alias ll='ls -alhF --group-directories-first --color=auto'\n" >> /root/.bashrc && \
	echo -e "\numask 0002" >> "/home/${USER}/.bashrc" && \
	echo "alias ls='ls -aF --group-directories-first --color=auto'" >> "/home/${USER}/.bashrc" && \
	echo -e "alias ll='ls -alhF --group-directories-first --color=auto'\n" >> "/home/${USER}/.bashrc" && \
	echo ". /opt/conda/etc/profile.d/conda.sh" >> "/home/${USER}/.bashrc" && \
	echo "conda activate base" >> "/home/${USER}/.bashrc" && \
	rm -rfv /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/* /root/.cache/* "/home/${USER}/.cache/*" && \
	mkdir -pv "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_CONFIGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" && \
	chown -Rc "${USER}:${GROUP}" \
		"{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}HOME_DIR}" \
		"{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_CONFIGS_DIR}" \
		"{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" \
		"{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" \
		"{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" && \
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_CONFIGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" -type d -exec chmod -c 770 {} + && \
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_CONFIGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}" -type d -exec chmod -c ug+s {} + && \
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" -type d -exec chmod -c 775 {} + && \
	find "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_LOGS_DIR}" "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_TMP_DIR}" -type d -exec chmod -c +s {} +

ENV	LANG=en_US.UTF-8 \
	LANGUAGE=en_US.UTF-8 \
	LC_ALL=en_AU.UTF-8

COPY --from=builder --chown=${UID}:${GID} /opt/conda /opt/conda


## Here is the final image:
FROM base AS app

WORKDIR "{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}"
COPY --chown=${UID}:${GID} ./src {% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DIR}
COPY --chown=${UID}:${GID} --chmod=770 ./scripts/docker/*.sh /usr/local/bin/

# VOLUME ["{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_DATA_DIR}"]
# EXPOSE {% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT}

# USER ${UID}:${GID}
# HEALTHCHECK --start-period=30s --start-interval=1s --interval=5m --timeout=5s --retries=3 \
# 	CMD curl -f http://localhost:{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT}/api/v{% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_VERSION:-1}/ping || exit 1

ENTRYPOINT ["docker-entrypoint.sh"]
# CMD ["-b", "uvicorn api.main:app --host=0.0.0.0 --port={% raw %}${{% endraw %}{{cookiecutter.env_prefix}}API_PORT:-8000} --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips='*'"]
