from fastapi import APIRouter, Depends, HTTPException

from core import db, require
from hold_input import BenchHold, Hold
from hold_note import active_all, listing, place, place_bench

router = APIRouter()

BENCHES = ("A", "B", "C")


@router.get("/wax-holds")
def index(bench: str | None = None, _=Depends(require())):
    if bench is not None and bench not in BENCHES:
        raise HTTPException(422, "修补台须为 A、B 或 C")
    with db() as cx:
        return active_all(cx, bench)


@router.post("/wax-holds", status_code=201)
def sweep(body: BenchHold, user=Depends(require("reviewer"))):
    """Register one bench's failure against several batches at once."""
    with db() as cx:
        return place_bench(cx, body.bench, body.batches, body.reason, user["email"])


@router.get("/wax-batches/{key}/holds")
def detail(key: str, _=Depends(require())):
    with db() as cx:
        return listing(cx, key)


@router.post("/wax-batches/{key}/holds", status_code=201)
def register(key: str, body: Hold, user=Depends(require("reviewer"))):
    with db() as cx:
        result = place(cx, key, body.bench, body.reason, user["email"])
        return result | listing(cx, key)
