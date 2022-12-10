import json
import os

from CityFlow.tools.generator.generate_json_from_grid import gridToRoadnet


def generate_roadnet(rowNum: int, colNum: int, rowDistance: int = 300, columnDistance: int = 300,
					 intersectionWidth: int = 100, numLeftLanes: int = 1, numStraightLanes: int = 1,
					 numRightLanes: int = 1, laneMaxSpeed: float = 16.67, vehLen: float = 5.0, vehWidth: float = 2.0,
					 vehMaxPosAcc: float = 2.0, vehMaxNegAcc: float = 4.5, vehUsualPosAcc: float = 2.0,
					 vehUsualNegAcc: float = 4.5,
					 vehMinGap: float = 2.5, vehMaxSpeed: float = 16.67, vehHeadwayTime: float = 1.5,
					 directory: str = "cityflow_config", roadnetFile: str = None, turn: bool = False,
					 tlPlan: bool = False, interval: float = 2.0,
					 flowFile: str = None):
	"""
	Generates grid-shaped roadnet and flow JSON files, and updates config.json file.

	(Code adapted from CityFlows/tools/generator directory)
	"""

	# Helper function
	def generate_route(rowNum, colNum, turn=False):
		routes = []
		move = [(1, 0), (0, 1), (-1, 0), (0, -1)]

		def get_straight_route(start, direction, step):
			x, y = start
			route = []
			for _ in range(step):
				route.append("road_%d_%d_%d" % (x, y, direction))
				x += move[direction][0]
				y += move[direction][1]
			return route

		for i in range(1, rowNum + 1):
			routes.append(get_straight_route((0, i), 0, colNum + 1))
			routes.append(get_straight_route((colNum + 1, i), 2, colNum + 1))
		for i in range(1, colNum + 1):
			routes.append(get_straight_route((i, 0), 1, rowNum + 1))
			routes.append(get_straight_route((i, rowNum + 1), 3, rowNum + 1))

		if turn:
			def get_turn_route(start, direction):
				if direction[0] % 2 == 0:
					step = min(rowNum * 2, colNum * 2 + 1)
				else:
					step = min(colNum * 2, rowNum * 2 + 1)
				x, y = start
				route = []
				cur = 0
				for _ in range(step):
					route.append("road_%d_%d_%d" % (x, y, direction[cur]))
					x += move[direction[cur]][0]
					y += move[direction[cur]][1]
					cur = 1 - cur
				return route

			routes.append(get_turn_route((1, 0), (1, 0)))
			routes.append(get_turn_route((0, 1), (0, 1)))
			routes.append(get_turn_route((colNum + 1, rowNum), (2, 3)))
			routes.append(get_turn_route((colNum, rowNum + 1), (3, 2)))
			routes.append(get_turn_route((0, rowNum), (0, 3)))
			routes.append(get_turn_route((1, rowNum + 1), (3, 0)))
			routes.append(get_turn_route((colNum + 1, 1), (2, 1)))
			routes.append(get_turn_route((colNum, 0), (1, 2)))

		return routes

	if roadnetFile is None:
		roadnetFile = "roadnet_%d_%d%s.json" % (rowNum, colNum, "_turn" if turn else "")
	if flowFile is None:
		flowFile = "flow_%d_%d%s.json" % (rowNum, colNum, "_turn" if turn else "")

	grid = {
		"rowNumber": rowNum,
		"columnNumber": colNum,
		"rowDistances": [rowDistance] * (colNum - 1),
		"columnDistances": [columnDistance] * (rowNum - 1),
		"outRowDistance": rowDistance,
		"outColumnDistance": columnDistance,
		"intersectionWidths": [[intersectionWidth] * colNum] * rowNum,
		"numLeftLanes": numLeftLanes,
		"numStraightLanes": numStraightLanes,
		"numRightLanes": numRightLanes,
		"laneMaxSpeed": laneMaxSpeed,
		"tlPlan": tlPlan
	}

	json.dump(gridToRoadnet(**grid), open(os.path.join(directory, "roadnets/", roadnetFile), "w"), indent=4)

	vehicle_template = {
		"length": vehLen,
		"width": vehWidth,
		"maxPosAcc": vehMaxPosAcc,
		"maxNegAcc": vehMaxNegAcc,
		"usualPosAcc": vehUsualPosAcc,
		"usualNegAcc": vehUsualNegAcc,
		"minGap": vehMinGap,
		"maxSpeed": vehMaxSpeed,
		"headwayTime": vehHeadwayTime
	}
	routes = generate_route(rowNum, colNum, turn)
	flow = []
	for route in routes:
		flow.append({
			"vehicle": vehicle_template,
			"route": route,
			"interval": interval,
			"startTime": 0,
			"endTime": -1
		})
	json.dump(flow, open(os.path.join(directory, "flows/", flowFile), "w"), indent=4)

	with open("cityflow_config/config.json", "r") as f:
		config_file = json.load(f)

	config_file["roadnetFile"] = f"roadnets/{roadnetFile}"
	config_file["flowFile"] = f"flows/{flowFile}"

	with open("cityflow_config/config.json", "w") as f:
		json.dump(config_file, f, indent=4)
