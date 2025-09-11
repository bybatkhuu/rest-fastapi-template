---
title: Examples
---

# 🚸 Examples

## CLI

Send request to the server using `curl` and parse the response using `jq`:

```sh
curl -s http://localhost:8000/api/v1/ping | jq
```

## Simple

Using python `requests` library to send request to the server:

[**`examples/simple/main.py`**](https://github.com/bybatkhuu/rest.fastapi-template/blob/main/examples/simple/main.py):

```python
--8<-- "./examples/simple/main.py"
```

## Async

Using python `aiohttp` library to send request to the server:

[**`examples/async/main.py`**](https://github.com/bybatkhuu/rest.fastapi-template/blob/main/examples/async/main.py):

```python
--8<-- "./examples/async/main.py"
```
