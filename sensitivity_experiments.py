import numpy as np
import pickle

from emulation.emulator import Emulator
from simulation_builder.scenarios import double_intersec_bal_2, double_intersec_lop_2, cambridge_scenario

from plot import plot_sensitivity

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    np.random.seed(42)

    interval = (10, 30)

    for kernel_name in ['RQ']:
        g, strategy = cambridge_scenario()

        e = Emulator(g, strategy)

        # define id
        lengthscale = 2
        num_init_points = 50
        metric_name = 'CJ'
        variance = 2

        file_id = f'BO_cambridge_lop_CJ_50'

        with open(f'bo_models/{file_id}.obj', 'rb') as f:
            bo_model = pickle.load(f)

        main_effects, total_effects = e.sensitivity(bo_model, interval=interval)
        print(main_effects)
        print(total_effects)

        plt = plot_sensitivity(main_effects, total_effects, f'sensitivity_plots/{file_id}.png')


