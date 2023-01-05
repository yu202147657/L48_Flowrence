from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
from typing import List


@dataclass
class Report:
    target_metric: Number  # 'normalised' for minimisation
    raw_metric: Number

    def __iter__(self):
        return iter((self.target_metric, self.raw_metric))


class Metric(ABC):
    @abstractmethod
    def update(self, eng):
        pass

    @abstractmethod
    def report(self) -> Report:
        pass

    name: str


class CompletedJourneysMetric(Metric):
    def __init__(self):
        self._total_vehicles = set() # unique vehicles in simulation
        self.name = 'completed journeys'

    def update(self, eng):

        # get all vehicles currently in simulation
        self._current_vehicles = set(eng.get_vehicles(include_waiting=True))

        # add new vehicles to total count
        self._total_vehicles |= self._current_vehicles

    def report(self) -> Report:

        # find the vehicles that had left simulator by last step
        total_completed = len(self._total_vehicles - self._current_vehicles)

        # optimisation target is 1 - (normalised total completed)
        target_metric = 1 - total_completed / len(self._total_vehicles)

        return Report(target_metric, total_completed)


class WaitTimeMetric(Metric):
    def __init__(self):
        self._unique_vehicles = set()  # unique vehicles in simulation (should be constant for given graph + flow)
        self._waiting_vehicle_steps = []  # a vehicle step is 1 vehicle waiting for 1 step
        self.name = 'average steps waiting'

    def update(self, eng):

        # get all vehicles currently in simulation, including those waiting offscreen
        current_vehicles = eng.get_vehicles(include_waiting=True)

        # add new vehicles to set of unique 
        self._unique_vehicles |= set(current_vehicles)

        # find the waiting vehicles
        waiting = 0
        for i, v in enumerate(current_vehicles):

            # get vehicle info from engine
            info = eng.get_vehicle_info(v)

            # check if car on road
            if info['running'] == '1':
                # get speed of car
                speed = float(info['speed'])
            else:
                # cars not on road have no key 'speed'
                speed = 0.0

            # check if speed is below threshold, add to count of waiting
            if speed < 0.1:
                waiting += 1

        # add waiting vehicles to stepwise list
        self._waiting_vehicle_steps.append(waiting)

    def report(self) -> Report:

        # computes the average proportion of time vehicles spent waiting in their journey
        total_average = sum(self._waiting_vehicle_steps) / len(self._unique_vehicles)

        # divide by number of steps (can't normalise as is not bounded)
        target_metric = total_average / len(self._waiting_vehicle_steps)

        return Report(target_metric, total_average)
