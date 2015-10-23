# Practicing Dynamic Programming (DP) with the log cutting problem given on the practice midterm.
# this file contains the solution from the given exam solutions.
import numpy as np


################################################################################
# Top Down Algorithm (Solution)
################################################################################


def top_down_woody(d):
    i = 0
    j = len(d) - 1
    c = np.ones([j+1, j+1])*np.inf
    return top_down_woody_aux(i, j, d, c)


def top_down_woody_aux(i, j, d, c):
    if j == i+1:
        return 0
    if c[i, j] == np.inf:
        for k in range(i+1, j):
            c[i, j] = min(c[i, j], d[j] - d[i] + top_down_woody_aux(i, k, d, c) + top_down_woody_aux(k, j, d, c))
    return c[i, j]


################################################################################
# Bottom Up Algorithm (solution)
################################################################################


def bottom_up_woody(d):
    n = len(d) - 2
    c = np.zeros([n+2, n+2])
    for m in range(2, n+2):
        for i in range(0, n-m+2):
            j = i + m
            c[i, j] = np.inf
            for k in range(i+1, j+1):
                c[i, j] = min(c[i, j], d[j] - d[i] + c[i, k] + c[k, j])
    return c[0, n+1]


################################################################################
# Main
################################################################################
if __name__ == '__main__':
    dist = np.array([0, 3, 8, 10])
    print("min cost (top down sol) = $" + str(top_down_woody(dist)))
    print("min cost (bottom up sol) = $" + str(bottom_up_woody(dist)))
