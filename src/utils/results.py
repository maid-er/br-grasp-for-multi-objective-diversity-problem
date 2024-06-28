import pandas as pd
import plotly.express as px


def pareto_front(table: pd.DataFrame, instance: str):
    table['Constraint values'] = ('Cost: ' + table.Cost.astype(str) +
                                  ' & Capacity: ' + table.Capacity.astype(str))
    fig = px.scatter(table, x='MaxMin', y='MaxSum', color='Constraint values')
    fig.update_layout(title_text=instance.split(".")[0])
    fig.show()

    return fig
