import math

NODES = []

class Node():
    def __init__(self, pos, nbrs, startPos):
        self.pos = [pos[0],pos[1]]
        self.cost = None
        self.heuristic = math.sqrt((pos[0] - startPos[0])**2 + (pos[1] - startPos[1])**2)
        self.prev = None
        self.nbrs = []
        self.pointer = None
        self.connectNbrs(nbrs)
    def connectNbrs(self, nbrs):
        for i in range(0,len(nbrs)-1,2):
            nbr = getNode(nbrs[i], nbrs[i+1])
            self.nbrs.append(nbr)
            nbr.nbrs.append(self)

def getNode(x, y):
    searchVal = int(str(x) + "{0:0>6}".format(str(y)))
    minPos = 0
    maxPos = len(NODES)-1
    curPos = (minPos + maxPos)//2
    curVal = int(str(NODES[curPos].pos[0]) + "{0:0>6}".format(str(NODES[curPos].pos[1])))
                    
    while curVal != searchVal and curPos != minPos:
        if curVal > searchVal:
            maxPos = curPos
        else:
            minPos = curPos
        curPos = (minPos + maxPos)//2
        curVal = int(str(NODES[curPos].pos[0]) + "{0:0>6}".format(str(NODES[curPos].pos[1])))

    if curVal == searchVal:
        return(NODES[curPos])
    maxVal = int(str(NODES[maxPos].pos[0]) + "{0:0>6}".format(str(NODES[maxPos].pos[1])))
    if maxVal == searchVal:
        return(NODES[maxPos])
    return None

def createNodes(nodeData,startPos):
    for node in nodeData:
        data = list(map(int, node.split(' ')))
        NODES.append(Node(data[0:2], data[2:], startPos))

def addUnvisited(nodes, new):
    searchVal = new.cost + new.heuristic
    minPos = 0
    maxPos = len(nodes)-1
    curPos = (minPos + maxPos)//2
    curVal = nodes[curPos].cost + nodes[curPos].heuristic
                    
    while curVal != searchVal and curPos != minPos:
        if curVal > searchVal:
            maxPos = curPos
        else:
            minPos = curPos
        curPos = (minPos + maxPos)//2
        curVal = nodes[curPos].cost + nodes[curPos].heuristic

    minVal = nodes[minPos].cost + nodes[minPos].heuristic
    maxVal = nodes[maxPos].cost + nodes[maxPos].heuristic
    if curVal == searchVal:
        if nodes[curPos].heuristic < new.heuristic:
            while (nodes[curPos].heuristic < new.heuristic and curVal == searchVal):
                curPos += 1
                curVal = nodes[curPos].cost + nodes[curPos].heuristic
        elif nodes[curPos].heuristic > new.heuristic:
            while (nodes[curPos].heuristic < new.heuristic and curVal == searchVal):
                curPos -= 1
                curVal = nodes[curPos].cost + nodes[curPos].heuristic
            curPos += 1
        finalPos = curPos
    elif searchVal == maxVal:
        curPos = maxPos
        curVal = maxVal
        if nodes[curPos].heuristic < new.heuristic:
            while (nodes[curPos].heuristic < new.heuristic and curVal == searchVal):
                curPos += 1
                curVal = nodes[curPos].cost + nodes[curPos].heuristic
        elif nodes[curPos].heuristic > new.heuristic:
            while (nodes[curPos].heuristic < new.heuristic and curVal == searchVal):
                curPos -= 1
                curVal = nodes[curPos].cost + nodes[curPos].heuristic
            curPos += 1
        finalPos = curPos        
    elif minVal < searchVal < maxVal:
        finalPos = minPos+1
    elif searchVal < minVal:
         finalPos = minPos
    elif searchVal > maxVal:
        finalPos = maxPos+1
    new.pointer = finalPos
    nodes.insert(finalPos, new)
    return nodes

def shortestPath(start, end):
    unvisited = [start]
    current = start

    while current != end:
        current = unvisited[0]
        unvisited.pop(0)
        added = []
        edited = []
        for nbr in current.nbrs:
            weight = abs(current.pos[0] - nbr.pos[0]) + abs(current.pos[1] - nbr.pos[1]) #WEIGHT OF THE EDGE
            if nbr.cost == None: #NO ROUTE TO NEIGHBOUR
                added.append(nbr)
                nbr.cost = current.cost + weight
                nbr.prev = current
            elif current.cost + weight < nbr.cost: #QUICKER ROUTE TO NEIGHBOUR
                edited.append(nbr)
                neighbour.cost = current.cost + weight
                neighbour.prev = current
        for nbr in added:
            if len(unvisited) == 0:
                unvisited.append(nbr)
            else:
                unvisited = addUnvisited(unvisited, nbr)
        for nbr in edited:
            unvisited = unvisited.pop(nbr.pointer)
            if len(unvisited) == 0:
                unvisited.append(nbr)
            else:
                unvisited = addUnvisited(unvisited, nbr)

    path = [end.pos]
    node = end.prev
    while node != None:
        path.append(node.pos)
        node = node.prev
    return path   

def findPath(nodeData):
    global NODES #mebs local
    NODES = []
    startPos = list(map(int, nodeData[0].split(' ')))
    endPos = list(map(int, nodeData[1].split(' ')))
    createNodes(nodeData[2:], startPos)

    startNode = getNode(startPos[0], startPos[1])
    endNode = getNode(endPos[0], endPos[1])
    startNode.cost = 0
    startNode.heuristic = 0
    startNode.pointer = 0

    path = shortestPath(startNode, endNode)
    return path
