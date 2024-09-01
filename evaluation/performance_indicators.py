'''Auxiliar functions to calculate Set Coverage and Epsilon Indicator'''


def dominates(point_a, point_b):

    cond1 = all(a >= b for a, b in zip(point_a, point_b))
    # cond2 = any(a > b for a, b in zip(point_a, point_b))
    cond2 = True

    return cond1 and cond2


def set_coverage(A, B):
    '''
    Number of solutions in reference front B dominated by any solution in evaluated front A.
    '''
    count = 0
    for b in B:
        if any(dominates(a, b) for a in A):
            count += 1
    return count / len(B)


def epsilon_indicator(A, B):
    '''
    Calculates the smallest distance eps that moves the evaluated front A to ensure that every
    solution from reference front B is dominated by A.
    '''
    eps = float('-inf')
    for b in B:
        min_eps = float('inf')
        for a in A:
            max_ratio = max((b[i] - a[i]) / a[i] for i in range(len(a)))
            min_eps = min(min_eps, max_ratio)
        eps = max(eps, min_eps)
    return eps
