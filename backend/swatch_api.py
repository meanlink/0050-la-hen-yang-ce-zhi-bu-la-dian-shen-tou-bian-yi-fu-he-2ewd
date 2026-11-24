from fastapi import APIRouter,Depends
from core import db,require
from fabric_registry import track

router=APIRouter(prefix="/wax-batches")

@router.get("")
def batches(_=Depends(require())):
    with db() as cx: return cx.execute("SELECT * FROM wax_batches ORDER BY code DESC").fetchall()

@router.get("/{key}/swatches")
def swatches(key:str,_=Depends(require())):
    with db() as cx: return track(cx,key)
