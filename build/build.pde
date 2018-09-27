int STATE;                                                                      //GLOBAL CONSTANTS
float MIN_SCALE = 1/pow(1.02,3);
String QUIT_FILE; 

Maze maze;                                                                      //GLOBAL VARIABLES
Menu main_menu;
int quit_timer, edit_timer;
int edit_pointer = -1;                                                          //MOVES BACK/FORWARD FOR UNDO/REDO
Boolean[] keys_down = {false, false, false, false, false, false, false, false};
ArrayList<int[]> edits = new ArrayList<int[]>();                                //KEEPS TRACK OF CELLS EDITED


void setup() {
  size(800,600);
  background(255);
  pixelDensity(displayDensity());
  noStroke();

  STATE = int(args[0]);                                                         //GET STATE FROM INPUT
  QUIT_FILE = "../" + args[1];  
  maze = new Maze("../" + args[2], float(args[4]) / float(args[3]), MIN_SCALE, #FF0066);
  main_menu = new Menu(1, createFont("Avenir Next", 16), #FF0066);
  quit_timer = millis();                                                        //CHECK QUIT AT REGULAR BASIS 
  edit_timer = millis();
  exit_handler();                                                               //SAVE END POINTS IF QUIT
  refresh_screen();
} 


void draw() {                                                                   //MAIN LOOP
  if (keys_down[0]) {maze.move(maze.x_pan, maze.y_pan + 5);}                    //CHECK WHICH KEYS ARE DOWN
  if (keys_down[1]) {maze.move(maze.x_pan, maze.y_pan - 5);}
  if (keys_down[2]) {maze.move(maze.x_pan + 5, maze.y_pan);}
  if (keys_down[3]) {maze.move(maze.x_pan - 5, maze.y_pan);}

  if (keys_down[4] && !keys_down[7]){
    maze.scale *= 1.02;
    maze.move(width*0.5 - (width*0.5 - maze.x_pan)*1.02, 
              height*0.5 - (height*0.5 - maze.y_pan)*1.02);
  }

  if (keys_down[5] && maze.scale > MIN_SCALE) {
    maze.scale = maze.scale/1.02;
    maze.move(width*0.5 - (width*0.5 - maze.x_pan)/1.02, 
              height*0.5 - (height*0.5 - maze.y_pan)/1.02);
  }
                                                                                //UNDO LAST MOVE
  if (keys_down[7] && keys_down[4] && edit_pointer >= 0 && millis() - edit_timer > 150){
    int[] pos = edits.get(edit_pointer);
    maze.grid[pos[1]][pos[0]] = (maze.grid[pos[1]][pos[0]] + 1) % 2;
    edit_pointer -= 1;
    edit_timer = millis();                                                      //STOP REPEAT UNDO'S OCCURING TOO FAST
  }
                                                                                //REDO LAST MOVE
  if (keys_down[7] && keys_down[6] && edit_pointer + 1 < edits.size() && millis() - edit_timer > 150){
    edit_pointer += 1;
    int[] pos = edits.get(edit_pointer);
    maze.grid[pos[1]][pos[0]] = (maze.grid[pos[1]][pos[0]] + 1) % 2;
    edit_timer = millis();
  }
  
  for (Boolean k : keys_down) {                                                 //UPDATE SCREEN IF SOMETHING CHANGES
    if (k) {
      refresh_screen();
      break;
    }
  }
  
  if (millis() - quit_timer > 500) {                                           //CHECK QUIT EVERY 500MS
    thread("check_quit");
    quit_timer = millis();
  }
}


void exit_handler() {                                                          //SAVE WHAT HAS BEEN DONE WHEN QUITTING
  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
    public void run () {
      if (STATE == 2) {
        println(maze.end_points[0], maze.end_points[1], maze.end_points[2], maze.end_points[3]);
      }
      else{
        maze.save_csv();
      }
    }
  }));
}