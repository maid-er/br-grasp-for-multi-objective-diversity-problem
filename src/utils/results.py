import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class OutputHandler:
    def __init__(self):
        self.execution_n = -1

        self._get_execution_number()

    def pareto_front(self, table: pd.DataFrame, instance: str) -> go.Figure:
        table['Constraint values'] = ('Cost: ' + table.Cost.astype(str) +
                                      ' & Capacity: ' + table.Capacity.astype(str))
        fig = px.scatter(table, x='MaxMin', y='MaxSum', color='Constraint values')
        fig.update_layout(title_text=os.path.split(instance)[-1].split(".")[0])
        # fig.show()

        return fig

    def save(self, table: pd.DataFrame, figure: go.Figure, params: str, instance: str):
        instance_id = os.path.split(instance)[-1].split(".")[0]

        os.makedirs(os.path.join('output',
                                 f'{params}',
                                 f'{instance_id}'), exist_ok=True)

        table.to_csv(os.path.join('output',
                                  f'{params}',
                                  f'{instance_id}',
                                  f'results_{self.execution_n}.csv'),
                     index=False)
        figure.write_html(os.path.join('output',
                                       f'{params}',
                                       f'{instance_id}',
                                       f'solution_{self.execution_n}.html'))

    def _get_execution_number(self):
        with open('temp/execution.txt', 'r+') as ex_file:
            self.execution_n = ex_file.read()
            ex_file.seek(0)
            ex_file.write(str(int(self.execution_n) + 1))
            ex_file.truncate()
