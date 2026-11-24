from typing import Annotated,Literal
from pydantic import BaseModel,StringConstraints

class Dispatch(BaseModel):
    decision:Literal['release','recheck']
    destination:Annotated[str,StringConstraints(strip_whitespace=True,min_length=2,max_length=48)]
    note:Annotated[str,StringConstraints(strip_whitespace=True,min_length=6,max_length=200)]
