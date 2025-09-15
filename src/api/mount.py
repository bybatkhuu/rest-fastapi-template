from pydantic import validate_call
from fastapi import FastAPI


@validate_call(config={"arbitrary_types_allowed": True})
def add_mounts(app: FastAPI) -> None:
    """Add mounts to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    # Add mounts here

    return


__all__ = ["add_mounts"]
