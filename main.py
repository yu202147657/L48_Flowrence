import cityflow as cf
from utils import generate_roadnet

if __name__ == "__main__":
	generate_roadnet(rowNum=2, colNum=2, numStraightLanes=1, numLeftLanes=1, numRightLanes=1)
	eng = cf.Engine("cityflow_config/config.json", thread_num=1)
	for _ in range(1000):
		eng.next_step()
