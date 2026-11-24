from fabric_registry import batch


def active(cx, key):
    return cx.execute(
        "SELECT * FROM wax_holds WHERE batch=%s AND cleared_at IS NULL ORDER BY bench",
        (key,),
    ).fetchall()


def active_all(cx, bench=None):
    """Active holds across batches, optionally narrowed to one repair bench."""
    rows = cx.execute(
        """SELECT h.*, b.fabric, b.stage, b.hold_epoch FROM wax_holds h
           JOIN wax_batches b ON b.code=h.batch
           WHERE h.cleared_at IS NULL
             AND (%(bench)s::text IS NULL OR h.bench=%(bench)s)
           ORDER BY h.bench, h.batch""",
        {"bench": bench},
    ).fetchall()
    groups = {}
    for row in rows:
        groups.setdefault(row["bench"], {"bench": row["bench"], "batches": []})["batches"].append(row)
    return list(groups.values())


def listing(cx, key):
    row = batch(cx, key)
    rows = cx.execute(
        "SELECT * FROM wax_holds WHERE batch=%s ORDER BY (cleared_at IS NULL) DESC, id",
        (key,),
    ).fetchall()
    return {
        "batch": key,
        "stage": row["stage"],
        "suspended": row["stage"] == "held",
        "active": [hold for hold in rows if hold["cleared_at"] is None],
        "holds": rows,
    }


def place(cx, key, bench, reason, manager):
    """Register a bench-wide hold on one batch, idempotently.

    The batch row lock serialises this with release signature, so a release and
    a hold submitted together always end with the batch stopped at the hold.
    """
    row = batch(cx, key, True)
    existing = cx.execute(
        "SELECT * FROM wax_holds WHERE batch=%s AND bench=%s AND cleared_at IS NULL",
        (key, bench),
    ).fetchone()
    if existing:
        # A retried registration keeps the original hold and does not bump the
        # evidence generation again.
        return {"hold": existing, "duplicate": True, "stage": row["stage"]}

    epoch = row["hold_epoch"] + 1
    if row["stage"] == "held":
        cx.execute(
            "UPDATE wax_batches SET hold_epoch=%s WHERE code=%s", (epoch, key)
        )
    else:
        # Any variance result still queued for the previous stage carries the
        # old epoch and is therefore unable to restore the handoff.
        cx.execute(
            "UPDATE wax_batches SET stage='held', pre_hold_stage=%s, hold_epoch=%s WHERE code=%s",
            (row["stage"], epoch, key),
        )
    hold = cx.execute(
        """INSERT INTO wax_holds(batch,bench,reason,manager,epoch)
           VALUES (%s,%s,%s,%s,%s) RETURNING *""",
        (key, bench, reason, manager, epoch),
    ).fetchone()
    return {"hold": hold, "duplicate": False, "stage": "held"}


def place_bench(cx, bench, codes, reason, manager):
    """Hold several batches for one repair bench in a single transaction.

    Batches are locked in code order so overlapping sweeps cannot deadlock.
    """
    results = []
    for key in sorted({code.strip() for code in codes if code.strip()}):
        results.append({"batch": key} | place(cx, key, bench, reason, manager))
    return {"bench": bench, "results": results}

