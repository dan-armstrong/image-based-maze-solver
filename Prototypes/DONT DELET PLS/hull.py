import math

import structures
import update
import csv


class Point():
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = 0


def merge(list_a, list_b):
    pointer_a = 0
    pointer_b = 0
    merged = []

    while (pointer_a < len(list_a)) & (pointer_b < len(list_b)):
        if list_a[pointer_a].angle == list_b[pointer_b].angle:
            if list_a[pointer_a].y == list_b[pointer_b].y:
                if list_a[pointer_a].x > list_b[pointer_b].x:
                    merged.append(list_a[pointer_a])
                else:
                    merged.append(list_b[pointer_b])
            elif list_a[pointer_a].y > list_b[pointer_b].y:
                merged.append(list_a[pointer_a])
            else:
                merged.append(list_b[pointer_b])
            pointer_a += 1
            pointer_b += 1

        elif list_a[pointer_a].angle > list_b[pointer_b].angle:
            merged.append(list_a[pointer_a])
            pointer_a += 1
        else:
            merged.append(list_b[pointer_b])
            pointer_b += 1

    if pointer_a < len(list_a):
        merged += list_a[pointer_a:]
    elif pointer_b < len(list_b):
        merged += list_b[pointer_b:]
    return merged


def sort(main_list):
    list_a = main_list[:len(main_list)//2]
    list_b = main_list[len(main_list)//2:]
    if len(list_a) > 1:
        list_a = sort(list_a)
    if len(list_b) > 1:
        list_b = sort(list_b)
    return merge(list_a, list_b)


def orientation(a, b, c):
    value = (c.x - b.x)*(a.y - b.y) - (b.x - a.x)*(b.y - c.y) #top corner is origin
    if value < 0 : return -1
    if value > 0 : return 1
    return 0


def convex_hull(positions):
    points = []
    start_index = 0
    for pos in positions:
        points.append(Point(pos))
        if points[-1].y == points[start_index].y and points[-1].x < points[start_index].x:
            start_index = len(points) - 1
        elif points[-1].y < points[start_index].y:
            start_index = len(points) - 1
    start = points[start_index]
    del points[start_index]
    
    for point in points:
        point.angle = (start.x-point.x) / math.sqrt((start.x-point.x)**2 + (start.y-point.y)**2)
    points = sort(points)
    if len(points) < 3 : return points

    stack = structures.Stack()
    stack.push(start)
    stack.push(points[0])
    stack.push(points[1])
    del points[0:2]

    for point in points:
        while orientation(stack.get(1), stack.get(0), point) != -1:
            stack.pop()
        stack.push(point)

    hull = []
    while stack.length() > 0:
        point = stack.pop()
        hull.append([point.x-1, point.y-1])
    hull.reverse()
    return hull


def mask_hull(file_name, hull):
    grid = csv.open_integer_grid(file_name)
    ranges = []
    if len(hull) > 2:
        for row in range(len(grid)):
            pointers = []
            for a in range(len(hull)):
                b = (a+1)%len(hull)
                if hull[a][1] == row : pointers.append(a)
                if min(hull[a][1], hull[b][1]) < row < max(hull[a][1], hull[b][1]):
                    pointers.append(a)

            if len(pointers) > 0:
                if len(pointers) == 1 : pointers.append(pointers[0])
                p1_a = hull[pointers[0]]
                p2_a = hull[(pointers[0]+1)%len(hull)]
                p1_b = hull[pointers[1]]
                p2_b = hull[(pointers[1]+1)%len(hull)]

                if p1_a[0] == p2_a[0]:
                    x_a = p1_a[0]
                else:
                    m_a = (p1_a[1] - p2_a[1])/(p1_a[0] - p2_a[0])
                    if m_a == 0 : x_a = p1_a[0]
                    else : x_a = math.ceil((row - p1_a[1])/m_a + p1_a[0])
                if p1_b[0] == p2_b[0]:
                    x_b = p1_b[0]
                else:               
                    m_b = (p1_b[1] - p2_b[1])/(p1_b[0] - p2_b[0])
                    if m_b == 0 : x_b = p2_b[0]
                    else : x_b = math.floor((row - p1_b[1])/m_b + p1_b[0])
                
                ranges.append([max(0,x_a-1), min(x_b+1,len(grid[0])-1)])
            else:
                ranges.append([])
        print(ranges)
        

            
