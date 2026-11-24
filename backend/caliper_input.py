from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel,Field

Depth=Annotated[Decimal,Field(ge=0,le=8,decimal_places=2)]
class Pair(BaseModel):
    seam:str=Field(pattern=r"^[A-Z0-9-]{2,12}$")
    first:Depth
    second:Depth
