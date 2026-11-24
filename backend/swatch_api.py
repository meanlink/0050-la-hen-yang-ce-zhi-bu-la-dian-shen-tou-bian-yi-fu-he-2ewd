from fastapi import APIRouter, Depends

from core import db, require
from fabric_registry import track

router = APIRouter(prefix="/wax-batches")


@router.get("")
def batches(_=Depends(require())):
    with db() as cx:
        return cx.execute(
            """SELECT b.*, COALESCE(h.benches, ARRAY[]::text[]) AS hold_benches
               FROM wax_batches b
               LEFT JOIN (
                   SELECT batch, array_agg(bench ORDER BY bench) AS benches
                   FROM wax_holds WHERE cleared_at IS NULL GROUP BY batch
               ) h ON h.batch=b.code
               ORDER BY b.code DESC"""
        ).fetchall()


@router.get("/{key}/swatches")
def swatches(key: str, _=Depends(require())):
    with db() as cx:
        return track(cx, key)
