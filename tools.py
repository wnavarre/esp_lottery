def shifted_left(ls):
    out = ls[1:]
    out.append(ls[0])
    return out

def max_with_gt(it, gt):
    ls = list(it)
    out = ls[0]
    for elem in it:
        if gt(elem, out):
            out = elem
    return out
