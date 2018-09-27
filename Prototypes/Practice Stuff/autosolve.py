def auto_end_points(grid):                                                      #RETURN COORDINATES OF END POINTS
    start_point = None
    end_point = None
    found = False
    for x in range(len(grid[0])):                                               #LOOP THROUGH TOP ROW
        if found : break
        if grid[0][x] == 0:
            if start_point == None:
                start_point = [x, 0]
            else:
                end_point = [x, 0]
                found = True
    for x in range(len(grid[len(grid)-1])):                                     #LOOP THROUGH BOTTOM ROW
        if found : break
        if grid[len(grid)-1][x] == 0:
            if start_point == None:
                start_point = [x, len(grid)-1]
            else:
                end_point = [x, len(grid)-1]
                found = True
    for y in range(1, len(grid)-1):                                             #LOOP THROUGH LEFT COL
        if found : break
        if grid[y][0] == 0:
            if start_point == None:
                start_point = [0, y]
            else:
                end_point = [0, y]
                found = True
    for y in range(1, len(grid)-1):                                             #LOOP THROUGH RIGHT COL
        if found : break
        if grid[y][len(grid[0])-1] == 0:
            if start_point == None:
                start_point = [len(grid[0])-1, y]
            else:
                end_point = [len(grid[0])-1, y]
                found = True
    if end_point == None:
        return None
    return [start_point, end_point]

grid = [[0,1,1,1,1],                                                               #TEST GRID
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,0]]

print(auto_end_points(grid))                       
