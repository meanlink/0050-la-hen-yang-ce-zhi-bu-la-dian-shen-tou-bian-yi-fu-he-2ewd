from fastapi import HTTPException

def batch(cx,key,lock=False):
    row=cx.execute("SELECT * FROM wax_batches WHERE code=%s"+(" FOR UPDATE" if lock else ""),(key,)).fetchone()
    if row is None: raise HTTPException(404,"织补试涂批次不存在")
    return row

def track(cx,key):
    batch(cx,key)
    return cx.execute("""SELECT s.*,r.pass,r.depth FROM wax_swatches s
         LEFT JOIN wax_readings r USING(batch,seam) WHERE s.batch=%s ORDER BY s.bench,s.seam,r.pass""",(key,)).fetchall()
