void refresh_screen() {                                                            //DRAWS CONTENTS TO SCREEN
  background(255);
  maze.display();
  main_menu.display();
}


void check_quit() {                                                                //CHECK QUIT FILE AND QUITS IF NEEDED
  String[] status = loadStrings(QUIT_FILE);
  if (status.length > 0) {
    if (status[0].equals("q")) {
      println("quit");
      exit();
    }
  }
}