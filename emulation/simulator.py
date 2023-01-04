import json
import os
import uuid
from typing import Optional

import numpy as np
import cityflow as cf

from simulation_builder.flows import FlowStrategy, graph_to_flow
from simulation_builder.graph import Graph
from simulation_builder.roadnets import graph_to_roadnet


class Simulator:
    def __init__(self, g: Graph, metric, strategy=None, timing_period: Optional[int] = None, steps=1000):
        """
        Parameters
        ----------
        g:              Graph of roadnet to run simulation on
        metric:         Metric class to be instantiated upon evaluation, and updated each iteration of the simulation
        strategy:       Flow strategy for the simulation - defaults to uniform flow
        timing_period:  Optional fixed duration for a full traffic light cycle. If specified, the timing of the fourth
                        traffic phase parameter will be inferred - if not, then total duration may vary.
        steps:          Number of steps to run the simulation for.
        """

        self.g = g
        self.metric = metric
        self.strategy = FlowStrategy() if strategy is None else strategy
        self.timing_period = timing_period
        self.steps = steps

        flow = graph_to_flow(self.g, self.strategy)
        with open("cityflow_config/flows/auto_flow.json", 'w') as f:
            f.write(json.dumps(flow, indent=4))

    def evaluate(self, x):
        """
        Parameters
        ----------
        x: A 1D numpy array of traffic light phase timings

        Returns
        -------
        The resulting aggregate metric calculated after N simulation iterations, with traffic light timings x.
        """

        # Infer missing parameters if fixed timing period is specified
        if self.timing_period is not None:
            x3 = np.array([[self.timing_period - x.sum()]])
            x = np.concatenate([x, x3], axis=1)

        traffic_light_phases = {(0, 0): x.flatten().tolist()}
        roadnet = graph_to_roadnet(self.g, traffic_light_phases, intersection_width=50, lane_width=8)

        flow = graph_to_flow(self.g, self.strategy)

        with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
            f.write(json.dumps(roadnet, indent=4))

        with open("cityflow_config/flows/auto_flow.json", 'w') as f:
            f.write(json.dumps(flow, indent=4))

        eng = cf.Engine("cityflow_config/config.json", thread_num=1)

        metric = self.metric()

        for _ in range(self.steps):
            eng.next_step()
            metric.update(eng)

        aggregate, _ = metric.report()

        return np.array([[1 - aggregate]])

    def multithreaded_evaluate(self, x):
        """
        Parameters
        ----------
        x: A 1D numpy array of traffic light phase timings

        Returns
        -------
        The resulting aggregate metric calculated after N simulation iterations, with traffic light timings x.
        """
        x = np.reshape(x, (1, -1))
        # Infer missing parameters if fixed timing period is specified
        if self.timing_period is not None:
            x3 = np.array([[self.timing_period - x.sum()]])
            x = np.concatenate([x, x3], axis=1)

        traffic_light_phases = {(0, 0): x.flatten().tolist()}
        roadnet = graph_to_roadnet(self.g, traffic_light_phases, intersection_width=50, lane_width=8)

        # Generate UUID tag to ensure each thread's config file is unique
        name = str(uuid.uuid1())[:8]

        roadnet_file = f"cityflow_config/roadnets/auto_roadnet_{name}.json"
        with open(roadnet_file, 'w') as f:
            f.write(json.dumps(roadnet, indent=4))
        config_file = f"cityflow_config/config_{name}.json"
        with open(f"cityflow_config/config.json", 'r') as f:
            config = json.loads(f.read())

        config["roadnetFile"] = f"roadnets/auto_roadnet_{name}.json"
        with open(config_file, 'w') as f:
            f.write(json.dumps(config, indent=4))

        eng = cf.Engine(config_file, thread_num=1)

        metric = self.metric()

        for _ in range(self.steps):
            eng.next_step()
            metric.update(eng)

        aggregate, _ = metric.report()
        os.remove(roadnet_file)
        os.remove(config_file)
        return np.array([[1 - aggregate]])