from fastapi import APIRouter, Depends

from core import db, require
from repair_input import Dispatch
from repair_note import sign

router = APIRouter(prefix="/wax-batches/{key}/dispatch")


@router.get("")
def get_ticket(key: str, _=Depends(require())):
    with db() as cx:
        return cx.execute(
            "SELECT * FROM wax_dispatch WHERE batch=%s ORDER BY id DESC", (key,)
        ).fetchall()


@router.post("", status_code=201)
def handoff(key: str, body: Dispatch, user=Depends(require("reviewer"))):
    with db() as cx:
        return sign(cx, key, body, user["email"])
