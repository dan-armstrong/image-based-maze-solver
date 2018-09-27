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
      open_csv();
    }
    else {
        end_points[0] = -1;
        end_points[1] = -1;
        end_points[2] = -1;
        end_points[3] = -1;
    }
  }
  if (key == 's' || key == 'S') {
    if (mode == 0) {
      thread("save_csv");
    }
    else {
      end_points = find_points();
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
  int[] selected = maze_index((mouseX - x_pan)/scale, (mouseY - y_pan)/scale);
  int x = selected[0];
  int y = selected[1];
  prev_selected = selected;

  if (x != -1 && y != -1) {
    if (mode == 0) {
      if (maze[y][x] == 0) {
        maze[y][x] = 1;
      }
      else if (maze[y][x] == 1) {
        maze[y][x] = 0;
      }
    }

    if (mode == 1) {
      if (x == end_points[0] && y == end_points[1]) {
        end_points[0] = end_points[2];
        end_points[1] = end_points[3];
        end_points[2] = -1;
        end_points[3] = -1;
      }
      else if (x == end_points[2] && y == end_points[3]) {
        end_points[2] = -1;
        end_points[3] = -1;
      }
      else if (maze[y][x] == 0) {
        if (end_points[2] != -1 && end_points[3] != -1) {
          end_points[0] = end_points[2];
          end_points[1] = end_points[3];
        }
        end_points[2] = x;
        end_points[3] = y;
      }
    }
  }
  refresh_screen();
}


void mouseDragged() {
  if (mode == 0) {
    int[] selected = maze_index((mouseX - x_pan)/scale, (mouseY - y_pan)/scale);
    int x = selected[0];
    int y = selected[1];
    if (x != -1 && y != -1 && (x != prev_selected[0] || y != prev_selected[1])) {
      if (maze[y][x] == 0) {
        maze[y][x] = 1;
      }
      else if (maze[y][x] == 1) {
        maze[y][x] = 0;
      }
    }
    prev_selected = selected;

  }
  refresh_screen();
}


void mouseReleased() {
  prev_selected[0] = -1;
  prev_selected[1] = -1;
}