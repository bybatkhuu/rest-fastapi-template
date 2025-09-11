---
title: "Quick Start"
---

# 🏃 Quick Start

## 1. 🌎 Configure environment variables

[NOTE] Please, check **[environment variables](./configuration.md)** section for more details.

### **OPTION A.** **[RECOMMENDED]** For **docker** runtime **[5.A]**

```sh
# Copy '.env.example' file to '.env' file:
cp -v ./.env.example ./.env

# Edit environment variables to fit in your environment:
nano ./.env
```

### **OPTION B.** For **standalone** runtime **[5.B ~ 5.F]**

```sh
# Copy '.env.example' file to '.env' file:
cp -v ./.env.example ./src/.env

# Edit environment variables to fit in your environment:
nano ./src/.env
```

## 2. 🏁 Start the server

[NOTE] Follow the one of below instructions based on your environment **[A, B, C, D, E, F]**:

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

**OPTION C.** Run server as **python script**:

```sh
cd src
python -u ./main.py
```

**OPTION D.** Run server as **python module**:

```sh
python -u -m src.api

# Or:
cd src
python -u -m api
```

**OPTION E.** Run with **uvicorn** cli:

```sh
uvicorn src.main:app --host=[BIND_HOST] --port=[PORT] --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"
# For example:
uvicorn src.main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"


# Or:
cd src
uvicorn main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*"

# For DEVELOPMENT:
uvicorn main:app --host="0.0.0.0" --port=8000 --no-access-log --no-server-header --proxy-headers --forwarded-allow-ips="*" --reload --reload-include="*.yml" --reload-include=".env"
```

**OPTION F.** Run with **fastapi** cli:

```sh
fastpi run src/main.py --host=[BIND_HOST] --port=[PORT]
# For example:
fastapi run src/main.py --port=8000

# For DEVELOPMENT:
fastapi dev src/main.py --host="0.0.0.0" --port=8000


# Or:
cd src
fastapi run --port=8000

# For DEVELOPMENT:
fastapi dev --host="0.0.0.0" --port=8000
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
    pm2 flush && \
    pm2 delete ./pm2-process.json
```

👍
