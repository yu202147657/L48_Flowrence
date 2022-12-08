# Problem: Cityflow loops through i, j, and k to create a grid. 
# Need to convert custom graph edges into roadnet structure.

# Assume 2-way traffic along each edge
# Current loop requires a full list of edges (e.g. both 1->2 AND 2->1)

def gridToRoadnet(edges, rowDistances, columnDistances, outRowDistance, outColumnDistance,
                  intersectionWidths, laneWidth=4, laneMaxSpeed=20,
                  numLeftLanes=1, numStraightLanes=1, numRightLanes=1, tlPlan=False, midPoints=10):

    
    #### Unchanged from cityflow#############################
    numLanes = numLeftLanes + numStraightLanes + numRightLanes
    
    x = [[None for _ in range(columnNumber)] for _ in range(rowNumber)]
    y = [[None for _ in range(columnNumber)] for _ in range(rowNumber)]

    rowDistances = [outRowDistance] + rowDistances + [outRowDistance]
    columnDistances = [outColumnDistance] + columnDistances + [outColumnDistance]
    
    for i in range(rowNumber):
        for j in range(columnNumber):
            if j > 0:
                x[i][j] = x[i][j - 1] + rowDistances[i - 1]
                y[i][j] = y[i][j - 1]
            elif i > 0:
                x[i][j] = x[i - 1][j]
                y[i][j] = y[i - 1][j] + columnDistances[j - 1]
            else:
                x[i][j] = -outRowDistance
                y[i][j] = -outColumnDistance
     ###########################################################           
    
    #Create as many roads/intersections as edges (as opposed to as many roads in a ixj grid)
    roads = [[None, None, None, None] for _ in range(len(edges))]
    intersections = [None for _ in range(len(edges))]

    
    for index, pair in enumerate(edges):

        i = pair[0][1]
        j = pair[0][0]
        ni = pair[1][1]
        nj = pair[1][0]

        if ni == i and nj > j:
        #traveling east
            k = 0
        elif ni == i and nj < j:
        #traveling west 
            k = 2
        elif nj == j and ni > i:
        #traveling north
            k = 1
        else:
        #traveling south
            k = 3

        road = {
            "id": "road_%d_%d_%d" % (j, i, k),
            "direction": k,
            "fromi": i,
            "fromj": j,
            "toi": ni,
            "toj": nj,
            "points": [
                pointToDict(x[i][j], y[i][j]),
                pointToDict(x[ni][nj], y[ni][nj])
            ],
            "lanes": [
                {
                    "width": laneWidth,
                    "maxSpeed": laneMaxSpeed
                }
            ] * numLanes,
            "startIntersection": "intersection_%d_%d" % (j, i),
            "endIntersection": "intersection_%d_%d" % (nj, ni)
        }
        roads[index] = road

