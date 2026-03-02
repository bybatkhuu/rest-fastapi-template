---
title: Quick Start
---

# 🏃 Quick Start

## 1. 🌎 Configure environment variables

[NOTE] Please, check **[environment variables](./configuration.md)** section for more details.

```sh
# Copy '.env.example' file to '.env' file:
cp -v ./.env.example ./.env

# Edit environment variables to fit in your environment:
nano ./.env
```

## 2. 🏁 Start the server

[NOTE] Follow the one of below instructions based on your environment **[A, B, C, D, E]**:

### Docker runtime

**OPTION A.** **[RECOMMENDED]** Run with **docker compose**:

```sh
## 1. Configure 'compose.override.yml' file.
# Copy 'compose.override.[ENV].yml' file to 'compose.override.yml' file:
cp -v ./templates/compose/compose.override.[ENV].yml ./compose.override.yml
# For example, DEVELOPMENT environment:
cp -v ./templates/compose/compose.override.dev.yml ./compose.override.yml
# For example, STATGING or PRODUCTION environment:
cp -v ./templates/compose/compose.override.prod.yml ./compose.override.yml
# Edit 'compose.override.yml' file to fit in your environment:
nano ./compose.override.yml

## 2. Check docker compose configuration is valid:
./compose.sh validate
# Or:
docker compose config

## 3. Start docker compose:
./compose.sh start -l
# Or:
docker compose up -d --remove-orphans --force-recreate && \
    docker compose logs -f --tail 100
```

### Standalone runtime (PM2)

**OPTION B.** Run with **PM2**:

[**IMPORTANT**] Before running, need to install [**PM2**](https://pm2.keymetrics.io/docs/usage/quick-start):

```sh
## 1. Configure PM2 configuration file.
# Copy example PM2 configuration file:
cp -v ./pm2-process.json.example ./pm2-process.json
# Edit PM2 configuration file to fit in your environment:
nano ./pm2-process.json

## 2. Start PM2 process:
pm2 start ./pm2-process.json && \
    pm2 logs --lines 50 ft
```

### Standalone runtime (Python)

**OPTION C.** Run server as **python module**:

```sh
python -u -m src.api
```

**OPTION D.** Run with **uvicorn** cli:

```sh
uvicorn src.api.main:app --host=[BIND_HOST] --port=[PORT] --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"
# For example:
uvicorn src.api.main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"

# For DEVELOPMENT:
uvicorn src.api.main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*" --reload --reload-dir=./src
```

**OPTION E.** Run with **fastapi** cli:

```sh
fastapi run src/api/main.py --host=[BIND_HOST] --port=[PORT] --forwarded-allow-ips="*"
# For example:
fastapi run src/api/main.py --port=8000 --forwarded-allow-ips="*"

# For DEVELOPMENT:
fastapi dev src/api/main.py --host="0.0.0.0" --port=8000 --forwarded-allow-ips="*"
```

### Run directly from src directory

```sh
# 1. Prepare environment variables:
# 1.a. Copy '.env.example' file into 'src' directory as '.env' file:
cp -v ./.env.example ./src/.env
# Edit environment variables to fit in your environment:
nano ./src/.env

# 1.b. Or symbolic link current '.env' file into 'src' directory:
ln -s -v ../.env ./src/.env

# 2. Enter into src directory:
cd src

# 3. Run server:
# 3.a. Run as python module:
python -u -m api

# 3.b. Or run with uvicorn cli:
uvicorn api.main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"
# For DEVELOPMENT:
uvicorn api.main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*" --reload

# 3.c. Or run with fastapi cli:
fastapi run api/main.py --port=8000 --forwarded-allow-ips="*"
# For DEVELOPMENT:
fastapi dev api/main.py --host="0.0.0.0" --port=8000 --forwarded-allow-ips="*"
```

## 3. ✅ Check server is running

Check with CLI (curl):

```sh
# Send a ping request with 'curl' to REST API server and parse JSON response with 'jq':
curl -s http://localhost:8000/api/v1/ping | jq
```

Check with web browser:

- Health check: <http://localhost:8000/api/v1/health>
- Swagger: <http://localhost:8000/docs>
- Redoc: <http://localhost:8000/redoc>
- OpenAPI JSON: <http://localhost:8000/openapi.json>

## 4. 🛑 Stop the server

Docker runtime:

```sh
# Stop docker compose:
./compose.sh stop
# Or:
docker compose down --remove-orphans
```

Standalone runtime (Only for **PM2**):

```sh
pm2 stop ./pm2-process.json && \
    pm2 flush ft && \
    pm2 delete ./pm2-process.json
```

👍
