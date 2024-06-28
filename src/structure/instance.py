'''Auxiliar function to read and process instances'''


def read_instance(path: str) -> dict:
    '''Reads and processes data from a file to create a dictionary representing an instance for the
    diversity problem with number of candidate nodes `n`, number of elements to be selected `p`,
    distances between each node pair `d`, cost of each node `a`, and capacity of each node `c`.
    Additionally, reads the cost constraint `K` and capacity constraint `B` of the problem.

    Args:
      path (str): file path to the instance file that contains the data to be read and processed by
    the function.

    Returns:
      (dict): contains the instance data. The dictionary includes the number of nodes `n`, the
    number of nodes to be selected `p`, a distance matrix `d` representing the distances from each
    node to the rest of the nodes, a cost vector `a` with the costs of each node, and a capacity
    vector `a` with the capacities of each node.
    '''
    instance = {}
    with open(path, "r") as f:
        n = int(f.readline())
        instance['n'] = n  # Size
        instance['d'] = []  # Distance matrix
        instance['a'] = [0] * n  # Cost vector
        instance['c'] = [0] * n  # Capacity vector
        for _ in range(n):
            instance['d'].append([0] * n)
        for i in range(n):
            for _ in range(i+1, n):
                u, v, d = f.readline().split()
                u = int(u) - 1  # Node u
                v = int(v) - 1  # Node v
                d = round(float(d), 2)  # Distance between u and v
                instance['d'][u][v] = d
                instance['d'][v][u] = d
        for i in range(n):
            u, a, _, c = f.readline().split()
            u = int(u) - 1  # Node u
            a = int(float(a))  # Cost of node u
            c = int(float(c))  # Capacity of node u
            instance['a'][u] = a
            instance['c'][u] = c
        K, _, B = map(int, f.readline().split())
        instance['K'] = K  # Maximum budget
        instance['B'] = B  # Minimum capacity
    return instance
