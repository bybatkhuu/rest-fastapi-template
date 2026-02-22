#!/usr/bin/env python

# Standard libraries
import sys
import logging
import pprint
import asyncio
from typing import Any

# Third-party libraries
import aiohttp

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S %z",
        format="[%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d]: %(message)s",
    )

    _base_url = "http://localhost:8000"
    _api_prefix = "/api/v1"
    _endpoint = "/ping"
    _method = "GET"

    _url = f"{_base_url}{_api_prefix}{_endpoint}"
    _payload = {}
    _headers = {"Accept": "application/json"}

    logger.info("Sending request...")
    _result_dict: dict[str, Any] = {}
    async with aiohttp.ClientSession() as _http_session:
        async with _http_session.request(
            method=_method, url=_url, headers=_headers, json=_payload
        ) as _response:
            _result_dict = await _response.json()
    logger.info("Done!\n")

    logging.info(f"\n{pprint.pformat(_result_dict)}")
    return


if __name__ == "__main__":
    asyncio.run(main())
