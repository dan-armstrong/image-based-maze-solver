Maze maze;
int mode;
PFont menu_font;
color pink = #FF0066;
int help_mode = 1;
float min_scale = 1/pow(1.02,3);
Boolean[] keys_down = {false, false, false, false, false, false};
Boolean loading = false;
Boolean load_finished = false;
Boolean saving = false;
Boolean save_finished = false;
String csv_file;


void setup() {
  size(800,600);
  background(255);
  pixelDensity(displayDensity());
  noStroke();
  menu_font = createFont("Avenir Next",16);
  csv_file = "../maze.csv";

//  int[][] maze_csv = open_csv("../" + args[0]);
  float wall_ratio = 0.5;
//  int wall_ratio = float(args[2]) / float(args[1]);
  maze =  new Maze(wall_ratio, min_scale, pink);
  
  exit_handler();
  refresh_screen();
} 


void draw() {
  if (keys_down[0]) {maze.y_pan += 5;}
  if (keys_down[1]) {maze.y_pan -= 5;}
  if (keys_down[2]) {maze.x_pan += 5;}
  if (keys_down[3]) {maze.x_pan -= 5;}
  if (keys_down[4]) {
    maze.scale *= 1.02;
    maze.x_pan = width*0.5 - (width*0.5 - maze.x_pan)*1.02;
    maze.y_pan = height*0.5 - (height*0.5 - maze.y_pan)*1.02;
  }
  if (keys_down[5] && maze.scale > min_scale) {
    maze.scale = maze.scale/1.02;
    maze.x_pan = width*0.5 - (width*0.5 - maze.x_pan)/1.02;
    maze.y_pan = height*0.5 - (height*0.5 - maze.y_pan)/1.02;
  }
  if (key_down()) {
    refresh_screen();
  }
}


void keyPressed() {
  if (keyCode == UP) {keys_down[0] = true;}
  if (keyCode == DOWN) {keys_down[1] = true;}
  if (keyCode == LEFT) {keys_down[2] = true;}
  if (keyCode == RIGHT) {keys_down[3] = true;}
  if (key == 'z' || key == 'Z') {keys_down[4] = true;}
  if (key == 'x' || key == 'X') {keys_down[5] = true;}
  if (key == 'h' || key == 'H') {help_mode = (help_mode + 1) % 3;}
  if (key == 'r' || key == 'R') {
    if (mode == 0 ) {
      maze.grid = open_csv("../maze.csv");
    }
    else {
        maze.end_points[0] = -1;
        maze.end_points[1] = -1;
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
    }
  }
  if (key == 's' || key == 'S') {
    if (mode == 0) {
      help_mode = 0;
      refresh_screen();
      rectMode(CENTER);
      fill(pink, 210);
      rect(width*0.5, height*0.5, width*0.6, 125, 7);
      textFont(menu_font, 20);
      textAlign(CENTER, CENTER);
      fill(255);
      text("SAVING MAZE", width*0.5, height*0.5 - 3);
      save_csv(maze.grid, "../maze.csv");
      //stop();
    }
  }
  refresh_screen();
}


void keyReleased() {
  if (keyCode == UP) {keys_down[0] = false;}
  if (keyCode == DOWN) {keys_down[1] = false;}
  if (keyCode == LEFT) {keys_down[2] = false;}
  if (keyCode == RIGHT) {keys_down[3] = false;}
  if (key == 'z' || key == 'Z') {keys_down[4] = false;}
  if (key == 'x' || key == 'X') {keys_down[5] = false;}
}


void mousePressed() {
  int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
  int x = selected[0];
  int y = selected[1];
  maze.prev_selected = selected;

  if (x != -1 && y != -1) {
    if (mode == 0) {
      if (maze.grid[y][x] == 0) {
        maze.grid[y][x] = 1;
      }
      else if (maze.grid[y][x] == 1) {
        maze.grid[y][x] = 0;
      }
    }

    if (mode == 1) {
      if (x == maze.end_points[0] && y == maze.end_points[1]) {
        maze.end_points[0] = maze.end_points[2];
        maze.end_points[1] = maze.end_points[3];
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
      }
      else if (x == maze.end_points[2] && y == maze.end_points[3]) {
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
      }
      else if (maze.grid[y][x] == 0) {
        if (maze.end_points[2] != -1 && maze.end_points[3] != -1) {
          maze.end_points[0] = maze.end_points[2];
          maze.end_points[1] = maze.end_points[3];
        }
        maze.end_points[2] = x;
        maze.end_points[3] = y;
      }
    }
  }
  refresh_screen();
}


void mouseDragged() {
  if (mode == 0) {
    int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
    int x = selected[0];
    int y = selected[1];
    if (x != -1 && y != -1 && (x != maze.prev_selected[0] || y != maze.prev_selected[1])) {
      if (maze.grid[y][x] == 0) {
        maze.grid[y][x] = 1;
      }
      else if (maze.grid[y][x] == 1) {
        maze.grid[y][x] = 0;
      }
    }
    maze.prev_selected = selected;

  }
  refresh_screen();
}


void mouseReleased() {
  maze.prev_selected[0] = -1;
  maze.prev_selected[1] = -1;
}


void refresh_screen() {
  background(255);
  maze.display();
  display_menu();
}


void display_menu() {
  if (help_mode != 0) {
    rectMode(CENTER);
    fill(pink, 210);
    rect(width*0.5, height*0.5, width*0.6, 125, 7);
    textFont(menu_font, 20);
    textAlign(CENTER, CENTER);
    fill(255);
  }
  if (help_mode == 1) {
    if (mode == 0) {
      textFont(menu_font, 40);
      text("EDITING MODE", width*0.5, height*0.5 - 40);
      textFont(menu_font, 20);
      text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
      text("PRESS [R] TO RESET MAZE", width*0.5, height*0.5 + 21);
      text("PRESS [Q] TO SAVE AND MOVE ON", width*0.5, height*0.5 + 45);
    }
    else {
      textFont(menu_font, 40);
      text("SELECTING MODE", width*0.5, height*0.5 - 40);
      textFont(menu_font, 20);
      text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
      text("PRESS [R] TO RESET END POINTS", width*0.5, height*0.5 + 21);
      text("PRESS [Q] TO SOLVE MAZE BETWEEN END POINTS", width*0.5, height*0.5 + 45);
    }
  }
  else if (help_mode == 2) {
    if (mode == 0) {
      text("CLICK ON WALLS TO CHANGE TO PATH", width*0.5, height*0.5 - 51);
      text("CLICK ON PATHS TO CHANGE TO WALL", width*0.5, height*0.5 - 27);
      text("USE [W A S D Z X] TO ZOOM AND PAN", width*0.5, height*0.5 - 3);
      text("PRESS [CTRL+Z / CTRL+Y] TO UNDO/REDO", width*0.5, height*0.5 + 21);
      text("MAZE WILL NOT SAVE IF PROGRAM CLOSED", width*0.5, height*0.5 + 45);
    }
    else {
      text("CLICK TO SELECT AN END POINT", width*0.5, height*0.5 - 51);
      text("CLICK ON AN END POINT TO REMOVE IT", width*0.5, height*0.5 - 27);
      text("END POINTS MUST BE ON THE PATH", width*0.5, height*0.5 - 3);
      text("END POINTS DISPLAYED IN PINK", width*0.5, height*0.5 + 21);
      text("POINTS WILL NOT SAVE IF PROGRAM CLOSED", width*0.5, height*0.5 + 45);
    }
  }
}


int[][] open_csv(String file_name) {
  String[] rows = loadStrings(file_name);
  int csv_width = split(rows[0], ",").length;
  int csv_height = rows.length;
  int[][] csv = new int[csv_height][csv_width];
  for (int y = 0; y < rows.length; y++) {
    String[] row = split(rows[y], ",");
    for (int x = 0; x < row.length; x++) {
      csv[y][x] = int(row[x]);
    }
  }
  return csv;
}


void save_csv(int[][] maze, String file_name) {
  String csv = "";
  for (int y = 0; y < maze.length; y++) {
    if (y != 0) {csv += "\n";}
    for (int x = 0; x < maze[y].length; x++) {
      if (x != 0) {csv += ",";}
      csv += str(maze[y][x]);
    }
  }
  PrintWriter file = createWriter(file_name);
  file.print(csv);
  file.flush();
  file.close();  
}


Boolean key_down() {
  for (Boolean k : keys_down) {
    if (k) {return true;}
  }
  return false;
}


void open_csv() {
  if (!loading && !saving) {
    loading = true;
    int[][] copy;
    String[] rows = loadStrings(csv_file);
    int num_col = split(rows[0], ",").length;
    int num_row = rows.length;
    copy = new int[num_row][num_col];
    for (int y = 0; y < num_row; y++) {
      String[] row = split(rows[y], ",");
      for (int x = 0; x < num_col; x++) {
        copy[y][x] = int(row[x]);
      }
    }
    maze.grid = copy;
    maze.maze_width = maze.grid[0].length/2 + maze.wall_ratio;
    maze.maze_height = maze.grid.length/2 + maze.wall_ratio;
    maze.cell_size = min(width/(maze.maze_width), height/maze.maze_height);
    loading = false;
    load_finished = true;
  }
}



void exit_handler() {
  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
    public void run () {
      println(maze.end_points[0], maze.end_points[1], maze.end_points[2], maze.end_points[3]);
    }
  }));
}