import os
import numpy as np
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots

from pymoo.indicators.hv import HV

from reference_front import calculate_reference_front
from performance_indicators import set_coverage, epsilon_indicator_mul


def get_coincident_instances(result_dir: str, inst_set: str, inst_subset: str) -> list:
    '''Get instances with solutions available for all the analyzed algorithms'''
    instances = []

    # Loop all analyzed algorithms
    algorithms_config = os.listdir(result_dir)
    # algorithms_config = os.listdir("C:/Users/Antor/Desktop/DOC PAPERS/Multi objective DP/nsga-ii-for-multi-objective-diversity-problem/src/output/GKD-b_11_n50_b02_m5_k03")
    for alg in algorithms_config:
        if alg.endswith('.csv'):
            continue

        subset_path = os.path.join(result_dir, alg, inst_set, inst_subset)
        subset_inst = os.listdir(subset_path)
        subset_inst = [i for i in subset_inst if i != 'ex_times.csv']
        instances.append(subset_inst)

    common_instances = list(set.intersection(*map(set, instances)))

    return common_instances


def plot_pareto_fronts(output_dir: str, inst_set: str, inst_subset: str, instances: list):
    '''Plot Pareto Fronts of all the analyzed algorithms'''
    colors = px.colors.qualitative.Plotly
    color_count = 0

    total_rows = len(instances) // 2 + len(instances) % 2

    fig = make_subplots(rows=total_rows, cols=2, subplot_titles=instances)
    for alg in os.listdir(output_dir):
        if alg.endswith('.csv'):
            continue

        col, row = 1, 1
        for count, inst in enumerate(instances):
            inst_path = os.path.join(output_dir, alg, inst_set, inst_subset, inst)
            file = [f for f in os.listdir(inst_path) if f != 'ex_times.csv'][0]

            filename = os.path.join(inst_path, file)

            result_table = pd.read_csv(filename)

            legend_name = 'Constraint values'
            result_table[legend_name] = ('Cost: ' + result_table.Cost.astype(str) +
                                         ' & Capacity: ' + result_table.Capacity.astype(str))

            fig.add_scatter(x=result_table['MaxMin'], y=result_table['MaxSum'],
                            text=result_table[legend_name],
                            mode='markers', line_color=colors[color_count], row=row, col=col,
                            name=alg, legendgroup=alg,
                            showlegend=True if count == 0 else False)

            if col == 2:
                row += 1
                col = 1
            else:
                col += 1

        color_count += 1

    fig.update_traces(marker={'size': 8})
    fig.update_xaxes(title_text='MaxMin')
    fig.update_yaxes(title_text='MaxSum')
    fig.update_layout(height=800)

    fig.show()


def calculate_performance_indicators(result_dir, inst_set, inst_subset):
    '''Calculates performance indicator and saves results in a CSV file'''
    # Initialize result summary table
    general_indicators = pd.DataFrame(columns=['inst', 'alg_config', 'time', 'HV', 'SC', 'eps'])

    # Loop all analyzed algorithms
    algorithms_config = os.listdir(result_dir)
    for alg in algorithms_config:
        if alg.endswith('.csv'):
            continue
        print(f'Evaluating algorithm {alg}')

        # Evaluated instance set path
        set_path = os.path.join(result_dir, alg, inst_set, inst_subset)
        instances = os.listdir(set_path)
        for count, inst in enumerate(instances):
            if inst.endswith('.csv'):
                continue
            print(f'    Evaluating instance {count+1}/{len(instances)}')
            inst_path = os.path.join(set_path, inst)

            # Obtain reference pareto front considering all the solutions
            reference_pareto_front = calculate_reference_front(result_dir,
                                                               inst_set,
                                                               inst_subset,
                                                               inst)
            if reference_pareto_front.empty:
                continue
            reference_pareto_front = reference_pareto_front[['MaxSum', 'MaxMin']].to_numpy()

            # Indicators
            indicators = pd.DataFrame(columns=['HV', 'SC', 'eps'])

            # Loop all the executions run during the experiments (1 csv per execution)
            executions = os.listdir(inst_path)
            for exec in executions:
                if exec == 'ex_times.csv':  # Ignore execution time csv
                    continue
                solutions = pd.read_csv(os.path.join(inst_path, exec))
                current_pareto_front = solutions[['MaxSum', 'MaxMin']].to_numpy()

                # Calculate hypervolume
                ind = HV(ref_point=np.array([0.0, 0.0]))
                # *(-1) since it's a maximization problem
                hypervolume = ind((-1) * current_pareto_front)

                # Calculate Set Coverage
                sc = set_coverage(current_pareto_front, reference_pareto_front)

                # Calculate Epsilon Indicator
                eps = epsilon_indicator_mul(current_pareto_front, reference_pareto_front)

                # Save indicators
                indicators = indicators._append(pd.DataFrame({'HV': [hypervolume],
                                                             'SC': [sc],
                                                             'eps': [eps]}))

            # Get table (csv) containing the exection time of all the experiments
            evaluation_table = pd.read_csv(os.path.join(inst_path, 'ex_times.csv'))
            evaluation_table = evaluation_table.join(indicators.round(2).reset_index(drop=True))

            # Save summary
            summary = pd.DataFrame({'alg_config': [alg]}) \
                .join(pd.DataFrame(evaluation_table.mean()).transpose())
            summary.drop(columns=['ex_number'], inplace=True)
            general_indicators = general_indicators._append(
                pd.DataFrame({'inst': [inst]}).join(summary))

    # Save table with indicator values for each instance-algorithm
    general_indicators['eps'].replace([np.inf, -np.inf], np.nan, inplace=True)
    general_indicators.to_csv(os.path.join(result_dir, 'indicators.csv'))

    # Save table with mean values of the indicators for each algorithm
    mean_indicators = general_indicators.groupby(['alg_config']).mean().round(2)
    mean_indicators.to_csv(os.path.join(result_dir, 'mean_indicators.csv'))