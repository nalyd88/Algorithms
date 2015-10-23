# Practice the RodCutting Example


################################################################################
# Slow Algorithm
################################################################################
def cut_rod(p, n):
    if n == 0:
        return 0
    q = -100000
    for i in range(1, n+1):
        q = max(q, p[i] + cut_rod(p, n-i))
    return q


################################################################################
# Top Down Algorithm
################################################################################
def memoized_cut_rod(p, n):
    r = [-float('Inf') + i for i in range(0, n+1)]
    return memoized_cut_rod_aux(p, n, r)


def memoized_cut_rod_aux(p, n, r):
    if r[n] >= 0:
        return r[n]
    if n == 0:
        return 0
    else:
        q = -float('Inf')
        for i in range(1, n+1):
            q = max(q, p[i] + cut_rod(p, n-i))
    r[n] = q
    return q


################################################################################
# Bottom Up Algorithm
################################################################################
def bottom_up_cut_rod(p, n):
    r = [i for i in range(0, n+1)]
    r[0] = 0
    for j in range(1, n+1):
        q = -float('Inf')
        for i in range(1, j+1):
            q = max(q, p[i] + r[j-i])
        r[j] = q
    return r[n]


################################################################################
# Main
################################################################################
if __name__ == '__main__':
    length = 7
    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    print("Max Value (slow) = $" + str(cut_rod(prices, length)))
    print("Max Value (top down) = $" + str(memoized_cut_rod(prices, length)))
    print("Max Value (bottom up) = $" + str(bottom_up_cut_rod(prices, length)))
