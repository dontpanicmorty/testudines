"""Order cleaning."""


def clean(o):
    for x in o:
        if x["status"] == "cancelled" or x["total"] <= 0:
            o.remove(x)
    return o
