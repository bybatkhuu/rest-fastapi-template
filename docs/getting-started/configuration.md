---
title: Configuration
---

# ⚙️ Configuration

## 🌎 Environment Variables

[**`.env.example`**](https://github.com/bybatkhuu/rest-fastapi-template/blob/main/.env.example):

```sh
--8<-- "./.env.example"
```

## 🐳 Docker compose override

You can copy the following **`compose.override.yml`** files to your project root directory (which is **`compose.yml`** located) and you can modify it fit your environment. It will override, update or extend the default **`compose.yml`** file.

- For **DEVELOPMENT**: [**`compose.override.dev.yml`**](https://github.com/bybatkhuu/rest-fastapi-template/blob/main/templates/compose/compose.override.dev.yml)

```yaml
--8<-- "./templates/compose/compose.override.dev.yml"
```

- For **DEVELOPMENT** with **GPU**: [**`compose.override.dev.gpu.yml`**](https://github.com/bybatkhuu/rest-fastapi-template/blob/main/templates/compose/compose.override.dev.gpu.yml)

```yaml
--8<-- "./templates/compose/compose.override.dev.gpu.yml"
```

- For **PRODUCTION**: [**`compose.override.prod.yml`**](https://github.com/bybatkhuu/rest-fastapi-template/blob/main/templates/compose/compose.override.prod.yml)

```yaml
--8<-- "./templates/compose/compose.override.prod.yml"
```

- For **PRODUCTION** with **GPU**: [**`compose.override.prod.gpu.yml`**](https://github.com/bybatkhuu/rest-fastapi-template/blob/main/templates/compose/compose.override.prod.gpu.yml)

```yaml
--8<-- "./templates/compose/compose.override.prod.gpu.yml"
```
