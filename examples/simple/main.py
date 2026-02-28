#!/usr/bin/env python

# Standard libraries
import sys
import logging
import pprint
from typing import Any

# Third-party libraries
import requests

logger = logging.getLogger(__name__)


def main() -> None:
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
    response = requests.request(
        method=_method, url=_url, headers=_headers, data=_payload
    )
    _result_dict = response.json()
    logger.info("Done!\n")

    logger.info(f"\n{pprint.pformat(_result_dict)}")
    return


if __name__ == "__main__":
    main()
