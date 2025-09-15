from pydantic import validate_call

from api.core.constants import ErrorCodeEnum, WarnEnum
from api.core import utils
from api.core.exceptions import BaseHTTPException
from api.logger import log_mode

from .schemas import TaskPM, TaskBasePM


# NOTE: This is a mock database for demonstration purposes.
_TASKS_DB: list[TaskPM] = []
for _i in range(1, 101):
    _task = TaskPM(name=f"Task {_i}", point=_i)
    _TASKS_DB.append(_task)


@validate_call
def get_list(
    request_id: str,
    offset: int = 0,
    limit: int = 100,
    is_desc: bool = True,
    warn_mode: WarnEnum = WarnEnum.IGNORE,
) -> tuple[list[TaskPM], int]:
    """Get list of tasks and total count.

    Args:
        request_id    (str         , required): ID of the request.
        offset        (int         , optional): Offset of the query. Defaults to 0.
        limit         (int         , optional): Limit of the query. Defaults to 100.
        is_desc       (bool        , optional): Is descending or ascending. Defaults to True.
        warn_mode     (WarnEnum    , optional): Warning mode. Defaults to `WarnEnum.IGNORE`.

    Returns:
        Tuple[List[TaskPM], int]: List of tasks and total count as tuple.
    """

    log_mode(message=f"[{request_id}] - Getting task list...", warn_mode=warn_mode)

    _task_list: list[TaskPM] = _TASKS_DB
    _all_count = len(_task_list)
    if is_desc:
        _task_list = _task_list[::-1]

    _task_list = _task_list[offset : offset + limit]  # noqa: E203

    log_mode(
        message=f"[{request_id}] - Successfully retrieved task list.",
        level="SUCCESS",
        warn_mode=warn_mode,
    )
    return _task_list, _all_count


@validate_call
def create(
    request_id: str, task_in: TaskBasePM, warn_mode: WarnEnum = WarnEnum.IGNORE
) -> TaskPM:
    """Create a new task.

    Args:
        request_id    (str         , required): ID of the request.
        task_in       (TaskBasePM  , required): New task data to create.
        warn_mode     (WarnEnum    , optional): Warning mode. Defaults to `WarnEnum.IGNORE`.

    Returns:
        TaskPM: New TaskPM object.
    """

    log_mode(message=f"[{request_id}] - Creating task...", warn_mode=warn_mode)

    _task: TaskPM = TaskPM(**task_in.model_dump())
    _TASKS_DB.append(_task)

    log_mode(
        message=f"[{request_id}] - Successfully created task with '{_task.id}' ID.",
        level="SUCCESS",
        warn_mode=warn_mode,
    )

    return _task


@validate_call
def get(
    request_id: str, id: str, warn_mode: WarnEnum = WarnEnum.IGNORE
) -> TaskPM | None:
    """Get task by ID.

    Args:
        request_id    (str         , required): ID of the request.
        id            (str         , required): ID of the task to get.
        warn_mode     (WarnEnum    , optional): Warning mode. Defaults to `WarnEnum.IGNORE`.

    Returns:
        Union[TaskPM, None]: TaskPM object or None.
    """

    log_mode(
        message=f"[{request_id}] - Getting task with '{id}' ID...",
        warn_mode=warn_mode,
    )

    _task: TaskPM | None = None
    for _task_db in _TASKS_DB:
        if _task_db.id == id:
            _task = _task_db

    if _task:
        log_mode(
            message=f"[{request_id}] - Successfully retrieved task with '{id}' ID.",
            level="SUCCESS",
            warn_mode=warn_mode,
        )

    return _task


@validate_call
def update(
    request_id: str,
    id: str,
    warn_mode: WarnEnum = WarnEnum.IGNORE,
    **kwargs,
) -> TaskPM:
    """Update task by ID.

    Args:
        request_id    (str         , required): ID of the request.
        id            (str         , required): ID of the task to update.
        warn_mode     (WarnEnum    , optional): Warning mode. Defaults to `WarnEnum.IGNORE`.
        **kwargs      (dict        , required): Column and value as key-value pair for updating.

    Raises:
        BaseHTTPException: If no task data provided to update.
        BaseHTTPException: If task is not found.

    Returns:
        TaskPM: Updated TaskPM object.
    """

    if not kwargs:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.UNPROCESSABLE_ENTITY,
            message="No task data provided to update!",
        )

    log_mode(
        message=f"[{request_id}] - Updating task with '{id}' ID...",
        warn_mode=warn_mode,
    )

    _task: TaskPM | None = get(request_id=request_id, id=id)

    if not _task:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.NOT_FOUND,
            message=f"Not found task with '{id}' ID!",
        )

    if "id" in kwargs:
        del kwargs["id"]

    for _key, _value in kwargs.items():
        if hasattr(_task, _key):
            setattr(_task, _key, _value)

    _task.updated_at = utils.now_utc_dt()

    log_mode(
        message=f"[{request_id}] - Successfully updated task with '{id}' ID.",
        level="SUCCESS",
        warn_mode=warn_mode,
    )

    return _task


@validate_call
def delete(
    request_id: str,
    id: str,
    warn_mode: WarnEnum = WarnEnum.IGNORE,
) -> None:
    """Delete task by ID.

    Args:
        request_id    (str         , required): ID of the request.
        id            (str         , required): ID of the task to delete.
        warn_mode     (WarnEnum    , optional): Warning mode. Defaults to `WarnEnum.IGNORE`.

    Raises:
        BaseHTTPException: If task is not found.
    """

    log_mode(
        message=f"[{request_id}] - Deleting task with '{id}' ID...", warn_mode=warn_mode
    )

    for _i, _task in enumerate(_TASKS_DB):
        if _task.id == id:
            del _TASKS_DB[_i]

            log_mode(
                message=f"[{request_id}] - Successfully deleted task with '{id}' ID.",
                level="SUCCESS",
                warn_mode=warn_mode,
            )
            return

    raise BaseHTTPException(
        error_enum=ErrorCodeEnum.NOT_FOUND,
        message=f"Not found task with '{id}' ID!",
    )


__all__ = [
    "get_list",
    "create",
    "get",
    "update",
    "delete",
]
