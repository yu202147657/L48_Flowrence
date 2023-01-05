# code adapted from https://nbviewer.org/github/emukit/emukit/blob/main/notebooks/Emukit-tutorial-Bayesian-optimization-introduction.ipynb

import numpy as np
import matplotlib.pyplot as plt

from emukit.test_functions import forrester_function
from emukit.core.loop import UserFunctionWrapper

from emukit.examples.gp_bayesian_optimization.single_objective_bayesian_optimization import GPBayesianOptimization
from emukit.core.loop import UserFunctionResult

target_function, space = forrester_function()

X = np.array([[0.1],[0.6],[0.9]])
Y = target_function(X)

num_iterations = 10

bo = GPBayesianOptimization(variables_list=space.parameters, X=X, Y=Y)
results = None

for _ in range(num_iterations):
    X_new = bo.get_next_points(results)
    Y_new = target_function(X_new)
    results = [UserFunctionResult(X_new[0], Y_new[0])]
    print(UserFunctionResult(X_new[0], Y_new[0]))

print(results)

X = bo.loop_state.X
Y = bo.loop_state.Y

x = np.arange(0.0, 1.0, 0.01)
y = target_function(x)

plt.figure()
plt.plot(x, y)
for i, (xs, ys) in enumerate(zip(X, Y)):
    plt.plot(xs, ys, 'ro', markersize=10 + 10 * (i+1)/len(X))

plt.show()
