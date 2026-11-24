from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints

Bench = Literal["A", "B", "C"]


class Hold(BaseModel):
    bench: Bench
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=6, max_length=200)]


class BenchHold(BaseModel):
    bench: Bench
    batches: Annotated[list[str], Field(min_length=1, max_length=100)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=6, max_length=200)]
