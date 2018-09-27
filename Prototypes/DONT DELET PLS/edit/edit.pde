int[][] maze = {{0}};
int[] prev_selected = {-1,-1};
int[] end_points = {-1,-1,-1,-1};
Boolean[] keys_down = {false, false, false, false, false, false};
int mode;
int help_mode = 1;
float maze_width, maze_height, cell_size, wall_ratio;
float min_scale = 1/pow(1.02,3);
float scale = min_scale;
float x_pan, y_pan = 0.0;
Boolean loading = false;
Boolean load_finished = false;
Boolean saving = false;
Boolean save_finished = false;
String csv_file;
PFont menu_font;
color pink = #FF0066;


void setup() {
  size(800,600);
  background(255);
  pixelDensity(displayDensity());
  noStroke();
//  csv_file = "../" + args[0];
  csv_file = "../maze.csv";
  thread("open_csv");
  wall_ratio = 0.5;
  mode = 0;
//  mode = int(args[1]);
//  wall_ratio = float(args[3]) / float(args[2]);
  maze_width = maze[0].length/2 + wall_ratio;
  maze_height = maze.length/2 + wall_ratio;
  cell_size = min(width/(maze_width), height/maze_height);
  menu_font = createFont("Avenir Next",16);
  
  exit_handler();
  refresh_screen();
} 


void draw() {
  if (keys_down[0]) {y_pan += 5;}
  if (keys_down[1]) {y_pan -= 5;}
  if (keys_down[2]) {x_pan += 5;}
  if (keys_down[3]) {x_pan -= 5;}

  if (keys_down[4]) {
    scale *= 1.02;
    x_pan = width*0.5 - (width*0.5 - x_pan)*1.02;
    y_pan = height*0.5 - (height*0.5 - y_pan)*1.02;
  }
  
  if (keys_down[5] && scale > min_scale) {
    scale = scale/1.02;
    x_pan = width*0.5 - (width*0.5 - x_pan)/1.02;
    y_pan = height*0.5 - (height*0.5 - y_pan)/1.02;
  }

  if (load_finished) {
    load_finished = false;
    refresh_screen();
  }
  
  else if (save_finished) {
    save_finished = false;
    refresh_screen();
  }

  else if (key_down()) {
    refresh_screen();
  }
}



void exit_handler() {
  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
    public void run () {
      if (mode == 0) {
        thread("save_csv");
      }
      else {println(end_points[0], end_points[1], end_points[2], end_points[3]);}
    }
  }));
}