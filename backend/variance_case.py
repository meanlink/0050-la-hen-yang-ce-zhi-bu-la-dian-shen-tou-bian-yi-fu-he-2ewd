from decimal import Decimal
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from core import enqueue
from fabric_registry import batch,track
from nested_design import design,full
from variance_math import analyze

def submit(cx,key):
    if batch(cx,key,True)["stage"]!="sampling": raise HTTPException(409,"该批已冻结")
    if not full(design(track(cx,key))):
        raise HTTPException(409,"三台各须两道接缝，每道接缝两次计量")
    cx.execute("UPDATE wax_batches SET stage='sealed' WHERE code=%s",(key,))
    return {"job_id":enqueue(cx,"study_wax_variance",{"batch":key})}

def calculate(cx,key):
    depth,bench,seam,repeat,sums=analyze(design(track(cx,key)))
    concern=depth>Decimal("1.2") or bench>Decimal(".15")
    row=cx.execute("INSERT INTO wax_components VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *",
                   (key,depth,bench,seam,repeat,concern,Jsonb(sums))).fetchone()
    cx.execute("UPDATE wax_batches SET stage='classified' WHERE code=%s",(key,))
    return row

def inspect(cx,key):
    batch_row=batch(cx,key)
    row=cx.execute("SELECT * FROM wax_components WHERE batch=%s",(key,)).fetchone()
    return {"stage":batch_row["stage"],"result":row}
