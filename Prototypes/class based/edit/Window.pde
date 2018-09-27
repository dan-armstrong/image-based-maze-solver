public class Window {
  int[] prev_selected = {-1,-1};
  boolean[] keys_down = {false, false, false, false, false, false};
  int mode, help_mode;
  color pink;
  PFont menu_font;

  
  Window(int program_mode, int help, color col, PFont font) {
    mode = program_mode;
    help_mode = help;
    pink = col;
    menu_font = font;
  }
  
  
  void refresh_screen() {
    background(255);
    draw_maze();
    draw_menu();
  }
  
  
  void draw_maze() {
    maze.display();
  }
  
  
  void draw_menu() {
    if (help_mode != 0 || maze.loading || maze.saving) {
      rectMode(CENTER);
      fill(pink, 210);
      rect(width*0.5, height*0.5, width*0.6, 125, 7);
      textAlign(CENTER, CENTER);
      fill(255);
    }
    if (maze.loading) {
        textFont(menu_font, 40);
        text("LOADING MAZE", width*0.5, height*0.5 - 3);
    }
    else if (maze.saving) {
        textFont(menu_font, 40);
        text("SAVING MAZE", width*0.5, height*0.5 - 3);
    }
    else if (help_mode == 1) {
      if (MODE == 0) {
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
      if (MODE == 0) {
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
}