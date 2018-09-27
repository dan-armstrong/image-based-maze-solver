import structures
import update
import csv


class Node:                                                                     #STORES DETAILS ABOUT INDIVIDUAL NODES
    def __init__(self, id_tag, prev_node, end, nbrs):
        try:                                                                    #CHECK ID IS IN CORRECT FORM
            pos = id_tag.split('-')
            x = int(pos[0])
            y = int(pos[1])
            if len(pos) > 2 : raise ValueError
        except:
            raise TypeError('ID should be in the form int-int')
        if not isinstance(prev_node, Node) and prev_node != None:
            raise TypeError('Previous node should be of type Node')
        if not isinstance(end, Node) and end != None:
            raise TypeError('End node should be of type Node')
        try:                                                                    #CHECK NBR IDS IN CORRECT FORM
            for nbr in nbrs:
                pos = id_tag.split('-')
                x = int(pos[0])
                y = int(pos[1])
                if len(pos) > 2 : raise ValueError
        except:
            raise TypeError('Neighbour ID should be in the form int-int')

        self.id = id_tag
        self.prev = prev_node
        self.cost = self.g(self.prev)                                           #CALCULATE STARTING COST + HEURISTIC
        self.heuristic = self.h(end)
        self.nbrs = nbrs
        self.queue_index = 0
        self.visited = False

    def get_id(self):                                                           #RETURNS NODE'S ID
        return self.id

    def get_x(self):                                                            #RETURNS NODE'S X-POS
        return int(self.id.split('-')[0])

    def get_y(self):                                                            #RETURNS NODE'S Y-POS
        return int(self.id.split('-')[1])

    def get_pos(self):                                                          #RETURNS COMBINED X-POS AND Y-POS
        return [self.get_x(), self.get_y()]

    def get_prev(self):                                                         #RETURNS NODE USED TO EXPLORE CURRENT
        return self.prev

    def get_cost(self):                                                         #RETURNS NODE'S COST
        return self.cost

    def get_nbrs(self):                                                         #RETURNS NODE'S NEIGHBOURS
        return self.nbrs

    def get_visited(self):                                                      #RETURNS IF NODE HAS BEEN VISITED
        return self.visited

    def set_prev(self, value):                                                  #CHECK THAT PREVIOUS IS A NODE
        if not isinstance(value, Node) : raise TypeError('Previous node must be of type Node')
        self.prev = value

    def set_visited(self):                                                      #SET VISITED TO TRUE
        self.visited = True
    
    def update_cost(self, prev):                                                #UPDATE COST OF NODE WITH NEW NODE
        new_cost = self.g(prev)
        if new_cost < self.cost:                                                #BETTER ROUTE FOUND TO NODE
            self.cost = new_cost
            self.prev = prev

    def g(self, node):                                                          #RETURNS COST OF PREV PLUS EDGE WEIGHT
        if node == None : return 0
        return node.get_cost() + abs(self.get_x() - node.get_x()) + abs(self.get_y() - node.get_y())
        
    def h(self, end):                                                           #RETURNS MANHATTAN DISTANCE BETWEEN NODE + END
        if end == None : return 0
        return abs(self.get_x() - end.get_x()) + abs(self.get_y() - end.get_y())
        
    def score(self):                                                            #RETURNS COMBINED COST AND HEURISTIC
        return self.cost + self.heuristic


def shortest_path(adj_list, start_pos, end_pos):                                #RETURNS SHORTEST PATH BETWEEN TWO POINTS
    nodes = structures.Hash_Table(adj_list.length())                            #LOOK-UP OF NODE OBJECTS BY ID
    queue = structures.Heap()                                                   #QUEUE OF NODES TO BE EXPLORED
    
    start_id = str(start_pos[0]) + '-' + str(start_pos[1])                      #CREATE START/END NODES
    start_nbrs = adj_list[start_id]
    start = Node(start_id, None, None, start_nbrs)
    end_id = str(end_pos[0]) + '-' + str(end_pos[1])
    end_nbrs = adj_list[end_id]
    end = Node(end_id, None, None, end_nbrs)

    nodes_visited = 0                                                           #USED IN UPDATE.TXT FILE
    total_nodes = adj_list.length()
    queue.push(start)
    nodes[start.get_id()] = start                                               #NODES ADDED TO LOOK-UP TABLE ONCE CREATED
    
    while queue.length() > 0:                                                   #IF QUEUE EMPTY THERE IS NO ROUTE BETWEEN THEM
        current = queue.pop()
        current.set_visited()
        if current.get_id() == end.get_id():                                    #SHORTEST PATH HAS BEEN FOUND
            path = get_path([], current, start)
            return path

        for nbr_id in current.get_nbrs():                                       #EXPLORE CURRENT NODE'S NBRS
            nbr = nodes[nbr_id]
            if nbr == None:                                                     #NODE NOT CREATED YET
                nbr_nbrs = adj_list[nbr_id]
                nbr = Node(nbr_id, current, end, nbr_nbrs)                      #CREATE AND ADD TO QUEUE
                queue.push(nbr)
                nodes[nbr_id] = nbr
            elif not nbr.get_visited():                                         #NODE CREATED BUT UNVISITED
                nbr.update_cost(current)                                        #UPDATE COST + POS IN QUEUE
                queue.update(nbr.queue_index)
            
        update.set_update(str(nodes_visited) + ' of ' + str(total_nodes) + ' Nodes Visited')
        nodes_visited += 1
    return None


def get_path(path, current, start):                                             #LOOP BACK THROUGH PREV NODES TO START
    while current != start:
        path.append(current.get_pos())                                          #ADD PREVIOUS NODES TO PATH 
        current = current.get_prev()
    path.append(current.get_pos())
    return path
