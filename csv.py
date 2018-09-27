def open_integer_grid(name):                                                    #RETURNS CSV AS A 2D GRID OF INTEGERS
    file = open(name, 'r')
    csv = file.read()
    file.close()
    csv_rows = csv.split('\n')
    grid = []
    for csv_row in csv_rows:                                                    #LOOP THROUGH FILE ROWS
        grid_row = []
        csv_row = csv_row.split(',')
        for item in csv_row:
            try:
                grid_row.append(int(item))                                      #IGNORE NON-INTEGERS
            except:
                if item == 'NA' : grid_row.append(-1)                           #NA VALUES ARE ADDED AS -1 (USED IN WALLS.CSV)
        if len(grid_row) > 0 : grid.append(grid_row)                            #IGNORE EMPTY ROWS
    return grid


def save_grid(name, grid):                                                      #SAVES 2D GRID AS CSV
    csv_string = ''
    for row in grid:
        csv_string += str(row)[1:-1].replace(' ','') + '\n'                     #REMOVE BRACKETS AND SPACES FROM LIST
    file = open(name, 'w')                                                      #[^CONTINUED^] TO FORMAT THE SAME AS CSV
    file.write(csv_string[:-1])
    file.close()
