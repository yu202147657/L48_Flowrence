import numpy as np
import pickle

from emulation.emulator import Emulator
from simulation_builder.scenarios import double_intersec_bal_2, double_intersec_lop_2

from plot import plot_sensitivity

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    np.random.seed(42)

    interval = (1, 30)

    for scenario in ['DB2', 'DL2']:

        for kernel_name in ['M52', 'RQ', 'RBF']:

            if scenario == 'DL2':
                g, strategy = double_intersec_lop_2()
            elif scenario == 'DB2':
                g, strategy = double_intersec_bal_2()

            e = Emulator(g, strategy)

            # define id
            lengthscale = 2
            num_init_points = 50
            metric_name = 'WT'
            variance = 2

            file_id = f'BO_{scenario}_{metric_name}_{kernel_name}_{variance}_{lengthscale}_{num_init_points}'

            with open(f'bo_models/{file_id}.obj', 'rb') as f:
                bo_model = pickle.load(f)

            main_effects, total_effects = e.sensitivity(bo_model, interval=interval)

            plt = plot_sensitivity(main_effects, total_effects, f'sensitivity_plots/{file_id}.png')


