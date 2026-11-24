from decimal import Decimal

from fastapi import HTTPException
from psycopg.types.json import Jsonb

from core import enqueue
from fabric_registry import batch, track
from nested_design import design, full
from variance_math import analyze


def submit(cx, key):
    row = batch(cx, key, True)
    if row["stage"] not in ("sampling", "held"):
        raise HTTPException(409, "该批已冻结")
    if not full(design(track(cx, key))):
        raise HTTPException(409, "三台各须两道接缝，每道接缝两次计量")
    if row["stage"] == "held" and not _retest_after_hold(cx, key):
        raise HTTPException(409, "涉事修补台的接缝须在扣留后重新计量，其余读数照用")
    epoch = row["hold_epoch"]
    if row["stage"] == "sampling":
        cx.execute("UPDATE wax_batches SET stage='sealed' WHERE code=%s", (key,))
    # A held batch stays held: its recomputation is only used to decide whether
    # the hold can be lifted, never to authorise a handoff by itself.
    return {"job_id": enqueue(cx, "study_wax_variance", {"batch": key, "epoch": epoch}), "epoch": epoch}


def calculate(cx, key, epoch):
    row = cx.execute(
        "SELECT stage,hold_epoch,pre_hold_stage FROM wax_batches WHERE code=%s FOR UPDATE", (key,)
    ).fetchone()
    if row is None:
        raise HTTPException(409, "织补试涂批次不存在")
    if epoch != row["hold_epoch"]:
        # Queued before a hold was placed, or superseded by a retried hold:
        # the evidence describes a finished epoch and must not move the batch.
        return {"batch": key, "ignored": True, "reason": "stale_epoch", "stage": row["stage"]}
    if row["stage"] not in ("sealed", "held"):
        return {"batch": key, "ignored": True, "reason": "stage", "stage": row["stage"]}

    if row["stage"] == "held" and not _retest_after_hold(cx, key):
        return {"batch": key, "ignored": True, "reason": "no_retest", "stage": "held"}

    depth, bench, seam, repeat, sums = analyze(design(track(cx, key)))
    concern = depth > Decimal("1.2") or bench > Decimal(".15")
    # Upsert in place: signed dispatch receipts reference this component row.
    cx.execute(
        """INSERT INTO wax_components(batch,avg_depth,bench_variance,seam_variance,reading_variance,requires_recheck,sums)
           VALUES (%s,%s,%s,%s,%s,%s,%s)
           ON CONFLICT(batch) DO UPDATE SET avg_depth=excluded.avg_depth,
             bench_variance=excluded.bench_variance, seam_variance=excluded.seam_variance,
             reading_variance=excluded.reading_variance, requires_recheck=excluded.requires_recheck,
             sums=excluded.sums""",
        (key, depth, bench, seam, repeat, concern, Jsonb(sums)),
    )
    if row["stage"] == "sealed":
        cx.execute("UPDATE wax_batches SET stage='classified' WHERE code=%s", (key,))
        return {"batch": key, "ignored": False, "stage": "classified", "requires_recheck": concern}

    # Held batch: a clean recomputation of freshly re-measured affected seams
    # lifts the hold and restores the handoff stage the batch had before the
    # hold. The original dispatch receipt is kept for tracing. Otherwise the
    # batch stays stopped at the hold.
    if concern:
        return {"batch": key, "ignored": False, "stage": "held", "requires_recheck": True}
    stage = _restore_stage(row["pre_hold_stage"])
    cx.execute("UPDATE wax_holds SET cleared_at=clock_timestamp() WHERE batch=%s AND cleared_at IS NULL", (key,))
    cx.execute("UPDATE wax_batches SET stage=%s, pre_hold_stage=NULL WHERE code=%s", (stage, key))
    return {"batch": key, "ignored": False, "stage": stage, "requires_recheck": False}


def _restore_stage(pre_hold):
    # A batch still under analysis becomes handoff-ready once re-measured;
    # a batch that already had a signed action returns to that action.
    if pre_hold in ("released", "recheck"):
        return pre_hold
    return "classified"



def _retest_after_hold(cx, key):
    """Every seam on a held bench must have been re-measured after the hold.
    Other seams keep their original readings."""
    missing = cx.execute(
        """SELECT 1 FROM wax_holds h
           WHERE h.batch=%s AND h.cleared_at IS NULL
             AND EXISTS (
                 SELECT 1 FROM wax_swatches s
                 WHERE s.batch=h.batch AND s.bench=h.bench
                   AND NOT EXISTS (
                       SELECT 1 FROM wax_readings r
                       WHERE r.batch=s.batch AND r.seam=s.seam AND r.recorded_at > h.created_at))
           LIMIT 1""",
        (key,),
    ).fetchone()
    return missing is None


def inspect(cx, key):
    batch_row = batch(cx, key)
    row = cx.execute("SELECT * FROM wax_components WHERE batch=%s", (key,)).fetchone()
    benches = cx.execute(
        "SELECT bench FROM wax_holds WHERE batch=%s AND cleared_at IS NULL ORDER BY bench", (key,)
    ).fetchall()
    return {
        "stage": batch_row["stage"],
        "result": row,
        "hold_epoch": batch_row["hold_epoch"],
        "hold_benches": [item["bench"] for item in benches],
    }
