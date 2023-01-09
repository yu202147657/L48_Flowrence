import numpy as np
import pickle

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from simulation_builder.scenarios import single_intersec_bal, single_intersec_lop, double_intersec_bal, double_intersec_lop


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    ### INTERVAL SHOULD BE (0.1, 30) AS STANDARD ###
    interval = (0.1, 30)

    ### CHOOSE SCENARIO HERE ###
    g, strategy = single_intersec_bal()
    e = Emulator(g, strategy)

    results, bo_model = e.bayes_opt(
            WaitTimeMetric,
            interval=interval,
            max_iterations=1000,
            progress_N=100,
            num_init_points=1)
    results.to_csv('BO_single_intersec_bal_m52.csv')

    breakpoint()

    ### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    #with open('BO_single_intersec_bal_m52.obj', 'wb') as f:
    #    pickle.dump(bo_model, f)

    #### CHOOSE SCENARIO HERE ###
    #g, strategy = single_intersec_lop()
    #e = Emulator(g, strategy)

    #results, bo_model = e.bayes_opt(WaitTimeMetric, interval=interval, iterations=1000, num_init_points=1)
    #results.to_csv('BO_single_intersec_lop_m52.csv')

    #breakpoint()

    #### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    #with open('BO_single_intersec_lop_m52.obj', 'wb') as f:
    #    pickle.dump(bo_model, f)

    #### CHOOSE SCENARIO HERE ###
    #g, strategy = double_intersec_bal()
    #e = Emulator(g, strategy)

    #results, bo_model = e.bayes_opt(WaitTimeMetric, interval=interval, iterations=1000, num_init_points=1)
    #results.to_csv('BO_double_intersec_bal_rbf.csv')

    #### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    #with open('BO_double_intersec_bal_rbf.obj', 'wb') as f:
    #    pickle.dump(bo_model, f)

    #### CHOOSE SCENARIO HERE ###
    #g, strategy = double_intersec_lop()
    #e = Emulator(g, strategy)

    #results, bo_model = e.bayes_opt(WaitTimeMetric, interval=interval, iterations=1000, num_init_points=1)
    #results.to_csv('BO_double_intersec_lop_rbf.csv')

    #### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    #with open('BO_double_intersec_lop_rbf.obj', 'wb') as f:
    #    pickle.dump(bo_model, f)


    ### READ .OBJ FILE ### (only need if loading one from previous run)

    #with open('bo_model.obj', 'rb') as f:
    #    bo_model = pickle.load(f)

    ### SENSITIVITY ANALYSIS ###

    # main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    # print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    # print('Total Effects\n', total_effects, '\n')
