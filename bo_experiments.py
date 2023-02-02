import numpy as np
import pickle
import matplotlib.pyplot as plt
import pandas as pd

from GPy.kern import Matern52, RBF, RatQuad

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from emulation.utils import run_simulation
from plot import plot_metric_results
from simulation_builder.scenarios import single_intersec_lop_2, single_intersec_bal_2, double_intersec_lop_2, \
    double_intersec_bal_2, cambridge_scenario


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    interval = (10, 30)
    N = 300
    num_init_points = 50

    # metric = WaitTimeMetric
    # metric_name = "WT"
    metric = CompletedJourneysMetric
    metric_name = "CJ"

    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    file_id = f'BO_cambridge_lop_{metric_name}_{num_init_points}'

    print(file_id)
    g, strategy = cambridge_scenario()

    kernel_func = RatQuad
    kernel_kwargs = {'variance': 1, 'lengthscale': 2}

    e = Emulator(g, strategy)

    results, bo_model = e.bayes_opt(
        kernel_func,
        kernel_kwargs,
        metric,
        interval=interval,
        max_iterations=N,
        progress_N=300,
        num_init_points=num_init_points)

    with open(f'bo_models/{file_id}.obj', 'wb') as f:
        pickle.dump(bo_model, f)

    results.to_csv(f'csv_files/{file_id}.csv')
    data = results[results.columns[-1]]

    plt.plot(np.arange(len(data) - num_init_points) + num_init_points, data[num_init_points:], zorder=1)
    # plt.scatter(num_init_points, data[num_init_points], s=100, zorder=2)
    print(f"{metric_name} Results: ")
    print(data[num_init_points:])
    # plt.legend(fontsize="large")
    plt.xlabel("Iterations")
    plt.ylabel("Completed Journeys" if metric_name == "CJ" else "Average Wait Time")
    plt.savefig(f"plots/kernel_tuning/cambridge_{metric_name}_", bbox_inches='tight', pad_inches=0.2)
    plt.close()
