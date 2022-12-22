from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
from typing import List


@dataclass
class Report:
    aggregate: Number
    data: List[Number]

    def __iter__(self):
        return iter((self.aggregate, self.data))


class Metric(ABC):
    @abstractmethod
    def update(self, eng):
        pass

    @abstractmethod
    def report(self) -> Report:
        pass


class CompletedJourneysMetric(Metric):
    def __init__(self):
        self._prev_step = set()
        self._completed_journeys = [0]

    def update(self, eng):
        curr_step = set(eng.get_vehicles(include_waiting=False))
        self._completed_journeys.append(len(self._prev_step - curr_step) + self._completed_journeys[-1])
        self._prev_step = curr_step

    def report(self) -> Report:
        return Report(self._completed_journeys[-1], self._completed_journeys)


class WaitTimeMetric(Metric):
    """
    Reports the overall average waiting time, and the proportion of cars waiting at each time step.
    """
    def __init__(self):
        self._waiting_vehicles = []
        self._total_vehicles = []

    def update(self, eng):
        vehicles = eng.get_vehicles(include_waiting=False)
        wait_time = sum([float(eng.get_vehicle_info(v)['speed']) < 0.1 for v in vehicles])
        self._total_vehicles.append(len(vehicles))
        self._waiting_vehicles.append(wait_time)

    def report(self) -> Report:
        total_average = sum(self._waiting_vehicles) / sum(self._total_vehicles)
        proportion_waiting = [wait / total if total > 0 else 0 for wait, total in
                              zip(self._waiting_vehicles, self._total_vehicles)]
        return Report(total_average, proportion_waiting)
