from typing import List, Optional

import numpy as np
import pandas


def results_to_df(x, time_period: Optional[float], y: Optional[List[float]] = None, metric_name: Optional[str] = None, num_init_points: Optional[int] = None):
    """
    Parameters
    ----------
    x:              Array-like (2D) list where each row represents a set of parameter values
    y:              Array-like (1D) list of results of simulation run
    metric_name:    Name for results column title
    time_period:    If specified, inserts a fourth column for every three parameters in x, and infers value from other three.

    Returns
    _______
    Dataframe representing results as table
    """
    d = {}

    if num_init_points != None:
        eval_type = ['init'] * num_init_points + ['BO'] * (x.shape[0] - num_init_points)
        d['eval type'] = eval_type

    for i in range(x.shape[1]):
        if time_period is not None:
            node, phase = i // 3, i % 3
            d[f"x_{node}_{phase}"] = np.array(x[:, i])
            if i % 3 == 2:
                d[f"x_{node}_3 (i)"] = time_period - x[:, i - 2:i + 1].sum(axis=1)
        else:
            node, phase = i // 4, i % 4
            d[f"x_{node}_{phase}"] = np.array(x[:, i])

    if y is not None:
        d[metric_name] = np.array(y).flatten()

    df = pandas.DataFrame(data=d)
    return df


# Test functions
def forrester(x):
    return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


def square_sum(x):
    return (x ** 2).sum(keepdims=True)
