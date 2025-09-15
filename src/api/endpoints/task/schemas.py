from typing_extensions import Self

from pydantic import Field, model_validator, ConfigDict

from api.core.constants import ALPHANUM_EXTEND_REGEX
from api.config import config
from api.core.schemas import IdPM, TimestampPM, BasePM, BaseResPM, LinksResPM


_tasks_base_url = f"{config.api.prefix}/tasks"


# Tasks
class TaskBasePM(BasePM):
    name: str = Field(
        ...,
        min_length=2,
        max_length=64,
        pattern=ALPHANUM_EXTEND_REGEX,
        title="Task name",
        description="Name of the task.",
        examples=["Task 1"],
    )
    point: int = Field(
        default=70,
        ge=0,
        le=100,
        title="Task point",
        description="Point of the task.",
        examples=[70],
    )


class TaskUpPM(TaskBasePM):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=64,
        pattern=ALPHANUM_EXTEND_REGEX,
        title="Task name",
        description="Name of the task.",
        examples=["Task 1"],
    )


class TaskPM(TimestampPM, TaskBasePM, IdPM):
    model_config = ConfigDict(from_attributes=True)


class TasksPM(TaskPM):
    links: LinksResPM = Field(
        default_factory=LinksResPM,
        title="Links",
        description="Links related to the current task.",
        examples=[
            {
                "self": f"{_tasks_base_url}/1699928748406212_46D46E7E55FA4A6E8478BD6B04195793"
            }
        ],
    )

    @model_validator(mode="after")
    def _check_all(self) -> Self:
        self.links.self_link = f"{_tasks_base_url}/{self.id}"
        return self


class ResTaskPM(BaseResPM):
    data: TaskPM | None = Field(
        default=None,
        title="Task data",
        description="Task as a main data.",
        examples=[
            {
                "id": "1699928748406212_46D46E7E55FA4A6E8478BD6B04195793",
                "name": "Task 1",
                "point": 70,
                "updated_at": "2021-01-01T00:00:00+00:00",
                "created_at": "2021-01-01T00:00:00+00:00",
            }
        ],
    )


class ResTasksPM(BaseResPM):
    data: list[TasksPM] = Field(
        default=[],
        title="List of tasks",
        description="List of tasks as main data.",
        examples=[
            [
                {
                    "id": "1699928748406212_46D46E7E55FA4A6E8478BD6B04195793",
                    "name": "Task 1",
                    "point": 70,
                    "updated_at": "2021-01-01T00:00:00+00:00",
                    "created_at": "2021-01-01T00:00:00+00:00",
                    "links": {
                        "self": f"{_tasks_base_url}/1699928748406212_46D46E7E55FA4A6E8478BD6B04195793"
                    },
                },
                {
                    "id": "1699854600504660_337FC34BE4304E14A193F6A2793AD9D1",
                    "name": "Task 2",
                    "point": 30,
                    "updated_at": "2021-01-01T00:00:00+00:00",
                    "created_at": "2021-01-01T00:00:00+00:00",
                    "links": {
                        "self": f"{_tasks_base_url}/1699854600504660_337FC34BE4304E14A193F6A2793AD9D1"
                    },
                },
            ]
        ],
    )


# Tasks


__all__ = [
    "TaskBasePM",
    "TaskUpPM",
    "TaskPM",
    "ResTaskPM",
    "ResTasksPM",
]
