def valid_node(x, y, grid, end_points):                                         #RETURNS TRUE/FALSE IS CELL IS NODE OR NOT
    if grid[y][x] == 1 : return False                                           #CELL IS WALL
    if [x,y] in end_points : return True
    nbrs_h = 0                                                                  #COUNT NUMBER OF HORIZONTAL/VERTICAL NBRS
    nbrs_v = 0
    if x > 0 : nbrs_h += 1 - grid[y][x-1]
    if y > 0 : nbrs_v += 1 - grid[y-1][x]
    if x < len(grid[y])-1 : nbrs_h += 1 - grid[y][x+1]
    if y < len(grid)-1 : nbrs_v += 1 - grid[y+1][x]
    if nbrs_h + nbrs_v > 2 : return True                                        #CELL IS JUNCTION
    if nbrs_h == 1 and nbrs_v == 1 : return True                                #CELL IS CORNER
    return False

def get_nodes(grid, end_points):                                                #RETURNS LIST OF NODE POS AND NBR POS
    nodes = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if valid_node(x, y, grid, end_points):
                nbr_left = -1
                nbr_up = -1
                for s in range(x-1, -1, -1):                                    #FIND NBR TO LEFT
                    if valid_node(s, y, grid, end_points):
                        nbr_left = s
                        break
                    elif grid[y][s] == 1:
                        break
                for s in range(y-1, -1, -1):                                    #FIND NBR ABOVE
                    if valid_node(x, s, grid, end_points):
                        nbr_up = s
                        break
                    elif grid[s][x] == 1:
                        break
                nodes.append([x, y, nbr_left, nbr_up])
    return nodes

def adjacency_dict(nodes_list):                                                 #RETURNS DICTIONARY OF ADJACENCIES
    adj_dict = {}
    for node_data in nodes_list:
        node_id = str(node_data[0]) + '-' + str(node_data[1])
        adj_dict[node_id] = []  
        if node_data[2] >= 0:                                                   #IF ADJACENCY EXISTS
            left_id = str(node_data[2]) + '-' + str(node_data[1])
            adj_dict[node_id].append(left_id)                                   #ADD ADJACENCY BOTH WAYS
            adj_dict[left_id].append(node_id)
        if node_data[3] >= 0:
            up_id = str(node_data[0]) + '-' + str(node_data[3])
            adj_dict[node_id].append(up_id)
            adj_dict[up_id].append(node_id)
    return adj_dict

g = [[1,0,1,1,0],                                                               #TEST GRID
     [0,0,0,0,0],
     [0,1,0,1,1],
     [0,1,0,1,0],
     [0,0,0,0,0]]
ep = [[0,2], [2,2]]                                                             #TEST END POINTS
nodes_list = get_nodes(g, ep)
adj_dict = adjacency_dict(nodes_list)
for key in adj_dict.keys():
    print(key, adj_dict[key])
