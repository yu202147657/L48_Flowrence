import numpy as np
import pickle

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from simulation_builder.scenarios import single_intersec_bal, single_intersec_lop


if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    ### CHOOSE SCENARIO HERE ###
    g, strategy = single_intersec_bal()

    e = Emulator(g, strategy)

    ### INTERVAL SHOULD BE (0.1, 30) AS STANDARD ###
    interval = (0.1, 30)

    results, bo_model = e.bayes_opt(WaitTimeMetric, interval=interval, iterations=5)

    ### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    results.to_csv('BO.csv')
    with open('bo_model.obj', 'wb') as f:
        pickle.dump(bo_model, f)

    results = e.grid_search_opt(WaitTimeMetric, interval=interval, steps_per_axis=5)

    ### BE CAREFUL NOT TO OVERWRITE FILES YOU WANT TO KEEP ###
    results.to_csv('GS.csv')

    ### READ .OBJ FILE ### (only need if loading one from previous run)

    #with open('bo_model.obj', 'rb') as f:
    #    bo_model = pickle.load(f)

    ### SENSITIVITY ANALYSIS ###

    # main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    # print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    # print('Total Effects\n', total_effects, '\n')
