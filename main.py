import json

import cityflow as cf

from simulation_builder.flows import graph_to_flow
from simulation_builder.roadnets import graph_to_roadnet
from simulation_builder.graph import Graph

if __name__ == "__main__":
	g = Graph([(-300, 300), (0, 300), (300, 300)],
			  [((-300, 300), (0, 300)), ((0, 300), (300, 300))])

	roadnet = graph_to_roadnet(g, 50, lane_width=8)
	flow = graph_to_flow(g)

	with open("cityflow_config/roadnets/auto_roadnet.json", 'w') as f:
		f.write(json.dumps(roadnet, indent=4))

	with open("cityflow_config/flows/auto_flow.json", 'w') as f:
		f.write(json.dumps(flow, indent=4))

	eng = cf.Engine("cityflow_config/config.json", thread_num=1)
	for _ in range(1000):
		eng.next_step()
