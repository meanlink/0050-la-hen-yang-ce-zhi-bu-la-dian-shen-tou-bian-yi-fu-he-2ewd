from fastapi import HTTPException
from fabric_registry import batch

def sign(cx,key,body,user):
    if batch(cx,key,True)["stage"]!="classified":
        raise HTTPException(409,"只有生成分量且未签的批次可以交接")
    row=cx.execute("SELECT requires_recheck FROM wax_components WHERE batch=%s",(key,)).fetchone()
    if body.decision=="release" and row["requires_recheck"]:
        raise HTTPException(409,"台间渗透变异或总均值超限，须走补测")
    ticket=cx.execute("INSERT INTO wax_dispatch VALUES (%s,%s,%s,%s,%s) RETURNING *",
        (key,body.decision,body.destination,body.note,user)).fetchone()
    stage="released" if body.decision=="release" else "recheck"
    cx.execute("UPDATE wax_batches SET stage=%s WHERE code=%s",(stage,key))
    return ticket
