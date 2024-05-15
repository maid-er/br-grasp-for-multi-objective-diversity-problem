'''Auxiliar function to read and process instances'''


def readInstance(path: str) -> dict:
    '''Reads and processes data from a file to create a dictionary representing an instance for the
    diversity problem with number of candidate nodes `n`, number of elements to be selected `p`, and
    distances between each node pair `d`.

    Args:
      path (str): file path to the instance file that contains the data to be read and processed by
    the function.

    Returns:
      (dict): contains the instance data. The dictionary includes the number of nodes `n`, the
    number of nodes to be selected `p`, and a distance matrix `d` representing the distances from
    each node to the rest of the nodes.
    '''
    instance = {}
    with open(path, "r") as f:
        n, p = map(int, f.readline().split())
        instance['n'] = n
        instance['p'] = p
        instance['d'] = []
        for _ in range(n):
            instance['d'].append([0] * n)
        for i in range(n):
            for j in range(i+1, n):
                u, v, d = f.readline().split()
                u = int(u)
                v = int(v)
                d = round(float(d), 2)
                instance['d'][u][v] = d
                instance['d'][v][u] = d
    return instance


def read_USCAP_instance(path: str):
    instance = {}
    with open(path, "r") as f:
        n = int(f.readline())
        instance['n'] = n
        instance['d'] = []
        instance['a'] = [0] * n  # cost
        instance['c'] = [0] * n  # capacity
        for _ in range(n):
            instance['d'].append([0] * n)
        for i in range(n):
            for _ in range(i+1, n):
                u, v, d = f.readline().split()
                u = int(u) - 1
                v = int(v) - 1
                d = round(float(d), 2)
                instance['d'][u][v] = d
                instance['d'][v][u] = d
        for i in range(n):
            u, a, _, c = f.readline().split()
            u = int(u) - 1
            a = int(a)
            c = int(c)
            instance['a'][u] = a
            instance['c'][u] = c
        K, _, B = map(int, f.readline().split())
        instance['K'] = K
        instance['B'] = B
    return instance
