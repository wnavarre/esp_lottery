def max_with_gt(it, gt):
    ls = list(it)
    candidate = ls[0]
    for i in range(1, len(ls)):
        if gt(ls[i], candidate):
            candidate = ls[i]
    return candidate
