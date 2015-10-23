# Practicing Dynamic Programming (DP) with the log cutting problem given on the practice midterm.
import numpy as np


################################################################################
# Slow Algorithm
################################################################################


def cut_log(d, j, k):
    if j+1 == k:
        return 0
    c = float('Inf')
    for i in range(j+1, k):
        c = min(c, d[k] + cut_log(d, j, i) + cut_log(d - d[i], i, k))
    return c


################################################################################
# Top Down Algorithm
################################################################################


def memoized_cut_log(d):
    k = len(d)
    j = 0
    r = np.ones([k, k])*np.inf
    v = memoized_cut_log_aux(d, j, k-1, r)
    return v


def memoized_cut_log_aux(d, j, k, r):
    if r[j, k] < np.inf:
        return r[j, k]
    if j+1 == k:
        r[j, k] = 0
    else:
        c = float('Inf')
        for i in range(j+1, k):
            c = min(c, d[k] + memoized_cut_log_aux(d, j, i, r) + memoized_cut_log_aux(d - d[i], i, k, r))
        r[j, k] = c
    return r[j, k]


################################################################################
# Bottom Up Algorithm
################################################################################


# def bottom_up_cut_log(d):
#     k = len(d)
#     r = np.zeros([k, k])
#     for i in range(2, k):
#         c = np.inf
#         for j in range(1, i):
#             c = min(c, d[i] + r[j, i-1] + r[j-1, i])
#         r[j, i] = c
#     print(r)
#     return r[0, k-1]


################################################################################
# Main
################################################################################
if __name__ == '__main__':
    dist = np.array([0, 3, 8, 10])
    print("min cost (slow) = $" + str(cut_log(dist, 0, 3)))
    print("min cost (top down) = $" + str(memoized_cut_log(dist)))
    # print("min cost (slow) = $" + str(bottom_up_cut_log(dist)))
