void keyPressed() {
  if (keyCode == UP) {main.keys_down[0] = true;}
  if (keyCode == DOWN) {main.keys_down[1] = true;}
  if (keyCode == LEFT) {main.keys_down[2] = true;}
  if (keyCode == RIGHT) {main.keys_down[3] = true;}
  if (key == 'z' || key == 'Z') {main.keys_down[4] = true;}
  if (key == 'x' || key == 'X') {main.keys_down[5] = true;}
  if (key == 'h' || key == 'H') {main.help_mode = (main.help_mode + 1) % 3;}
  if (key == 'r' || key == 'R') {
    if (main.mode == 0 ) {
      thread("maze.open_csv");
    }
    else {
        maze.end_points[0] = -1;
        maze.end_points[1] = -1;
        maze.end_points[2] = -1;
        maze.end_points[3] = -1;
    }
  }
  if (key == 's' || key == 'S') {
    if (main.mode == 0) {
      thread("maze.save_csv");
    }
    else {
      maze.find_points();
    }
  }
  main.refresh_screen();
}


void keyReleased() {
  if (keyCode == UP) {main.keys_down[0] = false;}
  if (keyCode == DOWN) {main.keys_down[1] = false;}
  if (keyCode == LEFT) {main.keys_down[2] = false;}
  if (keyCode == RIGHT) {main.keys_down[3] = false;}
  if (key == 'z' || key == 'Z') {main.keys_down[4] = false;}
  if (key == 'x' || key == 'X') {main.keys_down[5] = false;}
}


void mousePressed() {
  int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
  int x = selected[0];
  int y = selected[1];
  main.prev_selected = selected;

  if (x != -1 && y != -1) {
    if (main.mode == 0) {
      if (maze.grid[y][x] == 0) {
        maze.grid[y][x] = 1;
      }
      else if (maze.grid[y][x] == 1) {
        maze.grid[y][x] = 0;
      }
    }

    if (main.mode == 1) {
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
  main.refresh_screen();
}


void mouseDragged() {
  if (main.mode == 0) {
    int[] selected = maze.index((mouseX - maze.x_pan)/maze.scale, (mouseY - maze.y_pan)/maze.scale);
    int x = selected[0];
    int y = selected[1];
    if (x != -1 && y != -1 && (x != main.prev_selected[0] || y != main.prev_selected[1])) {
      if (maze.grid[y][x] == 0) {
        maze.grid[y][x] = 1;
      }
      else if (maze.grid[y][x] == 1) {
        maze.grid[y][x] = 0;
      }
    }
    main.prev_selected = selected;

  }
  main.refresh_screen();
}


void mouseReleased() {
  main.prev_selected[0] = -1;
  main.prev_selected[1] = -1;
}