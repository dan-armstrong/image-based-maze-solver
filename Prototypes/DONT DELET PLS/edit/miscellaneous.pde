void open_csv() {
  if (!loading && !saving) {
    loading = true;
    int[][] maze_copy;
    String[] rows = loadStrings(csv_file);
    int num_col = split(rows[0], ",").length;
    int num_row = rows.length;
    maze_copy = new int[num_row][num_col];
    for (int y = 0; y < num_row; y++) {
      String[] row = split(rows[y], ",");
      for (int x = 0; x < num_col; x++) {
        maze_copy[y][x] = int(row[x]);
      }
    }
    maze = maze_copy;
    maze_width = maze[0].length/2 + wall_ratio;
    maze_height = maze.length/2 + wall_ratio;
    cell_size = min(width/(maze_width), height/maze_height);
    loading = false;
    load_finished = true;
  }
}


void save_csv() {
  if (!loading && !saving) {
    saving = true;
    String csv = "";
    int[][] maze_copy = maze;
    for (int y = 0; y < maze_copy.length; y++) {
      if (y != 0) {csv += "\n";}
      for (int x = 0; x < maze_copy[y].length; x++) {
        if (x != 0) {csv += ",";}
        csv += str(maze_copy[y][x]);
      }
    }
    PrintWriter file = createWriter(csv_file);
    file.print(csv);
    file.flush();
    file.close();  
    saving = false;
    save_finished = true;
  }
}


float[] dimensions(int x, int y) {
  float x_pos, x_size, y_pos, y_size;
  if (x % 2 == 0) {
    x_pos = x/2 * cell_size;
    x_size = wall_ratio * cell_size;
  }
  else {
    x_pos = (x/2 + wall_ratio) * cell_size;
    x_size = (1-wall_ratio) * cell_size;
  }
  if (y % 2 == 0) {
    y_pos =  y/2 * cell_size;
    y_size = wall_ratio * cell_size;
  }
  else {
    y_pos = (y/2 + wall_ratio) * cell_size;
    y_size = (1-wall_ratio) * cell_size;
  }
  return new float[] {x_pos, y_pos, x_size, y_size};
}


int[] maze_index(float x, float y){
  float cell_x = x / cell_size;
  float cell_y = y / cell_size;
  int index_x, index_y;
  index_x = 2*floor(cell_x);
  index_y = 2*floor(cell_y);
  if (index_x < 0 || index_x >= maze[0].length) {index_x = -1;}
  else if (cell_x > floor(cell_x) + wall_ratio) {index_x += 1;}
  if (index_y < 0 || index_y >= maze.length) {index_y = -1;}
  else if (cell_y > floor(cell_y) + wall_ratio) {index_y += 1;}
  return new int[] {index_x, index_y};
}


Boolean key_down() {
  for (Boolean key_pressed : keys_down) {
    if (key_pressed) {return true;}
  }
  return false;
}


int[] find_points() {
  int[] points = {-1, -1, -1, -1};
  for (int x = 0; x < maze[0].length; x++) {
    if (maze[0][x] == 0) {
      if (points[0] == -1 || points[1] == -1) {
        points[0] = x;
        points[1] = 0;
      }
      else {
        points[2] = x;
        points[3] = 0;
        return points;
      }
    }
  }

  for (int x = 0; x < maze[maze.length-1].length; x++) {
    if (maze[maze.length-1][x] == 0) {
      if (points[0] == -1 || points[1] == -1) {
        points[0] = x;
        points[1] = maze.length-1;
      }
      else {
        points[2] = x;
        points[3] = maze.length-1;
        return points;
      }
    }
  }

  for (int y = 0; y < maze.length; y++) {
    if (maze[y][0] == 0) {
      if (points[0] == -1 || points[1] == -1) {
        points[0] = 0;
        points[1] = y;
      }
      else {
        points[2] = 0;
        points[3] = y;
        return points;
      }
    }
  }

  for (int y = 0; y < maze.length; y++) {
    if (maze[y][maze[y].length-1] == 0) {
      if (points[0] == -1 || points[1] == -1) {
        points[0] = maze[y].length-1;
        points[1] = y;
      }
      else {
        points[2] = maze[y].length-1;
        points[3] = y;
        return points;
      }
    }
  }
  
  return points;
}