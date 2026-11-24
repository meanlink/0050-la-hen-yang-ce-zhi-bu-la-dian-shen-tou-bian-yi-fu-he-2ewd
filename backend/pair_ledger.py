from fastapi import HTTPException

from fabric_registry import batch


def active_benches(cx, key):
    return {
        row["bench"]
        for row in cx.execute(
            "SELECT bench FROM wax_holds WHERE batch=%s AND cleared_at IS NULL", (key,)
        ).fetchall()
    }


def _archive(cx, key, seam, user):
    cx.execute(
        """INSERT INTO wax_reading_history(batch,seam,pass,depth,recorded_at,retired_by,retire_reason)
           SELECT batch,seam,pass,depth,recorded_at,%s,'重新计量' FROM wax_readings
           WHERE batch=%s AND seam=%s""",
        (user, key, seam),
    )


def note(cx, key, body, user):
    row = batch(cx, key, True)
    held = active_benches(cx, key)
    if row["stage"] == "sampling":
        pass
    elif row["stage"] == "held" and body.seam.split("-")[0] in held:
        # Only the seams belonging to a held bench are re-measured; every other
        # reading stays in use for the recomputation.
        pass
    elif row["stage"] == "held" and row["pre_hold_stage"] == "sampling":
        # Held before its evidence was complete: no readings to reuse yet.
        pass
    elif row["stage"] == "held":
        raise HTTPException(409, "扣留期间只补测涉事修补台的接缝，其余读数照用")
    else:
        raise HTTPException(409, "样册已留档，补测须另起试涂批次")
    if not cx.execute(
        "SELECT 1 FROM wax_swatches WHERE batch=%s AND seam=%s", (key, body.seam)
    ).fetchone():
        raise HTTPException(409, "成对计量须绑定该批已登记的试涂接缝")
    _archive(cx, key, body.seam, user)
    return cx.execute(
        """INSERT INTO wax_readings(batch,seam,pass,depth,recorded_at)
           VALUES (%s,%s,1,%s,clock_timestamp()),(%s,%s,2,%s,clock_timestamp())
           ON CONFLICT(batch,seam,pass)
           DO UPDATE SET depth=excluded.depth,recorded_at=excluded.recorded_at RETURNING *""",
        (key, body.seam, body.first, key, body.seam, body.second),
    ).fetchall()
