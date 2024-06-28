'''Main function'''
import datetime
import plotly.express as px
import os
import pandas as pd

from structure import instance, dominance
from algorithms import grasp

from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config = read_config('config')


# def executeInstance():
#     random.seed(1309)
#     path = "instances/preliminar/MDG-a_1_100_m10.txt"
#     inst = instance.read_instance(path)
#     sol = grasp.execute(inst, 100, config[0])
#     solution.print_sol(sol)


def executeDir():
    all_solutions = []
    dir = "instances/USCAP"
    with os.scandir(dir) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    for f in ficheros:
        logging.info('Solving instance %s:', f)
        for i in range(100):
            path = os.path.join(dir, f)
            logging.info(f'Finding solution #{i+1}')
            inst = instance.read_instance(path)
            for method_config in config:
                start = datetime.datetime.now()
                sol = grasp.execute(inst, method_config)
                elapsed = datetime.datetime.now() - start
                secs = round(elapsed.total_seconds(), 2)
                logging.info('MaxSum objective function value for the best result: %s',
                             sol.of_MaxSum)
                logging.info('MaxMin objective function value for the best result: %s',
                             sol.of_MaxMin)
                logging.info('Execution time: %s', secs)

                all_solutions.append(sol)

                selected_nodes = ' - '.join([str(s+1) for s in sorted(sol.solution_set)])
                result_table.loc[len(result_table)] = [selected_nodes] + [sol.of_MaxSum,
                                                                          sol.of_MaxMin,
                                                                          sol.total_cost,
                                                                          sol.total_capacity]

            logging.info('Final solution:')
            logging.info('Selected elements: %s', sol.solution_set)
            logging.info('MaxSum objective function value for the best result: %s',
                         sol.of_MaxSum)
            logging.info('MaxMin objective function value for the best result: %s',
                         sol.of_MaxMin)
            logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

        fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color='Solution')
        fig.show()

        is_non_dominated = dominance.get_nondominated_solutions(all_solutions)
        result_table = result_table[is_non_dominated].reset_index(drop=True)

        result_table['Constraint values'] = ('Cost: ' + result_table.Cost.astype(str) +
                                             ' & Capacity: ' + result_table.Capacity.astype(str))
        fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color='Constraint values')
        fig.update_layout(title_text=f.split(".")[0])
        fig.show()

        with open('temp/execution.txt', 'r+') as ex_file:
            execution_n = ex_file.read()
            ex_file.seek(0)
            ex_file.write(str(int(execution_n) + 1))
            ex_file.truncate()
        os.makedirs(f'output/{f.split(".")[0]}', exist_ok=True)

        result_table.to_csv(f'output/{f.split(".")[0]}/results_{f.split(".")[0]}_{execution_n}.csv',
                            index=False)
        fig.write_html(f'output/{f.split(".")[0]}/solution_{execution_n}.html')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')
    # executeInstance()
    executeDir()
