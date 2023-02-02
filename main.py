import matplotlib.pyplot as plt
import numpy as np
import pickle

import pandas as pd
from GPy.kern import Matern52, RBF, RatQuad

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from emulation.utils import run_simulation
from plot import plot_metric_results
from simulation_builder.scenarios import single_intersec_lop_2, single_intersec_bal_2, cambridge_scenario, \
    double_intersec_bal_2



def plot_cum(file_name, new_name=""):
    df = pd.read_csv(file_name)

    met_name = df.columns[-1]
    res = df[met_name]

    file = f'plots/cambridge/cum_{new_name}.png'

    if False:
        cuma = res.cummin()
    else:
        cuma = res.cummax()

    plt.figure()
    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    plt.plot(np.arange(len(res)), res, )
    plt.plot(np.arange(len(res)), cuma)
    plt.legend(['Actual', 'Cumulative'])
    plt.xlabel("Iterations")
    plt.ylabel("Completed Journeys")
    # plt.title(file_id)
    plt.savefig(file, bbox_inches='tight', pad_inches=0.2)


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    interval = (0.1, 30)

    np.random.seed(42)

    # g, strategy = double_intersec_bal_2()
    g, strategy = cambridge_scenario()
    run_simulation(g, strategy)
    # plot_cum("csv_files/BO_cambridge_lop_CJ_50.csv", "CJ_lop")

    # for scenario in ['DB2']:
    #     for kernel_name in ['RQ', 'RBF']:
    #
    #         # define id
    #         scenario = 'SL2'
    #         num_init_points = 1
    #         metric_name = 'WT'
    #         variance = 2
    #
    #         # id -> config
    #         if scenario == 'SL2':
    #             g, strategy = single_intersec_lop_2()
    #         if scenario == 'SB2':
    #             g, strategy = single_intersec_bal_2()
    #
    #         if kernel_name == 'M52':
    #             kernel_func = Matern52
    #         elif kernel_name == 'RBF':
    #             kernel_func = RBF
    #         else:
    #             kernel_func = RatQuad
    #
    #         if metric_name == 'WT':
    #             metric = WaitTimeMetric
    #         else:
    #             metric = CompletedJourneysMetric
    #
    #         kernel_kwargs = {'variance': variance}
    #
    #         e = Emulator(g, strategy)
    #
    #         results, bo_model = e.bayes_opt(
    #             kernel_func,
    #             kernel_kwargs,
    #             metric,
    #             interval=interval,
    #             max_iterations=250,
    #             progress_N=500,
    #             num_init_points=num_init_points)
    #
    #         file_id = f'BO_{scenario}_{metric_name}_{kernel_name}_{variance}_{num_init_points}'
    #
    #         results.to_csv(f'csv_files/{file_id}.csv')
    #
    #         plot_metric_results(results, f'plots/{file_id}.png')
    #
    #         with open(f'bo_models/{file_id}.obj', 'wb') as f:
    #             pickle.dump(bo_model, f)
