from fastapi import APIRouter,Depends
from core import db,require
from variance_case import submit,inspect

router=APIRouter(prefix="/wax-batches/{key}/variance")

@router.get("")
def view(key:str,_=Depends(require())):
    with db() as cx:return inspect(cx,key)

@router.post("",status_code=202)
def queue(key:str,_=Depends(require("reviewer"))):
    with db() as cx:return submit(cx,key)
