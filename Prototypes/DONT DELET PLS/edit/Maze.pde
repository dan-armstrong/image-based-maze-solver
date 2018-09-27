public class Maze {
  int[][] grid = {{0}};
  int[] end_points = {-1, -1, -1, -1};
  int[] prev_selected = {-1, -1};
  float wall_ratio, maze_width, maze_height, cell_size, scale;
  float x_pan  = 0.0;
  float y_pan = 0.0;
  String csv_name;
  boolean loading = false;
  boolean load_finished = false;
  boolean saving = false;
  boolean save_finished = false;
  color point_colour;
  
  
  Maze(float ratio, float maze_scale, color col) {
    thread("open_csv");
    wall_ratio = ratio;
    maze_width = grid[0].length/2 + wall_ratio;
    maze_height = grid.length/2 + wall_ratio;
    cell_size = min(width/(maze_width), height/maze_height);
    scale = maze_scale;
    point_colour = col;
  }
  
  
  void display() {
    center();
    int x_min = max(0, floor((-x_pan/scale)/cell_size)*2);
    int x_max = min(grid[0].length, ceil(((width-x_pan)/scale)/cell_size)*2);
    int y_min = max(0, floor((-y_pan/scale)/cell_size)*2);
    int y_max = min(grid.length, ceil(((height-y_pan)/scale)/cell_size)*2);
    
    rectMode(CORNER);
    pushMatrix();
    scale(scale);
    translate(x_pan/scale, y_pan/scale);

    for (int y = y_min; y < y_max; y++) {
      for (int x = x_min; x < x_max; x++) {
        float[] dims = dimensions(x, y);
        if ((x == end_points[0] && y == end_points[1]) || (x == end_points[2] && y == end_points[3])) {
          fill(point_colour);
          rect(dims[0], dims[1], dims[2], dims[3]);
        }
        else if (grid[y][x] == 1) {
          fill(0);
          rect(dims[0], dims[1], dims[2], dims[3]);
        }
      }
    }
    popMatrix();
  }
 
 
  void center() {
    if (maze_width*cell_size*scale < width) {
      x_pan = (width - maze_width*cell_size*scale) / 2;
    }
    else if (x_pan > 0) {
      x_pan = 0.0;
    }
    else if (x_pan + maze_width*cell_size*scale < width) {
      x_pan = width - maze_width*cell_size*scale;
    }

    if (maze_height*cell_size*scale < height) {
      y_pan = (height - maze_height*cell_size*scale) / 2;
    }
    else if (y_pan > 0) {
      y_pan = 0.0;
    }
    if (y_pan + maze_height*cell_size*scale < height) {
      y_pan = height - maze_height*cell_size*scale;
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
    return new float[] {x_pos, y_pos, x_size, y_size}; // talk to yannis
  }


  int[] index(float x, float y){
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
  
  
  void open_csv() {
    if (!loading && !saving) {
      loading = true;
      int[][] copy;
      String[] rows = loadStrings(csv_name);
      int num_col = split(rows[0], ",").length;
      int num_row = rows.length;
      copy = new int[num_row][num_col];
      for (int y = 0; y < num_row; y++) {
        String[] row = split(rows[y], ",");
        for (int x = 0; x < num_col; x++) {
          copy[y][x] = int(row[x]);
        }
      }
      grid = copy;
      maze_width = grid[0].length/2 + wall_ratio;
      maze_height = grid.length/2 + wall_ratio;
      cell_size = min(width/(maze_width), height/maze_height);
      loading = false;
      load_finished = true;
    }
  }
  
  
  void save_csv() {
    if (!loading && !saving) {
      saving = true;
      String csv = "";
      int[][] copy = grid;
      for (int y = 0; y < copy.length; y++) {
        if (y != 0) {csv += "\n";}
        for (int x = 0; x < copy[y].length; x++) {
          if (x != 0) {csv += ",";}
          csv += str(copy[y][x]);
        }
      }
      PrintWriter file = createWriter(csv_name);
      file.print(csv);
      file.flush();
      file.close();  
      saving = false;
      save_finished = true;
    }
  }

  
  void find_points() {
    int[] points = {-1, -1, -1, -1};
    for (int y : new int[] {0, grid.length-1}) {
      if (points[2] != -1 && points[3] != -1) {break;}
      for (int x = 0; x < grid[y].length; x++) {
        if (grid[y][x] == 0) {
          if (points[0] == -1 || points[1] == -1) {
            points[0] = x;
            points[1] = y;
          }
          else {
            points[2] = x;
            points[3] = y;
            end_points = points;
            break;
          }
        }
      }
    }
    
    for (int x : new int[] {0, grid[0].length-1}) {
      if (points[2] != -1 && points[3] != -1) {break;}
      for (int y = 0; y < grid.length; y++) {
        if (grid[y][x] == 0) {
          if (points[0] == -1 || points[1] == -1) {
            points[0] = x;
            points[1] = y;
          }
          else {
            points[2] = x;
            points[3] = y;
            end_points = points;
            break;
          }
        }
      }
    }
    end_points = points;
  }
}