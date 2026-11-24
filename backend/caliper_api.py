from fastapi import APIRouter, Depends

from caliper_input import Pair
from core import db, require
from pair_ledger import note

router = APIRouter(prefix="/wax-batches/{key}/readings")


@router.put("")
def save(key: str, body: Pair, user=Depends(require("operator"))):
    with db() as cx:
        return note(cx, key, body, user["email"])


@router.get("")
def history(key: str, _=Depends(require())):
    with db() as cx:
        current = cx.execute(
            "SELECT batch,seam,pass,depth,recorded_at FROM wax_readings WHERE batch=%s ORDER BY seam,pass",
            (key,),
        ).fetchall()
        retired = cx.execute(
            """SELECT batch,seam,pass,depth,recorded_at,retired_at,retired_by
               FROM wax_reading_history WHERE batch=%s ORDER BY id DESC""",
            (key,),
        ).fetchall()
    return {"current": current, "history": retired}
