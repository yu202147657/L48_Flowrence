import numpy as np
import pickle

from emulation.emulator import Emulator
from simulation_builder.scenarios import single_intersec_bal, single_intersec_lop, double_intersec_bal, \
    double_intersec_lop, single_intersec_lop_2, single_intersec_bal_2

from plot import plot_sensitivity

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    np.random.seed(42)

    interval = (1, 30)

    for scenario in ['SL2', 'SB2']:

        for kernel_name in ['RBF', 'RQ', 'M52']:

            if scenario == 'SL2':
                g, strategy = single_intersec_lop_2()
            if scenario == 'SB2':
                g, strategy = single_intersec_bal_2()

            e = Emulator(g, strategy)

            # define id
            lengthscale = 1
            num_init_points = 1
            metric_name = 'WT'
            variance = 2

            file_id = f'BO_{scenario}_{metric_name}_{kernel_name}_{variance}_{lengthscale}_{num_init_points}'

            file_id = 'BO_SL2_CJ_M52_2_1_1'
            with open(f'bo_models/{file_id}.obj', 'rb') as f:
                bo_model = pickle.load(f)

            main_effects, total_effects = e.sensitivity(bo_model, interval=interval)

            plt = plot_sensitivity(main_effects, total_effects, f'plots/{file_id}.png')


