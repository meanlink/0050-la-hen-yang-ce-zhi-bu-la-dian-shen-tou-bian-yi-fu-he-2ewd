from fastapi import APIRouter,Depends
from core import db,require
from caliper_input import Pair
from pair_ledger import note

router=APIRouter(prefix="/wax-batches/{key}/readings")

@router.put("")
def save(key:str,body:Pair,_=Depends(require("operator"))):
    with db() as cx: return note(cx,key,body)
