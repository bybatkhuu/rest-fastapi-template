from datetime import datetime

from pydantic import BaseModel, Field, constr, ConfigDict

from potato_util.dt import now_utc_dt
from potato_util.generator import gen_unique_id


class BasePM(BaseModel):
    # model_config = ConfigDict(json_encoders={datetime: dt_to_iso})
    pass


class ExtraBasePM(BaseModel):
    model_config = ConfigDict(
        extra="allow", json_schema_extra={"additionalProperties": False}
    )


class IdPM(BasePM):
    id: constr(strip_whitespace=True) = Field(  # type: ignore
        default_factory=gen_unique_id,
        min_length=8,
        max_length=64,
        title="ID",
        description="Identifier value of the resource.",
        examples=["res1701388800_dc2cc6c9033c4837b6c34c8bb19bb289"],
    )


class TimestampPM(BasePM):
    updated_at: datetime = Field(
        default_factory=now_utc_dt,
        title="Updated datetime",
        description="Last updated datetime of the resource.",
        examples=["2024-12-01T00:00:00+00:00"],
    )
    created_at: datetime = Field(
        default_factory=now_utc_dt,
        title="Created datetime",
        description="Created datetime of the resource.",
        examples=["2024-12-01T00:00:00+00:00"],
    )


__all__ = [
    "BasePM",
    "ExtraBasePM",
    "IdPM",
    "TimestampPM",
]
