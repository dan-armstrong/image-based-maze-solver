void refresh_screen() {
  background(255);
  draw_maze();
  draw_menu();
}


void draw_maze() {
  if (x_pan/scale > 0) {
    x_pan = 0.0;
  }
  if (y_pan/scale > 0) {
    y_pan = 0.0;
  }
  if (x_pan + maze_width*cell_size*scale < width) {
    x_pan = width - maze_width*cell_size*scale;
  }
  if (y_pan + maze_height*cell_size*scale < height) {
    y_pan = height - maze_height*cell_size*scale;
  }
  if (maze_width*cell_size*scale < width) {
    x_pan = (width - maze_width*cell_size*scale) / 2;
  }
  if (maze_height*cell_size*scale < height) {
    y_pan = (height - maze_height*cell_size*scale) / 2;
  }
  
  int x_min = max(0, floor((-x_pan/scale)/cell_size)*2);
  int x_max = min(maze[0].length, ceil(((width-x_pan)/scale)/cell_size)*2);
  int y_min = max(0, floor((-y_pan/scale)/cell_size)*2);
  int y_max = min(maze.length, ceil(((height-y_pan)/scale)/cell_size)*2);
  
  rectMode(CORNER);
  pushMatrix();
  scale(scale);
  translate(x_pan/scale,y_pan/scale);
  for (int y = y_min; y < y_max; y++) {
    for (int x = x_min; x < x_max; x++) {
      float[] dims = dimensions(x, y);
      if ((x == end_points[0] && y == end_points[1]) || (x == end_points[2] && y == end_points[3])) {
        fill(pink);
        rect(dims[0], dims[1], dims[2], dims[3]);
      }
      else if (maze[y][x] == 1) {
        fill(0);
        rect(dims[0], dims[1], dims[2], dims[3]);
      }
    }
  }
  popMatrix();
}


void draw_menu() {
  if (help_mode != 0 || loading || saving) {
    rectMode(CENTER);
    fill(pink, 210);
    rect(width*0.5, height*0.5, width*0.6, 125, 7);
    textAlign(CENTER, CENTER);
    fill(255);
  }
  if (loading) {
      textFont(menu_font, 40);
      text("LOADING MAZE", width*0.5, height*0.5 - 3);
  }
  else if (saving) {
      textFont(menu_font, 40);
      text("SAVING MAZE", width*0.5, height*0.5 - 3);
  }
  else if (help_mode == 1) {
    if (mode == 0) {
      textFont(menu_font, 40);
      text("EDITING MODE", width*0.5, height*0.5 - 40);
      textFont(menu_font, 20);
      text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
      text("PRESS [R] TO RESET MAZE TO LAST SAVE", width*0.5, height*0.5 + 21);
      text("PRESS [S] TO SAVE EDITS", width*0.5, height*0.5 + 45);
    }
    else {
      textFont(menu_font, 40);
      text("SELECTING MODE", width*0.5, height*0.5 - 40);
      textFont(menu_font, 20);
      text("PRESS [H] TO TOGGLE HELP", width*0.5, height*0.5 - 3);
      text("PRESS [R] TO RESET END POINTS", width*0.5, height*0.5 + 21);
      text("PRESS [A] TO AUTO-FIND POINTS", width*0.5, height*0.5 + 45);
    }
  }
  else if (help_mode == 2) {
    if (mode == 0) {
      textFont(menu_font, 20);
      text("CLICK ON WALLS TO CHANGE TO PATH", width*0.5, height*0.5 - 51);
      text("CLICK ON PATHS TO CHANGE TO WALL", width*0.5, height*0.5 - 27);
      text("USE ARROWS AND [Z X] TO ZOOM AND PAN", width*0.5, height*0.5 - 3);
      text("PRESS [CTRL+Z / CTRL+Y] TO UNDO/REDO", width*0.5, height*0.5 + 21);
      text("ONCE FINISHED, SAVE AND QUIT TO CONTINUE", width*0.5, height*0.5 + 45);
    }
    else {
      textFont(menu_font, 20);
      text("CLICK TO SELECT AN END POINT", width*0.5, height*0.5 - 51);
      text("CLICK ON AN END POINT TO REMOVE IT", width*0.5, height*0.5 - 27);
      text("END POINTS MUST BE ON THE PATH", width*0.5, height*0.5 - 3);
      text("END POINTS DISPLAYED IN PINK", width*0.5, height*0.5 + 21);
      text("ONCE POINTS SELECTED, QUIT TO CONTINUE", width*0.5, height*0.5 + 45);
    }
  }
}