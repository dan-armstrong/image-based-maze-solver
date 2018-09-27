library("data.table")

merge_sort <- function(v, string_input) {
  if (length(v) > 1) {
    m <- ceiling(length(v) / 2)
    a <- merge_sort(v[1:m], string_input)
    b <- merge_sort(v[(m+1):length(v)], string_input)
    return(merge_vectors(a, b, string_input))
  }
  return(v)
}


merge_vectors <- function(a, b, string_input) {
  pointer_a = 1
  pointer_b = 1
  range <- length(a)+length(b)
  merged <- rep(0, range)
  for (i in 1:range) {
    if (pointer_a > length(a)) {
      merged[i] <- b[pointer_b]
      pointer_b <- pointer_b + 1
    }
    else if (pointer_b > length(b)) {
      merged[i] <- a[pointer_a]
      pointer_a <- pointer_a + 1
    }
    else if (string_input) {
      a_value <- prod(as.integer(strsplit(a[pointer_a], '-')[[1]][3:4]))
      b_value <- prod(as.integer(strsplit(b[pointer_b], '-')[[1]][3:4]))
      if (a_value > b_value) {
        merged[i] <- a[pointer_a]
        pointer_a <- pointer_a + 1
      }
      else{
        merged[i] <- b[pointer_b]
        pointer_b <- pointer_b + 1
      }
    }
    else {
      if (a[pointer_a] < b[pointer_b]) {
        merged[i] <- a[pointer_a]
        pointer_a <- pointer_a + 1
      }
      else{
        merged[i] <- b[pointer_b]
        pointer_b <- pointer_b + 1
      }
    }
  }
  return(merged)
}


threshold_value <- function(hist) {                                             #CALCULATE T-VALUE FOR HISTOGRAM USING OTSU'S METHOD
  weighted_hist <- as.numeric(hist*0:(length(hist)-1))                          #WEIGHTED HIST STORED TO AVOID REPEATED CALCULATION
  class_variance <- function(t) {                                               #CALCULATE CLASS VARAINCE FOR PARTICULAR VALUE
    range_fg <- (t+1):length(hist)                                              #VECTORS OF FOREGROUND & BACKGROUND RANGES
    range_bg <- 1:t
    weight_fg <- sum(hist[range_fg])/sum(hist)                                  #CALCULATE FOREGROUND & BACKGROUND WEIGHTS & MEANS
    weight_bg <- sum(hist[range_bg])/sum(hist)
    mean_fg <- ifelse(sum(hist[range_fg]) > 0, sum(weighted_hist[range_fg])/sum(hist[range_fg]), 0)   #AVOID DIVISION BY ZERO
    mean_bg <- ifelse(sum(hist[range_bg]) > 0, sum(weighted_hist[range_bg])/sum(hist[range_bg]), 0)
    return(weight_fg*weight_bg*(mean_bg-mean_fg)^2)                             #RETURN CLASS VARIANCE FOR GIVEN VALUE
  }
  class_variances <- sapply(1:(length(hist)-1), class_variance)                 #CALCULATE CLASS VARIANCE FOR ALL POSSIBLE T_VALUES
  t_values <- which(class_variances==max(class_variances))                      #VECTOR OF ALL T-VALUES WITH MAXIMUM CLASS VARIANCE
  return(median(t_values))                                                      #RETURN MEDIAN T-VALUE IF MULTIPLE MAXIMUMS FOUND
}


threshold <- function(grid) {                                                   #THRESHOLD GREYSCALE GRID USING OTSU'S METHOD
  frequency <- function(x) {
    sum(as.numeric(grid==x)) }
  hist <- sapply(0:max(grid), frequency)                                        #CREATE HISTOGRAM OF LUMINANCE FREQUENCIES
  t <- threshold_value(hist)                                                    #USE OTSU'S METHOD TO CALCULATE APPROPRIATE THRESHOLD
  threshold_grid <- ifelse(grid > t, 0, 1)                                      #APPLY THRESHOLD TO GRID TO CREATE BINARY GRID
  return(threshold_grid)                                                        #RETURN BINARY MATRIX
}

setwd('/Users/danarmstrong/Desktop/Coursework')

greyscale_grid <- data.matrix(fread("/Users/danarmstrong/Desktop/Coursework/greyscale.csv"))
threshold_grid <- data.matrix(fread("/Users/danarmstrong/Desktop/Coursework/maze.csv"))

frequencies_h <- apply(threshold_grid, 1, sum)                                  #SUM ROWS AND COLUMNS SEPERATELY
frequencies_v <- apply(threshold_grid, 2, sum)

edges_up <- c(head(frequencies_h, 1), diff(frequencies_h))                      #FIND FREQUENCY DIFFERENCES BETWEEN NEIGHBOURING ROWS/COLUMNS
edges_down <- c(diff(frequencies_h)*(-1), tail(frequencies_h, 1))
edges_left <- c(head(frequencies_v, 1), diff(frequencies_v))
edges_right <- c(diff(frequencies_v)*(-1), tail(frequencies_v, 1))

#plot(ifelse(edges_left<0,0,edges_left), pch=1, cex=0.4,  xlab="Column number", ylab="Left-difference")
#abline(30, 0, untf = FALSE, col='brown3')

histogram_h <- sapply(0:max(edges_up), function(x) sum(edges_up==x))            #CALCULATE THRESHOLD VALUE USING OTSU'S METHOD
histogram_v <- sapply(0:max(edges_left), function(x) sum(edges_left==x))
threshold_h <- threshold_value(histogram_h)
threshold_v <- threshold_value(histogram_v)

walls_up <- which(edges_up>threshold_h)                                         #ROWS/COLUMNS WITH DIFFERENCES ABOVE THRESHOLD ARE WALL EDGES
walls_down <- which(edges_down>threshold_h)
walls_left <- which(edges_left>threshold_v)
walls_right <- which(edges_right>threshold_v)

cell_widths <- diff(walls_left)                                                 #CALCULATE AVERAGE DISTANCE BETWEEN WALLS
cell_heights <- diff(walls_up)
cell_width <- mean(cell_widths[cell_widths<=median(cell_widths)])               #CALCULATE MEAN BY IGNORING LARGE VALUES
cell_height <- mean(cell_heights[cell_heights<=median(cell_heights)])

c <- 1                                                                          #FIND MISSING HORIZONTAL WALLS
while (c <= length(cell_heights)) {
  if (cell_widths[c] > 1.5*cell_height) {
    range <- edges_up[(walls_up[c]+1):(walls_up[c]+round(cell_height))]
    maximum <- round(median(which(range==max(range))))
    walls_up <- append(walls_up, walls_up[c] + maximum - 1, after=c)
  }
  c <- c + 1
}

c <- 1                                                                          #FIND MISSING VERTICAL WALLS
while (c <= length(cell_widths)) {
  if (cell_widths[c] > 1.5*cell_width) {
    range <- edges_left[(walls_left[c]+1):(walls_left[c]+round(cell_width))]
    maximum <- round(median(which(range==max(range))))
    walls_left <- append(walls_left, walls_left[c] + maximum - 1, after=c)
  }
  c <- c + 1
}

wall_widths <- sapply(walls_left, function(x) walls_right[walls_right>=x][1] - x)#AVERAGE DISTANCE BETWEEN SIDES OF WALL
wall_heights <- sapply(walls_up, function(x) walls_down[walls_down>=x][1] - x)
wall_width <- mean(wall_widths[wall_widths<=median(wall_widths)]) + 1           #ADD 1 DUE TO UNDERCALCULATION OF SIZE
wall_height <- mean(wall_heights[wall_heights<=median(wall_heights)]) + 1

maze_grid <- matrix(0, nrow=length(walls_up)*2-1, ncol=length(walls_left)*2-1)

for (y in 1:length(walls_up)) {                                                 #LOOP THROUGH SECTIONS
  for (x in 1:length(walls_left)) {
    top_left <- threshold_grid[walls_up[y]:(walls_up[y]+wall_height),           #CALCULATE DENSITY OF EACH SQUARE
                               walls_left[x]:(walls_left[x]+wall_width)]
    if (mean(top_left) > 0.25) {maze_grid[2*y-1, 2*x-1] <- 1}

    if (x < length(walls_left)) {
      top_right <- threshold_grid[walls_up[y]:(walls_up[y]+wall_height),
                                 (walls_left[x]+wall_width):walls_left[x+1]]
      if (mean(top_right) > 0.25) {maze_grid[2*y-1, 2*x] <- 1}
    }

    if (y < length(walls_up)) {
      bottom_left <- threshold_grid[(walls_up[y]+wall_height):walls_up[y+1],
                                    walls_left[x]:(walls_left[x]+wall_width)]
      if (mean(bottom_left) > 0.25) {maze_grid[2*y, 2*x-1] <- 1}
    }

    if (x < length(walls_left) && y < length(walls_up)) {
      bottom_right <- threshold_grid[(walls_up[y]+wall_height):walls_up[y+1],
                                     (walls_left[x]+wall_width):walls_left[x+1]]
      if (mean(bottom_right) > 0.25) {maze_grid[2*y, 2*x] <- 1}
    }
  }
}

height_above <- function(x, y) {                                                #FIND AMOUNT OF EMPTY SPACE ABOVE A CELL
  height <- 0
  while (threshold_grid[y-height, x] == 0 && y-height >= 1) {height <- height + 1}
  return(height)
}

max_area <- function(x, y) {                                                    #FIND LARGEST RECTANGLE FOR A GIVEN CELL
  width <- 1
  height <- height_above(x, y)
  max_width <- 0
  max_height <- 0
  while (height >= 3 && x - width >= 0) {                                       #LOOP THROUGH DIFFERENT WIDTHS
    if (height_above(x - (width-1), y) < height) {
      height <- height_above(x - (width-1), y)
    }
    if (width*height > max_width*max_height && width >= 3 && height >= 3) {     #NEW MAX RECT FOUND
      max_width <- width
      max_height <- height
    }
    width <- width + 1
  }
  return(paste(max_width, max_height, sep='-'))
}

area_grid <- matrix(mapply(max_area, col(threshold_grid), row(threshold_grid)), nrow=nrow(threshold_grid))

area_vector <- c()
for (y in 1:nrow(area_grid)) {
  for (x in 1:ncol(area_grid)) {
    data <- as.integer(strsplit(area_grid[y, x], '-')[[1]])
    area <- data[1] * data[2]
    if (area > 0) {
      area_vector <- c(area_vector, paste(x, y, data[1], data[2], sep='-'))
    }
  }
}

if (length(area_vector) > 0) {
  area_vector <- merge_sort(na.omit(area_vector), TRUE)
}

rect_grid <- matrix(0, nrow=nrow(area_grid), ncol=ncol(area_grid))
for (row in area_vector) {
  area_data <- as.integer(strsplit(row, '-')[[1]])
  x <- area_data[1]
  y <- area_data[2]
  width <- area_data[3]
  height <- area_data[4]
  if (rect_grid[y, x] == 0) {
    empty_row <- FALSE
    empty_col <- FALSE
    while (width >= 3 && height >= 3 && (!empty_row || !empty_col)) {
      if (!empty_row) {
        if (all(rect_grid[y-(height-1), (x-(width-1)):x] == 0)) {empty_row = TRUE}
        else {height <- height - 1}
      }
      if (!empty_col) {
        if (all(rect_grid[(y-(height-1)):y, x-(width-1)] == 0)) {empty_col = TRUE}
        else {width <- width - 1}
      }
    }
    if (width >= 3 && height >= 3) {
      rect_grid[(y-(height-1)):y, (x-(width-1)):x] <- 1
      rect_grid[(y-(height-1)+1):(y-1), (x-(width-1)+1):(x-1)] <- 2
    }
  }
}

print(rect_grid)
