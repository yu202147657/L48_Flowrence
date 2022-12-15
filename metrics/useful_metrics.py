import numpy as np

set_ids = set()
last_step = None
counter = 0

def completed_journeys(eng, online = False):
    """Returns online or total completed journeys"""
    global last_step
    # List of vehicle IDs currently on road
    current_ids = eng.get_vehicles(include_waiting=False)

    # If want completed journeys at each time step:
    if online:
        # If function is called for the first time
        if last_step is None:
            last_step = current_ids
            return
        # Yields the elements in last_step that are NOT in current_ids
        completed_ids = np.setdiff1d(last_step, current_ids)
        completed_journeys = len(completed_ids)

        last_step = current_ids
        return completed_journeys

    # total = set of car ids - number of cars on road at last step
    set_ids.update(current_ids)
    total_completed_journeys = len(set_ids) - len(eng.get_vehicles())

    return total_completed_journeys

def count_waiting_cars(eng, current_ids, counter):
    for car in current_ids:
        # CityFlow defines a waiting car
        # as speed < 0.1 mph
        if float(eng.get_vehicle_info(car)['speed']) < 0.1:
            counter += 1


def wait_time(eng, _ = False, steps = False, online = False):
    """Returns online or total average wait"""
    #List of IDs of cars currently on road
    current_ids = eng.get_vehicles(include_waiting=False)

    # If want average wait across entire simulation
    global counter
    for car in current_ids:
        # CityFlow defines a waiting car
        # as speed < 0.1 mph
        if float(eng.get_vehicle_info(car)['speed']) < 0.1:
            counter += 1
    set_ids.update(current_ids)
    # If last step of simulation, calculate total avg
    if _ == steps - 1:
        # avg = num of times cars were idle in sim / num cars in sim
        total_avg = counter / len(set_ids)
        return total_avg

    # If want average wait at each time step
    if online:
        counter = 0
        for car in current_ids:
            # CityFlow defines a waiting car
            # as speed < 0.1 mph
            if float(eng.get_vehicle_info(car)['speed']) < 0.1:
                counter += 1
        if counter == 0:
            return
        # avg = num cars that were idle / num cars on road
        avg = counter / len(eng.get_vehicles())
        return avg
    

