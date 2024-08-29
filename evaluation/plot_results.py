import os
import pandas as pd
import plotly.express as px


# instance = 'GKD-b_11_n50_b02_m5_k02'
# file = 'results_GKD-b_11_n50_b02_m5_k02_2.csv'
instance = 'USCAP/Bi-objective'
file = 'results_USCAP_5.csv'

cap_table = pd.read_csv(os.path.join('output', 'USCAP', 'abbreviation_node.csv'), sep=';',
                        names=['State', 'number', 'Abbr'])

filename = os.path.join('output',
                        instance,
                        file)

result_table = pd.read_csv(filename)
result_table.Solution = result_table.Solution.apply(lambda s: [int(n) for n in s.split('-')])
results = result_table.Solution.apply(
    lambda nodes: cap_table.Abbr.loc[cap_table.number.isin(nodes)].to_list())
results = results.apply(lambda s: ' - '.join(s))


result_table['Solution and constraint values'] = ('<b>' + results + '</b>' + '<br>'
                                                  'Cost: ' + result_table.Cost.astype(str) +
                                                  ' & Capacity: ' +
                                                  result_table.Capacity.astype(str))


result_table['Constraint values'] = ('Cost: ' + result_table.Cost.astype(str) +
                                     ' & Capacity: ' + result_table.Capacity.astype(str))

fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color='Solution and constraint values',
                 color_discrete_sequence=px.colors.qualitative.Light24)
fig.update_traces(marker={'size': 8})
fig.update_layout(title_text=instance)
fig.show()
