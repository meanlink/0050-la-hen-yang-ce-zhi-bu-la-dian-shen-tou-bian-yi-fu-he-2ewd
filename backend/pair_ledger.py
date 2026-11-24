from fastapi import HTTPException
from fabric_registry import batch

def note(cx,key,body):
    if batch(cx,key,True)["stage"]!="sampling":
        raise HTTPException(409,"样册已留档，补测须另起试涂批次")
    if not cx.execute("SELECT 1 FROM wax_swatches WHERE batch=%s AND seam=%s",(key,body.seam)).fetchone():
        raise HTTPException(409,"成对计量须绑定该批已登记的试涂接缝")
    return cx.execute("""INSERT INTO wax_readings VALUES (%s,%s,1,%s),(%s,%s,2,%s)
          ON CONFLICT(batch,seam,pass) DO UPDATE SET depth=excluded.depth RETURNING *""",
         (key,body.seam,body.first,key,body.seam,body.second)).fetchall()
