'''Auxiliar class to handle candidate solutions'''


class Solution:
    def __init__(self, instance: dict):
        self.solution_set = set()
        self.of_MaxSum = 0
        self.of_MaxMin = 0x3f3f3f3f
        self.total_cost = 0
        self.total_capacity = 0
        self.instance = instance

    def add_to_solution(self, u: int, min_distance: float = -1, sum_variation: float = -1):
        '''Updates a solution by adding a specified element and its corresponding value to the
        objective function.

        Args:
          u (int): represents the ID of an element (node) that will be added to the solution.
          ofVariation (float): is an optional parameter with a default value of -1. The default
        value -1 is used when the first candidate is added to sum all the distances from selected
        candidate `u` to the rest of the candidates in the objective function 'of'. Then, each
        time a new candidate is added, the `ofVariation` is received as an input representing the
        sum of the distances from the added element `u` and the rest of the nodes in the solution.
        '''
        if sum_variation == -1 or min_distance == -1:
            for s in self.solution_set:
                distance_u_s = self.instance['d'][u][s]
                self.of_MaxSum += distance_u_s
                if self.of_MaxMin > distance_u_s:
                    self.of_MaxMin = distance_u_s
        else:
            self.of_MaxSum += sum_variation
            if self.of_MaxMin > min_distance:
                self.of_MaxMin = min_distance
        self.total_cost += self.instance['a'][u]
        self.total_capacity += self.instance['c'][u]
        self.solution_set.add(u)

    def remove_from_solution(self, u: int, sum_variation: float = -1):
        '''Removes an element from a solution and updates the objective function value accordingly.

        Args:
          u (int): represents the ID of an element (node) that will be removed from the solution.
          ofVariation (float): is an optional parameter with a default value of -1. Each time a node
        is removed from the solution, the `ofVariation` is received as an input representing the sum
        of the distances from the removed element `u` and the rest of the nodes in the solution.
        '''
        self.solution_set.remove(u)
        if sum_variation == -1:
            for s in self.solution_set:
                self.of_MaxSum -= self.instance['d'][u][s]
        else:
            self.of_MaxSum -= sum_variation
        self.total_cost -= self.instance['a'][u]
        self.total_capacity -= self.instance['c'][u]

    def contains(self, u: int) -> bool:
        '''Checks if a given candidate ID `u` is present in the current solution dictionary `sol`
        under the key 'sol'.

        Args:
          u (int): represents the ID of a candidate element (node).

        Returns:
          (bool): indicates whether the variable `u` is present in the 'sol' key of the dictionary
        `sol`.
        '''
        return u in self.solution_set

    def distance_sum_to_solution(self, u: int, without: int = -1) -> float:
        '''Calculates the sum of the distances from a given node to the rest of the nodes in the
        solution graph, excluding the node specified with the optional input `without`.

        Args:
          u (int): represents the ID of the candidate element (node) from which we want to calculate
        the sum of the distances to the rest of the nodes.
          without (int): it is an optional parameter that allows you to specify the ID of the node
        that should be excluded from the calculation of the sum of the distances. If the `without`
        parameter is provided, the function will skip calculating the distance to the specified
        value in the solution.

        Returns:
          (float): returns the sum of the distances from a given node `u` to the rest of the nodes
        in solution `sol`, excluding the distance to a specific node `without` if provided.
        '''
        d = 0
        for s in self.solution_set:
            if s != without:
                d += self.instance['d'][s][u]
        return round(d, 2)

    def minimum_distance_to_solution(self, u: int, without: int = -1) -> float:
        '''Calculates the minimum distance from a given node to the rest of the nodes in the
        solution graph, excluding the node specified with the optional input `without`.

        Args:
          u (int): represents the ID of the candidate element (node) from which we want to find the
        minimum distance to the rest of the nodes.
          without (int): it is an optional parameter that allows you to specify the ID of the node
        that should be excluded from the search of the minimum distance. If the `without` parameter
        is provided, the function will skip calculating the distance to the specified value in the
        solution.

        Returns:
          (float): returns the minimum distance value from a given node `u` to the rest of the
        nodes in solution `sol`, excluding the distance to a specific node `without` if provided.
        '''
        min_d = 0x3f3f3f3f
        for s in self.solution_set:
            if s != without and s != u:
                d = self.instance['d'][s][u]
                if d < min_d:
                    min_d = d
        return round(min_d, 2)

    def is_feasible(self) -> float:
        '''Checks if a solution has the same number of elements specified in the instance parameter `p`.

        Returns:
          (bool): indicates whether the length of the 'sol' key in the input dictionary 'sol', that is,
        the selected candidates in the solution, is equal to the required number of selected elements
        'p' in the 'instance'.
        '''
        return len(self.solution_set) > 2

    def satisfies_cost(self, u: int, v: int = -1):
        # removing_candidate = 0
        # if v != -1:
        #     removing_candidate = sol['instance']['a'][v]
        possible_cost = self.total_cost
        if v != -1:
            for q in v:
                possible_cost -= self.instance['a'][q]
        for q in u:
            possible_cost += self.instance['a'][q]

        return possible_cost < self.instance['K']

    def satisfies_capacity(self, u: int = -1, v: int = -1):
        # new_candidate = 0
        # if u != -1:
        #     new_candidate = sol['instance']['c'][u]
        # removing_candidate = 0
        # if v != -1:
        #     removing_candidate = sol['instance']['c'][v]
        possible_capacity = self.total_capacity
        if v != -1:
            for q in v:
                possible_capacity -= self.instance['c'][q]
        if u != -1:
            for q in u:
                possible_capacity += self.instance['c'][q]

        return possible_capacity > self.instance['B']

    def print_sol(self):
        '''Prints the solution.

        Args:
          sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
        of selected candidates for the solution, 'of' with the objective value, and 'instance' that
        contains the instance data, with key 'd' representing the distance matrix between all the
        candidate nodes.
        '''
        print(f"SOL: {self.solution_set}")
        print(f"OF MaxSum: {round(self.of_MaxSum, 2)}")
        print(f"OF MaxMin: {round(self.of_MaxMin, 2)}")
        print(f"Total cost: {round(self.total_cost, 2)}")
        print(f"Total capacity: {round(self.total_capacity, 2)}")
