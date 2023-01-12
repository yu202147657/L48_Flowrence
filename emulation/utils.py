import json
from typing import List, Optional, Dict

import numpy as np
import pandas

import cityflow as cf

from emulation.metrics import CompletedJourneysMetric
from simulation_builder.flows import FlowStrategy, graph_to_flow
from simulation_builder.graph import Graph
from simulation_builder.roadnets import graph_to_roadnet


def results_to_df(x, time_period: Optional[float], y: Optional[List[float]] = None, metric_name: Optional[str] = None,
                  num_init_points: Optional[int] = None):
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


def run_simulation(g: Graph, strategy: FlowStrategy, n=1000, traffic_light_phases: Optional[Dict] = None):
    roadnet = graph_to_roadnet(g, traffic_light_phases, intersection_width=50, lane_width=8)
    flow = graph_to_flow(g, strategy)
    with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
        f.write(json.dumps(roadnet, indent=4))

    with open("cityflow_config/flows/auto_flow.json", 'w') as f:
        f.write(json.dumps(flow, indent=4))
    eng = cf.Engine("cityflow_config/config.json", thread_num=1)

    metric = CompletedJourneysMetric()
    for _ in range(n):
        eng.next_step()
        metric.update(eng)
    print(metric.report())


# Test functions
def forrester(x):
    return (6 * x - 2) ** 2 * np.sin(12 * x - 4)


def square_sum(x):
    return (x ** 2).sum(keepdims=True)
