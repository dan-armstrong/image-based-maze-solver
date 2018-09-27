Float scale, x_pan, y_pan;

void setup() {
  size(800,600);
  background(35);
  pixelDensity(displayDensity());
  fill(255);
  stroke(255);
  strokeWeight(0);
  scale = 1.0;
  x_pan = 0.0;
  y_pan = 0.0;
}

void draw() {
  if (keyPressed == true) { 
    if (key == 'w') {y_pan += 5 + scale;}
    if (key == 'a') {x_pan += 5 + scale;}
    if (key == 's') {y_pan -= 5 + scale;}
    if (key == 'd') {x_pan -= 5 + scale;}
    if (key == 'z') {
      scale *= 1.02;
      x_pan = width/2.0 - (width/2.0 - x_pan)*1.02;
      y_pan = height/2.0 - (height/2.0 - y_pan)*1.02;
    }
    if (key == 'x' && scale > 1) {
      scale = scale/1.02;
      x_pan = width/2.0 - (width/2.0 - x_pan)/1.02;
      y_pan = height/2.0 - (height/2.0 - y_pan)/1.02;

    }
  }
  
  Integer x_min = 0;
  Integer x_max = 5;
  Integer y_min = 0;
  Integer y_max = 5;
  background(30);
  scale(scale);
  translate(x_pan/scale,y_pan/scale);
  fill(255,100,0);
  fill(255);
  for (int y = y_min; y < y_max; y++) {
    for (int x = x_min; x < x_max; x++) {
      rect(x*50,y*50,40,40);
    }
  }
}