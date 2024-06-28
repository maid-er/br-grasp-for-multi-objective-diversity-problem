'''
Auxiliar function to apply Variable Neighborhood Descent with Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
import random
from itertools import combinations

from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)


LS = 'first'


def improve(sol: dict, max_iter: int = 50):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    neighborhoods = {1: [1, 1],
                     2: [1, 2],
                     3: [2, 1]}

    nb = 1
    count = 0
    abs_count = 0
    improve = True
    while count < max_iter and (improve or nb <= len(neighborhoods)):
        switch = neighborhoods[nb]
        logging.info('Local searching in neighbourhood %s with switch type %s.', nb, switch)
        if LS == 'best':
            best_improve = BestImprove()
            improve = best_improve.try_improvement(sol, switch)
        else:
            first_improve = FirstImprove()
            improve = first_improve.tryImprove(sol, switch)
        if not improve:
            logging.info('Unable to improve solution. Change neighborhood.')
            count += 1
            nb += 1
        else:
            logging.info('Improved solution.')
            nb = 1
        abs_count += 1
    logging.info('Local search stopped with %s total IT and %s IT with no improvements.',
                 abs_count, count)


class BestImprove:
    def try_improvement(self, sol: Solution, neighborhood: int) -> bool:
        '''Attempts to improve a solution by selecting and interchanging a selected element (node)
        with an unselected element. The improvement is obtained if the sum of the distances of the
        new element to the rest of the selected nodes is higher than the distance of the previous
        selection.

        Args:
        sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
        of selected candidates for the solution, 'of' with the objective value, and 'instance' that
        contains the instance data, with key 'd' representing the distance matrix between all the
        candidate nodes.

        Returns:
        (bool): `True` if the improvement was successful (i.e., if `ofVarSel` is less than
        `ofVarUnsel`), and `False` otherwise.
        '''
        (worst_selected,
         sel_maxsum_variability, sel_maxmin,
         best_unselected,
         unsel_maxsum_variability, unsel_maxmin) = self.select_interchange(sol, neighborhood)

        if (sel_maxsum_variability <= unsel_maxsum_variability) and (sel_maxmin <= unsel_maxmin):

            for v in best_unselected:
                sol.add_to_solution(v, unsel_maxmin, unsel_maxsum_variability)
            for u in worst_selected:
                sol.remove_from_solution(u, sel_maxsum_variability)
            return True
        return False

    def select_interchange(self, sol: Solution, neighborhood: list):
        '''Interchanges the worst element in solution (lowest sum of distances to the rest of the
        selected elements) with the best unselected element (highest sum of distances to the rest
        of the selected elements).

        Args:
        sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
        of selected candidates for the solution, 'of' with the objective value, and 'instance' that
        contains the instance data, with key 'd' representing the distance matrix between all the
        candidate nodes.

        Returns:
        sel (int): worst selected element ID.
        bestSel (float): sum of distances from `sel` to the rest of the elements in solution.
        unsel (int): best unselected element ID.
        bestUnsel (float): sum of distances from `unsel` to the rest of the elements in solution.
        '''
        n = sol.instance['n']
        sel = -1
        best_sum_sel = 0x3f3f3f3f
        best_min_sel = 0x3f3f3f3f
        unsel = -1
        best_sum_unsel = 0
        best_min_unsel = 0
        for combo in combinations(sol.solution_set, neighborhood[0]):
            d_sum = [sol.distance_sum_to_solution(v) for v in combo]
            d_min = [sol.minimum_distance_to_solution(v) for v in combo]
            if sum(d_sum) <= best_sum_sel and max(d_min) <= best_min_sel:
                best_sum_sel = sum(d_sum)
                best_min_sel = max(d_min)
                sel = list(combo)

        for combo in combinations(range(n), neighborhood[1]):
            if not any(sol.contains(v) for v in combo):
                d_sum = [sol.distance_sum_to_solution(v, without=sel) for v in combo]
                d_min = [sol.minimum_distance_to_solution(v, without=sel) for v in combo]
                if sum(d_sum) >= best_sum_unsel and max(d_min) >= best_min_unsel \
                    and sol.satisfies_cost(combo, sel) \
                        and sol.satisfies_capacity(combo, sel):

                    best_sum_unsel = sum(d_sum)
                    best_min_unsel = max(d_min)
                    unsel = list(combo)

        return sel, best_sum_sel, best_min_sel, unsel, best_sum_unsel, best_min_unsel


class FirstImprove:
    def tryImprove(self, sol: Solution, switch) -> bool:
        '''Attempts to improve a solution by selecting and interchanging a selected element (node)
        with an unselected element. The improvement is obtained if the sum of the distances of the
        new element to the rest of the selected nodes is higher than the distance of the previous
        selection.
        Args:
        sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
        of selected candidates for the solution, 'of' with the objective value, and 'instance' that
        contains the instance data, with key 'd' representing the distance matrix between all the
        candidate nodes.
        Returns:
        (bool): `True` if the improvement was successful (i.e., if `ofVarSel` is less than
        `ofVarUnsel`), and `False` otherwise.
        '''
        selected, unselected = self.createSelectedUnselected(sol)
        random.shuffle(selected)
        random.shuffle(unselected)
        for combo_s in combinations(selected, switch[0]):
            d_sum_s = [sol.distance_sum_to_solution(v) for v in combo_s]
            d_min_s = [sol.minimum_distance_to_solution(v) for v in combo_s]
            for combo_u in combinations(selected, switch[1]):
                d_sum_u = [sol.distance_sum_to_solution(v) for v in combo_u]
                d_min_u = [sol.minimum_distance_to_solution(v) for v in combo_u]
                if sum(d_sum_u) > sum(d_sum_s) and max(d_min_u) > max(d_min_s) \
                    and sol.satisfies_cost(combo_u, combo_s) \
                        and sol.satisfies_capacity(combo_u, combo_s):

                    for v in combo_u:
                        sol.add_to_solution(v, max(d_min_u), sum(d_sum_u))
                    for u in combo_s:
                        sol.remove_from_solution(u, sum(d_sum_s))

                    return True
        return False

    def createSelectedUnselected(self, sol: Solution):
        '''Takes a solution dictionary as input and returns two lists - one containing selected items
        and the other containing unselected items based on the solution.
        Args:
        sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
        of selected candidates for the solution, 'of' with the objective value, and 'instance' that
        contains the instance data, with key 'd' representing the distance matrix between all the
        candidate nodes.
        Returns:
        selected (list): contains the candidates selected in the current solution.
        unselected (list): contains the unselected candidates in the current solution.
        '''
        selected = []
        unselected = []
        n = sol.instance['n']
        for v in range(n):
            if sol.contains(v):
                selected.append(v)
            else:
                unselected.append(v)
        return selected, unselected
