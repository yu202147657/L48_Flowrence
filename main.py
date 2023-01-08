import numpy as np

from emulation.emulator import Emulator
from metrics import CompletedJourneysMetric, WaitTimeMetric

from simulation_builder.scenarios import single_intersec_bal

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g, strategy = single_intersec_bal()

    e = Emulator(g, strategy, fixed_time_period=60)

    print(e.bayes_opt(CompletedJourneysMetric, interval=(0.1, 20), iterations=5))
    print(e.bayes_opt(WaitTimeMetric, interval=(0.1, 20), iterations=5))

    print(e.grid_search_opt(CompletedJourneysMetric, interval=(0.1, 20), steps_per_axis=2))
    print(e.grid_search_opt(WaitTimeMetric, interval=(0.1, 20), steps_per_axis=2))
