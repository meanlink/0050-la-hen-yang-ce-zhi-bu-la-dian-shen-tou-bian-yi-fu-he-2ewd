from collections import defaultdict

def design(rows):
    data=defaultdict(lambda:defaultdict(list))
    for row in rows:
        data[row["bench"]][row["seam"]].append(row["depth"])
    return data

def full(data):
    return set(data)=={"A","B","C"} and all(
        len(seams)==2 and all(len(readings)==2 and None not in readings for readings in seams.values())
        for seams in data.values())
