void keyPressed() {                                                               //CALLED WHEN KEYS ARE PRESSED DOWN
  if (keyCode == UP) {keys_down[0] = true;}                                       //CHANGE STATE OF KEYS_DOWN FOR EACH KEY
  if (keyCode == DOWN) {keys_down[1] = true;}                                     //MEANS CERTAIN KEYS CAN BE HELD DOWN
  if (keyCode == LEFT) {keys_down[2] = true;}
  if (keyCode == RIGHT) {keys_down[3] = true;}
  if (key == 'z' || key == 'Z') {keys_down[4] = true;}
  if (key == 'x' || key == 'X') {keys_down[5] = true;}
  if (key == 'y' || key == 'Y') {keys_down[6] = true;}
  if (keyCode == 157 || keyCode == CONTROL) {keys_down[7] = true;}
  if (key == 'h' || key == 'H') {main_menu.change_mode();}                        //CHANGE MENU MDOE
  if (key == 'r' || key == 'R') {                                                 //RESET MAZE
    if (STATE == 0 ||  STATE == 1) {
      maze.open_csv();
    }
    else {
        maze.end_points[0] = -1;
        maze.end_points[1] = -1;
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
    }
  }
  if (key == 's' || key == 'S') {                                                 //SAVE MAZE
    if (STATE == 0 || STATE == 1) {
      maze.save_csv();
    }
    exit();
  }
  refresh_screen();
}


void keyReleased() {                                                              //CALLED WHEN KEY LIFTED
  if (keyCode == UP) {keys_down[0] = false;}                                      //CHANGE STATE OF KEYS_DOWN FOR EACH KEY
  if (keyCode == DOWN) {keys_down[1] = false;}
  if (keyCode == LEFT) {keys_down[2] = false;}
  if (keyCode == RIGHT) {keys_down[3] = false;}
  if (key == 'z' || key == 'Z') {keys_down[4] = false;}
  if (key == 'x' || key == 'X') {keys_down[5] = false;}
  if (key == 'y' || key == 'Y') {keys_down[6] = false;}
  if (keyCode == 157 || keyCode == CONTROL) {keys_down[7] = false;}
}


void mousePressed() {                                                             //CALLED WHEN MOUSE PRESSED
  int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
  int x = selected[0];                                                            //GET MOUSE POSITION INDEX
  int y = selected[1];
  maze.prev_selected = selected;                                                  //SET PREVIOUS TO CURRENT SELECTION

  if (x != -1 && y != -1) {                                                       //VALID INDEX ONLY
    if (STATE == 0 || STATE == 1) {
      maze.grid[y][x] = (maze.grid[y][x] + 1) % 2;                                //CHANGE STATE
      while (edit_pointer + 1 < edits.size()) {edits.remove(edit_pointer + 1);}   //REMOVE ALL POSSIBLE REDO EDITS
      edits.add(new int[] {x, y});
      edit_pointer += 1;
    }

    else {                                                           
      if (x == maze.end_points[0] && y == maze.end_points[1]) {                   //DESELECT 1ST END POINT
        maze.end_points[0] = maze.end_points[2];    
        maze.end_points[1] = maze.end_points[3];
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
      }
      else if (x == maze.end_points[2] && y == maze.end_points[3]) {              //DESELECT 2ND END POINT
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
      }
      else if (maze.grid[y][x] == 0) {
        if (maze.end_points[2] != -1 && maze.end_points[3] != -1) {               //2ND END POINT
          maze.end_points[0] = maze.end_points[2];                                //SHIFT END POINTS UP QUEUE
          maze.end_points[1] = maze.end_points[3];
        }
        maze.end_points[2] = x;                                                   //ADD SELECTED TO END POINT
        maze.end_points[3] = y;
      }
    }
  }
  refresh_screen();
}


void mouseDragged() {                                                             //CALLED WHEN MOUSE HELD DOWN + MOVED
  if (STATE == 0 || STATE == 1) {
    int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
    int x = selected[0];
    int y = selected[1];                                                          //CHECK VALID POINT + NOT CURRENT POINT
    if (x != -1 && y != -1 && (x != maze.prev_selected[0] || y != maze.prev_selected[1])) {//STOPS REPEATED CHANGE OF SAME POINT
      maze.grid[y][x] = (maze.grid[y][x] + 1) % 2;
      while (edit_pointer + 1 < edits.size()) {edits.remove(edit_pointer + 1);}   //REMOVE INVALID EDITS
      edits.add(new int[] {x, y});
      edit_pointer += 1;
    }
    maze.prev_selected = selected;
  }
  refresh_screen();
}


void mouseReleased() {                                                             //REMOVE PREVIOUSLY SELECTED WHEN RELEASED
  maze.prev_selected[0] = -1;
  maze.prev_selected[1] = -1;
}