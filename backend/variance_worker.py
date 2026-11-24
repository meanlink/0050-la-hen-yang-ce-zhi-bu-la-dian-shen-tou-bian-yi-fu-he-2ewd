from variance_case import calculate

def run(cx,kind,data):
    if kind!="study_wax_variance": raise ValueError(kind)
    return calculate(cx,data["batch"],data.get("epoch",0))
