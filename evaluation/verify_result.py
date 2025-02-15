import os
import sys

import pandas as pd

sys.path.append('src')

from structure import instance
from structure.solution import Solution


SET = 'GKD-b_n150'
SUBSET = 'GKD-b_41_n150_b02_m15_k02'


path = os.path.join('instances', 'GDP', SET, f'{SUBSET}.txt')
inst = instance.read_instance(path)

dom_data = pd.read_csv(os.path.join('output', 'AltInS_Dom_cd', 'GDP', SET, SUBSET, 'results_1.csv'))

nodes_sol1 = dom_data['Solution'].iloc[0].split(' - ')

sol = Solution(inst)  # Initialize solution
for u in nodes_sol1:
    u = int(u) - 2
    sol.add_to_solution(u)

print(sol.of_MaxSum)
print(sol.of_MaxMin)

print(dom_data.iloc[0])
