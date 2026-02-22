from fastapi import APIRouter, Request, Path, Body, Query, HTTPException
from pydantic import constr

from api.core.constants import ALPHANUM_HYPHEN_REGEX, ErrorCodeEnum
from api.core import utils
from api.core.exceptions import BaseHTTPException
from api.core.responses import BaseResponse
from api.logger import logger

from .schemas import TaskBasePM, TaskPM, TaskUpPM, ResTaskPM, ResTasksPM
from . import service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    "/",
    summary="Get Task List",
    response_model=ResTasksPM,
    responses={422: {}},
)
def get_tasks(
    request: Request,
    skip: int = Query(
        default=0,
        ge=0,
        title="Skip",
        description="Number of data to skip.",
        examples=[0],
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100000,
        title="Limit",
        description="Limit of data list.",
        examples=[100],
    ),
    is_desc: bool = Query(
        default=True,
        title="Sort Direction",
        description="Is sort descending or ascending.",
        examples=[True],
    ),
):
    _request_id = request.state.request_id
    logger.info(f"[{_request_id}] - Getting task list...")

    _message = "Not found any task!"
    _task_list: list[TaskPM] = []
    _links = {
        "first": None,
        "prev": None,
        "next": None,
        "last": None,
    }
    _list_count = 0
    _all_count = 0
    try:
        _result_tuple: tuple[list[TaskPM], int] = service.get_list(
            request_id=_request_id, offset=skip, limit=(limit + 1), is_desc=is_desc
        )
        _task_list, _all_count = _result_tuple

        _url = request.url.remove_query_params(["skip", "limit", "is_desc"])

        if 0 < _all_count:
            _links["first"] = utils.get_relative_url(
                _url.include_query_params(skip=0, limit=limit, is_desc=is_desc)
            )

            _last_skip = max((_all_count - 1) // limit * limit, 0)
            _links["last"] = utils.get_relative_url(
                _url.include_query_params(skip=_last_skip, limit=limit, is_desc=is_desc)
            )

        if 0 < skip:
            _prev_skip = max(skip - limit, 0)
            _links["prev"] = utils.get_relative_url(
                _url.include_query_params(skip=_prev_skip, limit=limit, is_desc=is_desc)
            )

        if limit < len(_task_list):
            _task_list = _task_list[:limit]
            _links["next"] = utils.get_relative_url(
                _url.include_query_params(
                    skip=(skip + limit), limit=limit, is_desc=is_desc
                )
            )

        _list_count = len(_task_list)
        if 0 < _list_count:
            _message = "Successfully retrieved task list."

        logger.success(
            f"[{_request_id}] - Successfully retrieved task list count: {len(_task_list)}/{_all_count}."
        )
    except Exception as err:
        if isinstance(err, HTTPException):
            raise

        logger.error(f"[{_request_id}] - Failed to get task list!")
        raise

    _response = BaseResponse(
        request=request,
        message=_message,
        content=_task_list,
        links=_links,
        meta={
            "list_count": _list_count,
            "all_count": _all_count,
        },
        response_schema=ResTasksPM,
    )
    return _response


@router.post(
    "/",
    summary="Create Task",
    status_code=201,
    response_model=ResTaskPM,
    responses={422: {}},
)
def create_task(
    request: Request,
    task_in: TaskBasePM = Body(
        ...,
        title="Task data",
        description="Task data to create.",
    ),
):
    _request_id = request.state.request_id
    logger.info(f"[{_request_id}] - Creating task with '{task_in.name}' name...")

    _task: TaskPM
    try:
        _task: TaskPM = service.create(request_id=_request_id, task_in=task_in)

        logger.success(
            f"[{_request_id}] - Successfully created task with '{_task.id}' ID."
        )
    except Exception as err:
        if isinstance(err, HTTPException):
            raise

        logger.error(
            f"[{_request_id}] - Failed to create task with '{task_in.name}' name!"
        )
        raise

    _response = BaseResponse(
        request=request,
        status_code=201,
        message="Successfully created task.",
        content=_task,
        response_schema=ResTaskPM,
    )
    return _response


@router.get(
    "/{task_id}",
    summary="Get Task",
    response_model=ResTaskPM,
    responses={404: {}, 422: {}},
)
def get_task(
    request: Request,
    task_id: constr(strip_whitespace=True) = Path(  # type: ignore
        ...,
        min_length=8,
        max_length=64,
        pattern=ALPHANUM_HYPHEN_REGEX,
        title="Task ID",
        description="Task ID to get.",
        examples=["1701388800_a0dc99d68d5e427eafe00525fac47012"],
    ),
):
    _request_id = request.state.request_id
    logger.info(f"[{_request_id}] - Getting task with '{task_id}' ID...")

    try:
        _task: TaskPM | None = service.get(request_id=_request_id, id=task_id)

        if not _task:
            raise BaseHTTPException(
                error_enum=ErrorCodeEnum.NOT_FOUND,
                message=f"Not found task with '{id}' ID!",
            )

        logger.success(
            f"[{_request_id}] - Successfully retrieved task with '{task_id}' ID."
        )
    except Exception as err:
        if isinstance(err, HTTPException):
            raise

        logger.error(f"[{_request_id}] - Failed to get task with '{task_id}' ID!")
        raise

    _response = BaseResponse(
        request=request,
        message="Successfully retrieved task info.",
        content=_task,
        response_schema=ResTaskPM,
    )
    return _response


@router.put(
    "/{task_id}",
    summary="Update Task",
    response_model=ResTaskPM,
    responses={404: {}, 422: {}},
)
def update_task(
    request: Request,
    task_id: constr(strip_whitespace=True) = Path(  # type: ignore
        ...,
        min_length=8,
        max_length=64,
        pattern=ALPHANUM_HYPHEN_REGEX,
        title="Task ID",
        description="Task ID to update.",
        examples=["1701388800_cd388fca74de4e8085df41e7c6df762e"],
    ),
    task_up: TaskUpPM = Body(
        ..., title="Task data", description="Task data to update."
    ),
):
    _request_id = request.state.request_id
    logger.info(f"[{_request_id}] - Updating task with '{task_id}' ID...")

    _task: TaskPM
    try:
        _task: TaskPM = service.update(
            request_id=_request_id, id=task_id, **task_up.model_dump(exclude_unset=True)
        )

        logger.success(
            f"[{_request_id}] - Successfully updated task with '{task_id}' ID."
        )
    except Exception as err:

        if isinstance(err, HTTPException):
            raise

        logger.error(f"[{_request_id}] - Failed to update task with '{task_id}' ID!")
        raise

    _response = BaseResponse(
        request=request,
        message="Successfully updated task.",
        content=_task,
        response_schema=ResTaskPM,
    )
    return _response


@router.delete(
    "/{task_id}",
    summary="Delete Task",
    status_code=204,
    responses={404: {}, 422: {}},
)
def delete_task(
    request: Request,
    task_id: str = Path(
        ...,
        min_length=8,
        max_length=64,
        pattern=ALPHANUM_HYPHEN_REGEX,
        title="Task ID",
        description="Task ID to delete.",
        examples=["1701388800_cd388fca74de4e8085df41e7c6df762e"],
    ),
):
    _request_id = request.state.request_id
    logger.info(f"[{_request_id}] - Deleting task with '{task_id}' ID...")

    try:
        service.delete(request_id=_request_id, id=task_id)

        logger.success(
            f"[{_request_id}] - Successfully deleted task with '{task_id}' ID."
        )
    except Exception as err:

        if isinstance(err, HTTPException):
            raise

        logger.error(f"[{_request_id}] - Failed to delete task with '{task_id}' ID!")
        raise

    return


__all__ = ["router"]
