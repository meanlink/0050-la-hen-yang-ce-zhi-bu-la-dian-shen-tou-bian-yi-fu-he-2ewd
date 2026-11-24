from fastapi import HTTPException

from fabric_registry import batch
from hold_note import active as active_holds


def sign(cx, key, body, user):
    row = batch(cx, key, True)
    if row["stage"] == "held":
        raise HTTPException(409, "批次因量具失准扣留，交接已暂停，须补测复算后才能恢复")
    if row["stage"] != "classified":
        raise HTTPException(409, "只有生成分量且未签的批次可以交接")
    if active_holds(cx, key):
        raise HTTPException(409, "批次仍有未解除的扣留，交接已暂停")
    component = cx.execute("SELECT requires_recheck FROM wax_components WHERE batch=%s", (key,)).fetchone()
    if body.decision == "release" and component["requires_recheck"]:
        raise HTTPException(409, "台间渗透变异或总均值超限，须走补测")
    ticket = cx.execute(
        "INSERT INTO wax_dispatch(batch,decision,destination,note,manager) VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (key, body.decision, body.destination, body.note, user),
    ).fetchone()
    stage = "released" if body.decision == "release" else "recheck"
    cx.execute("UPDATE wax_batches SET stage=%s WHERE code=%s", (stage, key))
    return ticket
