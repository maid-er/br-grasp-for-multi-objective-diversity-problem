'''Main function to execute instance solution set evaluation'''
import os
import numpy as np
import pandas as pd
from pymoo.indicators.hv import HV

from reference_front import calculate_reference_front
from performance_indicators import set_coverage, epsilon_indicator


if __name__ == '__main__':

    # Evaluated instance set path
    set_path = os.path.join('output', 'GDP_test', 'SOM-a')

    general_indicators = pd.DataFrame(columns=['inst', 'config', 'time', 'HV', 'SC', 'eps'])

    instances = os.listdir(set_path)
    for count, inst in enumerate(instances):
        if inst.endswith('.csv'):
            continue
        print(f'Evaluating instance {count+1}/{len(instances)}')
        inst_path = os.path.join(set_path, inst)
        reference_pareto_front = calculate_reference_front(inst_path)
        if reference_pareto_front.empty:
            continue
        reference_pareto_front = reference_pareto_front[['MaxSum', 'MaxMin']].to_numpy()

        config_comparison = pd.DataFrame(columns=['config', 'time', 'HV', 'SC', 'eps'])
        configurations = os.listdir(inst_path)
        for config in configurations:

            indicators = pd.DataFrame(columns=['HV', 'SC', 'eps'])

            config_path = os.path.join(inst_path, config)
            executions = os.listdir(config_path)
            for exec in executions:
                if exec == 'ex_times.csv':
                    continue
                solutions = pd.read_csv(os.path.join(config_path, exec))
                current_pareto_front = solutions[['MaxSum', 'MaxMin']].to_numpy()

                # Calculate hypervolume
                ind = HV(ref_point=np.array([0.0, 0.0]))
                # *(-1) since it's a maximization problem
                hypervolume = ind((-1) * current_pareto_front)

                # Calculate Set Coverage
                sc = set_coverage(current_pareto_front, reference_pareto_front)

                # Calculate Epsilon Indicator
                eps = epsilon_indicator(current_pareto_front, reference_pareto_front)

                indicators = indicators.append(pd.DataFrame({'HV': [hypervolume],
                                                             'SC': [sc],
                                                             'eps': [eps]}))

            evaluation_table = pd.read_csv(os.path.join(config_path, 'ex_times.csv'))
            evaluation_table = evaluation_table.join(indicators.round(2).reset_index(drop=True))

            summary = pd.DataFrame({'config': [config]}) \
                .join(pd.DataFrame(evaluation_table.mean()).transpose())
            summary.drop(columns=['ex_number'], inplace=True)

            config_comparison = config_comparison.append(summary)
            general_indicators = general_indicators.append(
                pd.DataFrame({'inst': [inst]}).join(summary))

        # config_comparison.to_csv(os.path.join(inst_path, 'indicators.csv'))

    general_indicators['eps'].replace([np.inf, -np.inf], np.nan, inplace=True)
    general_indicators = general_indicators.groupby(['config']).mean().round(2)
    general_indicators.to_csv(os.path.join(set_path, 'general_indicators.csv'))
