'''Class to handle result plotting and saving'''
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class OutputHandler:
    '''Class to handle result plotting and saving'''
    def __init__(self):
        '''Initialize OutputHandler'''
        self.execution_n = -1

        self._get_execution_number()

    def pareto_front(self, table: pd.DataFrame, instance: str) -> go.Figure:
        '''
        Generates a scatter plot using data from a DataFrame and customizes the plot.

        Args:
          table (pd.DataFrame): contains solution data.
          instance (str): represents the name or path of a specific file (instance).

        Returns:
          (go.Figure): figure with solution's Pareto Front plot.
        '''
        table['Constraint values'] = ('Cost: ' + table.Cost.astype(str) +
                                      ' & Capacity: ' + table.Capacity.astype(str))
        fig = px.scatter(table, x='MaxMin', y='MaxSum', color='Constraint values')
        fig.update_layout(title_text=os.path.split(instance)[-1].split(".")[0])
        # fig.show()

        return fig

    def save(self, table: pd.DataFrame, figure: go.Figure, params: str, instance: str):
        '''
        This function saves the solution DataFrame as a CSV and the Figure as an HTML file in a
        specified directory structure that contains the instance name and execution number as ID.

        Args:
          table (pd.DataFrame): contains solution data.
          figure (go.Figure): figure with solution's Pareto Front plot.
          params (str): parameter configuration used in the optimization algorithm.
          instance (str): represents the name or path of a specific file (instance).
        '''
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
        '''
        The function reads an execution number from a file, increments it by 1, and writes the
        updated number back to the file.
        '''
        with open('temp/execution.txt', 'r+') as ex_file:
            self.execution_n = ex_file.read()
            ex_file.seek(0)
            ex_file.write(str(int(self.execution_n) + 1))
            ex_file.truncate()
