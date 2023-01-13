import numpy as np
import pickle

from GPy.kern import Matern52, RBF

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from emulation.utils import run_simulation
from plot import plot_metric_results
from simulation_builder.scenarios import single_intersec_bal, single_intersec_lop, double_intersec_bal, \
    double_intersec_lop, single_intersec_lop_2, single_intersec_bal_2

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    interval = (1, 30)

    for scenario in ['SL2', 'SB2']:

        for lengthscale in [1, 2, 4, 8]:

            # define id
            num_init_points = 1
            metric_name = 'CJ'
            variance = 2

            # id -> config
            if scenario == 'SL2':
                g, strategy = single_intersec_lop_2()
            if scenario == 'SB2':
                g, strategy = single_intersec_bal_2()

            if kernel_name == 'M52':
                kernel_func = Matern52
            elif kernel_name == 'RBF':
                kernel_func = RBF

            if metric_name == 'WT':
                metric = WaitTimeMetric
            elif metric_name == 'CJ':
                metric = CompletedJourneysMetric

            kernel_kwargs = {'variance': variance, 'lengthscale': lengthscale}

            e = Emulator(g, strategy)

            results, bo_model = e.bayes_opt(
                kernel_func,
                kernel_kwargs,
                metric,
                interval=interval,
                max_iterations=200,
                progress_N=200,
                num_init_points=num_init_points)

            file_id = f'BO_{scenario}_{metric_name}_{kernel_name}_{variance}_{lengthscale}_{num_init_points}'

            results.to_csv(f'csv_files/{file_id}.csv')

            plt = plot_metric_results(results, f'plots/{file_id}.png')

            with open(f'bo_models/{file_id}.obj', 'wb') as f:
                pickle.dump(bo_model, f)
