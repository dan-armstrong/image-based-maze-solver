public class Maze {                                                             //MAZE CLASS - STORES MAZE ARRAY + DISPLAYS IT
  int[][] grid;                     
  int[] end_points = {-1, -1, -1, -1};
  int[] prev_selected = {-1, -1};
  float wall_ratio, maze_width, maze_height, cell_size, scale;
  float x_pan = 0.0;                                                            //TOP-LEFT MAZE IMAGE HANDLE
  float y_pan = 0.0;
  String csv_name;
  color point_colour;
  
  
  Maze(String maze_file, float maze_ratio, float maze_scale, color maze_colour) {
    csv_name = maze_file;
    open_csv();                                                                 //LOAD CSV FILE
    wall_ratio = maze_ratio;
    maze_width = (grid[0].length-1)/2.0 + wall_ratio;
    maze_height = (grid.length-1)/2.0 + wall_ratio;
    cell_size = min(width/maze_width, height/maze_height);                      //SIZE OF EACH MAZE CELL
    scale = maze_scale;
    move(0,0);                                                                  //CENTER IMAGE 
    point_colour = maze_colour;
  }
  
  
  void display() {                                                              //DRAWS MAZE TO CANVAS
    int x_min = max(0, floor((-x_pan/scale)/cell_size)*2);                      //GET MINIMUM INDEXES NEEDED TO DISPLAY
    int x_max = min(grid[0].length, ceil(((width-x_pan)/scale)/cell_size)*2);   //DON'T DRAW MAZE SECTIONS OUTSIDE WINDOW
    int y_min = max(0, floor((-y_pan/scale)/cell_size)*2);
    int y_max = min(grid.length, ceil(((height-y_pan)/scale)/cell_size)*2);
    
    rectMode(CORNER);
    pushMatrix();
    scale(scale);                                                               //MOVE/SCALE CANVAS
    translate(x_pan/scale, y_pan/scale);
    for (int y = y_min; y < y_max; y++) {
      for (int x = x_min; x < x_max; x++) {
        float[] dims = dimensions(x, y);                                        //GET CELL DIMENSIONS
        if ((x == end_points[0] && y == end_points[1]) || (x == end_points[2] && y == end_points[3])) {
          fill(point_colour);
          rect(dims[0], dims[1], dims[2], dims[3]);                             //DRAW IF POINT
        }
        else if (grid[y][x] == 1) {
          fill(0);
          rect(dims[0], dims[1], dims[2], dims[3]);                             //DRAW IF WALL
        }
      }
    }
    popMatrix();                                                                //RESET CANVAS TRANSFORMATIONS
  }
 
  
  void move(float x, float y) {                                                 //MOVES MAZE HANDLE TO SPECIFIED POS
    if (maze_width*cell_size*scale < width) {                                   //MAZE WIDTH SMALLER THAN CANVAS WIDTH
      x_pan = (width - maze_width*cell_size*scale) / 2.0;                       //CENTER IN THE MIDDLE OF THE CANVAS
    }
    else if (x > 0) {                                                           //MAZE DRAGGED TOO FAR RIGHT
      x_pan = 0.0;
    }
    else if (x + maze_width*cell_size*scale < width) {                          //MAZE DRAGGED TOO FAR LEFT
      x_pan = width - maze_width*cell_size*scale;
    }
    else {
      x_pan = x;
    }

    if (maze_height*cell_size*scale < height) {                                 //MAZE HEIGHT SMALLER THAN CANVAS HEIGHT
      y_pan = (height - maze_height*cell_size*scale) / 2.0;                     //CENTER IN THE MIDDLE OF THE CANVAS
    }
    else if (y > 0) {                                                           //MAZE DRAGGED TOO FAR DOWN
      y_pan = 0.0;
    }
    else if (y + maze_height*cell_size*scale < height) {                        //MAZE DRAGGED TOO FAR UP
      y_pan = height - maze_height*cell_size*scale;
    }
    else {
      y_pan = y;
    }
  }

  
  float[] dimensions(int x, int y) {                                            //RETURNS DIMENSIONS OF DRAWING FROM INDEX
    float x_pos, x_size, y_pos, y_size;
    if (x % 2 == 0) {                                                           //PATH SECTION
      x_pos = x/2 * cell_size;
      x_size = wall_ratio * cell_size;
    }
    else {                                                                      //WALL SECTION
      x_pos = (x/2 + wall_ratio) * cell_size;
      x_size = (1-wall_ratio) * cell_size;
    }
    if (y % 2 == 0) {                                                           //PATH SECTION
      y_pos =  y/2 * cell_size;
      y_size = wall_ratio * cell_size;
    }
    else {                                                                      //WALL SECTION
      y_pos = (y/2 + wall_ratio) * cell_size;
      y_size = (1-wall_ratio) * cell_size;
    }
    return new float[] {x_pos, y_pos, x_size, y_size};                          //INFORMATION NEEDED TO DRAW RECT
  }


  int[] index(float x, float y){                                                //RETURNS INDEX OF MAZE CELL AT CANVAS POS
    float cell_x = x / cell_size;                                               //RELATIVE CELL POS
    float cell_y = y / cell_size;
    int index_x, index_y;
    index_x = 2*floor(cell_x);                                                  //RELATIVE INDEX
    index_y = 2*floor(cell_y);

    if (cell_x > floor(cell_x) + wall_ratio) {index_x += 1;}                    //IF FURTHER OVER THAN WALL SECTION
    if (index_x < 0 || index_x >= grid[0].length) {index_x = -1;}               //NOT IN CORRECT RANGE
    if (cell_y > floor(cell_y) + wall_ratio) {index_y += 1;}
    if (index_y < 0 || index_y >= grid.length) {index_y = -1;}
    return new int[] {index_x, index_y};
  }

  
  void open_csv() {                                                             //READS MAZE GRID FILE AND LOADS IT IN
    String[] rows = loadStrings(csv_name);
    int num_col = split(rows[0], ",").length;
    int num_row = rows.length;
    grid = new int[num_row][num_col];
    for (int y = 0; y < num_row; y++) {
      String[] row = split(rows[y], ",");
      for (int x = 0; x < num_col; x++) {
        grid[y][x] = int(row[x]);
      }
    }
  }


  void save_csv() {                                                               //SAVES CURRENT MAZE GRID TO FILE
    PrintWriter file = createWriter(maze.csv_name);
    for (int y = 0; y < grid.length; y++) {
      if (y != 0) {file.print("\n");}
      for (int x = 0; x < grid[y].length; x++) {
        if (x != 0) {file.print(",");}
        file.print(str(grid[y][x]));                                              //SAVE EACH CELL
      }
    }
    file.flush();
    file.close();  
  }
}


public class Menu {                                                               //CLASS FOR HEADS-UP DISPLAY
  int mode;
  PFont font;
  color background_colour; 
  
  Menu(int menu_mode, PFont menu_font, color menu_colour) {                       //CONSTRUCTOR
    mode = menu_mode;
    font = menu_font;
    background_colour = menu_colour;
  }
  
  
  void display() {                                                                //DRAW MENU
    if (mode != 0) {                                                              //MODE 0 = OFF
      rectMode(CENTER);
      fill(background_colour, 210);
      rect(width*0.5, height*0.5, width*0.6, 125, 7);                             //TRANSLUCENT PINK RECTANGLE
      textAlign(CENTER, CENTER);
      fill(255);
    }
    if (mode == 1) {                                                              //MODE 1 = FIRST PAGE OF INFO
      if (STATE == 0) {                                                           //STATE 0 = USER IS DRAWING NEW MAZE
        textFont(font, 40);
        text("DRAWING MODE", width*0.5, height*0.5 - 40);
        textFont(font, 20);
        text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
        text("PRESS [R] TO RESET MAZE TO BLANK CANVAS", width*0.5, height*0.5 + 21);
        text("PRESS [S] TO SAVE DRAWING AND RETURN", width*0.5, height*0.5 + 45);
      }
      else if (STATE == 1) {                                                      //STATE 1 = USER IS EDITING MAZE
        textFont(font, 40);
        text("EDITING MODE", width*0.5, height*0.5 - 40);
        textFont(font, 20);
        text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
        text("PRESS [R] TO RESET MAZE", width*0.5, height*0.5 + 21);
        text("PRESS [S] TO SAVE EDITS AND RETURN", width*0.5, height*0.5 + 45);
      }
      else {                                                                      //STATE 2 = USER IS SELECTING POINTS
        textFont(font, 40);
        text("SELECTING MODE", width*0.5, height*0.5 - 40);
        textFont(font, 20);
        text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
        text("PRESS [R] TO RESET END POINTS", width*0.5, height*0.5 + 21);
        text("PRESS [S] TO SAVE POINTS AND RETURN", width*0.5, height*0.5 + 45);
      }
    }
    else if (mode == 2) {                                                         //MODE 2 = SECOND PAGE OF INFO
      if (STATE == 0 || STATE == 1) {
        textFont(font, 20);
        text("CLICK ON WALLS TO CHANGE TO PATH", width*0.5, height*0.5 - 51);
        text("CLICK ON PATHS TO CHANGE TO WALL", width*0.5, height*0.5 - 27);
        text("USE ARROWS AND [Z X] TO ZOOM AND PAN", width*0.5, height*0.5 - 3);
        text("PRESS [CTRL/CMD + Z/Y] TO UNDO/REDO", width*0.5, height*0.5 + 21);
        text("RESET CANNOT BE UNDONE", width*0.5, height*0.5 + 45);
      }
      else {
        textFont(font, 20);
        text("CLICK TO SELECT AN END POINT", width*0.5, height*0.5 - 51);
        text("CLICK ON AN END POINT TO REMOVE IT", width*0.5, height*0.5 - 27);
        text("END POINTS MUST BE ON THE PATH", width*0.5, height*0.5 - 3);
        text("END POINTS DISPLAYED IN PINK", width*0.5, height*0.5 + 21);
        text("ONCE POINTS SELECTED, PRESS Q TO CONTINUE", width*0.5, height*0.5 + 45); 
      }
    }
  }
  
  
  void change_mode() {                                                            //INCREMENT MODE BY 1
    mode = (mode + 1) % 3;
  }
}