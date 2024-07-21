import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pareto_front(table: pd.DataFrame, instance: str) -> go.Figure:
    table['Constraint values'] = ('Cost: ' + table.Cost.astype(str) +
                                  ' & Capacity: ' + table.Capacity.astype(str))
    fig = px.scatter(table, x='MaxMin', y='MaxSum', color='Constraint values')
    fig.update_layout(title_text=os.path.split(instance)[-1].split(".")[0])
    # fig.show()

    return fig


def save(table: pd.DataFrame, figure: go.Figure, params: str, instance: str):
    instance_id = os.path.split(instance)[-1].split(".")[0]

    with open('temp/execution.txt', 'r+') as ex_file:
        execution_n = ex_file.read()
        ex_file.seek(0)
        ex_file.write(str(int(execution_n) + 1))
        ex_file.truncate()
    os.makedirs(os.path.join('output',
                             f'{params}',
                             f'{instance_id}'), exist_ok=True)

    execution_n = 0
    table.to_csv(os.path.join('output',
                              f'{params}',
                              f'{instance_id}',
                              f'results_{instance_id}_{execution_n}.csv'),
                 index=False)
    figure.write_html(os.path.join('output',
                                   f'{params}',
                                   f'{instance_id}',
                                   f'solution_{execution_n}.html'))
