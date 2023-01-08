import numpy as np

from emulation.emulator import Emulator
from emulation.metrics import CompletedJourneysMetric, WaitTimeMetric
from simulation_builder.scenarios import single_intersec_bal

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g, strategy = single_intersec_bal()

    e = Emulator(g, strategy)

    results, bo_model = e.bayes_opt(CompletedJourneysMetric, interval=(0.1, 20), iterations=5)
    print(results)
    main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    print('Total Effects\n', total_effects, '\n')

    results, bo_model = e.bayes_opt(WaitTimeMetric, interval=(0.1, 20), iterations=5)
    print(results)
    main_effects, total_effects = e.sensitivity(bo_model, interval=(0.1, 20))
    print('\nSENSITIVITY ANALYSIS\n', 'Main Effects\n', main_effects)
    print('Total Effects\n', total_effects, '\n')

    print(e.grid_search_opt(CompletedJourneysMetric, interval=(0.1, 20), steps_per_axis=2))
    print(e.grid_search_opt(WaitTimeMetric, interval=(0.1, 20), steps_per_axis=2))
