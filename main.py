import numpy as np

from simulation_builder.graph import Graph
from emulator.emulation import Simulator, random_sampling, bayesian_optimisation, square_sum

if __name__ == "__main__":

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    g = Graph([(0, -400), (0, 0), (0, 400), (-400, 0), (400, 0)],
            [((0, -400), (0, 0)), ((0, 400), (0, 0)), ((-400, 0), (0, 0)), ((400, 0), (0, 0))])

    simulator = Simulator(g)

    print()
    print('BO on squared sum, 20 iterations')
    bayesian_optimisation(square_sum, num_parameters = 3, interval = (-4, 4), num_iterations = 20)

    print()
    print('RANDOM SAMPLING ON CITYFLOW, 20 ITERATIONS')
    random_sampling(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)

    print()
    print('BO ON CITYFLOW, 20 ITERATIONS')
    bayesian_optimisation(simulator.evaluate, num_parameters = 4, interval = (0.1, 4), num_iterations = 20)

