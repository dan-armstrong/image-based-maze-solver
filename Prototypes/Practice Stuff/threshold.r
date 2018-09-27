library("data.table")

threshold_value <- function(hist) {                                             #CALCULATE T-VALUE FOR HISTOGRAM USING OTSU'S METHOD
  weighted_hist <- as.numeric(hist*0:(length(hist)-1))                          #WEIGHTED HIST STORED TO AVOID REPEATED CALCULATION
  class_variance <- function(t) {                                               #CALCULATE CLASS VARAINCE FOR PARTICULAR VALUE
    range_fg <- 1:t                                                             #VECTORS OF FOREGROUND & BACKGROUND RANGES
    range_bg <- (t+1):length(hist)
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
  hist <- sapply(1:max(grid), function(x) sum(grid==x))                         #CREATE HISTOGRAM OF LUMINANCE FREQUENCIES
  t <- threshold_value(hist)                                                    #USE OTSU'S METHOD TO CALCULATE APPROPRIATE THRESHOLD
  theshold_grid <- ifelse(grid > t, 0, 1)                                       #APPLY THRESHOLD TO GRID TO CREATE BINARY GRID
  return(theshold_grid)                                                         #RETURN BINARY MATRIX
}


local_maximum <- function(vector, a, b) {
  range <- vector[a:b]
  maximum <- round(median(which(range==max(range))))
  return(a + maximum - 1)
}


wall_data <- function(threshold_grid) {                                         #DETERMINES STRUCTURE OF WALLS FROM THRESHOLD GRID
  rows <- nrow(threshold_grid)                                                  #GET SIZE OF GRID
  cols <- ncol(threshold_grid)
  frequencies_h <- apply(threshold_grid, 1, sum)                                #CALCULATE FREQUENCY OF 1'S PER ROW/COLUMN (H/V)
  frequencies_v <- apply(threshold_grid, 2, sum)
  differences_up <- frequencies_h - c(0,frequencies_h[1:(rows-1)])              #FIND FREQUENCY DIFFERENCES BETWEEN NEIGHBOURING ROWS/COLUMNS
  differences_down <- frequencies_h - c(frequencies_h[2:rows],0)
  differences_left <- frequencies_v - c(0,frequencies_v[1:(cols-1)])
  differences_right <- frequencies_v - c(frequencies_v[2:cols],0)

  histogram_h <- sapply(0:max(differences_up), function(x) sum(differences_up==x)) #CALCULATE THRESHOLD VALUE USING OTSU'S METHOD
  histogram_v <- sapply(0:max(differences_left), function(x) sum(differences_left==x))
  threshold_h <- threshold_value(histogram_h)                                   #ROWS/COLUMNS WITH DIFFERENCES ABOVE THRESHOLD ARE WALLS
  threshold_v <- threshold_value(histogram_v)

  walls_up <- which(differences_up>threshold_h)                                 #POSITION OF HORIZONTAL/VERTICAL WALLS IN GRID
  walls_down <- which(differences_down>threshold_h)                             #UP IS TOP SIDE OF WALL & DOWN IS BOTTOM SIDE
  walls_left <- which(differences_left>threshold_v)
  walls_right <- which(differences_right>threshold_v)
  wall_widths <- sapply(walls_left, function(x) walls_right[walls_right>=x][1] - x) #AVERAGE DISTANCE BETWEEN SIDES OF WALL
  wall_heights <- sapply(walls_up, function(x) walls_down[walls_down>=x][1] - x)
  wall_width <- mean(wall_widths[wall_widths<=median(wall_widths)])
  wall_height <- mean(wall_heights[wall_heights<=median(wall_heights)])

  cell_widths <- walls_left[2:length(walls_left)] - walls_left[1:(length(walls_left)-1)] #GET DISTANCE BETWEEN NEIGHBOURING WALLS
  cell_heights <- walls_up[2:length(walls_up)] - walls_up[1:(length(walls_up)-1)]
  cell_width <- mean(cell_widths[cell_widths<=median(cell_widths)])             #CALCULATE AVERAGE DISTANCE BETWEEN WALLS
  cell_height <- mean(cell_heights[cell_heights<=median(cell_heights)])

  add_left <- function(i) {
    missing_amount <- round(cell_widths[i] / cell_width) - 1
    if (missing_amount > 0) {
      mid_estimates <- (1:missing_amount)*cell_width+walls_left[i]
      min_ranges <- sapply(mid_estimates, function(x) round(x-0.5*cell_width))
      max_ranges <- sapply(mid_estimates, function(x) round(x+0.5*cell_width))
      positions <- mapply(function(a, b) local_maximum(differences_left, a, b), min_ranges, max_ranges)
      return(positions) }
    return(NA) }

  add_up <- function(i) {
    missing_amount <- round(cell_heights[i] / cell_height) - 1
    if (missing_amount > 0) {
      mid_estimates <- (1:missing_amount)*cell_height+walls_up[i]
      min_ranges <- sapply(mid_estimates, function(x) round(x-0.5*cell_height))
      max_ranges <- sapply(mid_estimates, function(x) round(x+0.5*cell_height))
      positions <- mapply(function(a, b) local_maximum(differences_up, a, b), min_ranges, max_ranges)
      return(positions) }
    return(NA) }

  missing_left <- sapply(1:length(cell_widths), add_left)
  missing_up <- sapply(1:length(cell_heights), add_up)
  walls_horizontal <- sort(c(walls_up, missing_up[!is.na(missing_up)]))
  walls_vertical <- sort(c(walls_left, missing_left[!is.na(missing_left)]))

  range <- 1:max(length(c(wall_width,wall_height)),length(walls_horizontal),length(walls_vertical))
  return(matrix(c(c(wall_width,wall_height)[range],walls_horizontal[range],walls_vertical[range]),ncol=3))
}


maze <- function(threshold_grid) {                                              #CREATE MAZE GRID FROM THRESHOLD GRID
  structure_matrix <- wall_data(threshold_grid)                                 #GET STRUCTURE OF MAZE FROM THRESHOLD GRID
  wall_width <- structure_matrix[1,1]
  wall_height <- structure_matrix[2,1]
  walls_horizontal <- structure_matrix[,2][!is.na(structure_matrix[,2])]
  walls_vertical <- structure_matrix[,3][!is.na(structure_matrix[,3])]
  dimensions_x <- length(walls_vertical)-1
  dimensions_y <- length(walls_horizontal)-1

  position_x <- walls_vertical[1]
  position_y <- walls_horizontal[1]
  maze_width <- walls_vertical[length(walls_vertical)] + wall_width - position_x
  maze_height <- walls_horizontal[length(walls_horizontal)] + wall_width - position_y

  section_density <- function(x, y) {
    if (x %% 2 == 0) {
      range_x <- (walls_vertical[x/2]+wall_width+1):(walls_vertical[x/2+1]-1) }
    else {
      range_x <- walls_vertical[(x+1)/2]:(walls_vertical[(x+1)/2]+wall_width) }
    if (y %% 2 == 0) {
      range_y <- (walls_horizontal[y/2]+wall_height+1):(walls_horizontal[y/2+1]-1) }
    else {
      range_y <- walls_horizontal[(y+1)/2]:(walls_horizontal[(y+1)/2]+wall_height) }
    section <- threshold_grid[range_y,range_x]
    return(sum(section)/(length(range_x)*length(range_y))) }

  empty_grid <- matrix(0, nrow=dimensions_y*2+1, ncol=dimensions_x*2+1)
  density_grid <- matrix(mapply(section_density, col(empty_grid), row(empty_grid)), nrow=nrow(maze_grid))
  maze_grid <- ifelse(density_grid > 0.5, 1, 0)
  return(maze_grid)
}

create_nodes <- function(maze_grid) {
  valid_node <- function(x, y) {
    if (x == 1) {return TRUE}
    if (y == 1) {return TRUE}
    if (x == ncol(maze_grid)) {return TRUE}
    if (y == ncol(maze_grid)) {return TRUE}
    
  }
}



csv_file <- as.character(commandArgs(trailingOnly = TRUE))
csv_file <- '/Users/danarmstrong/Desktop/Coursework/greyscale.csv'
greyscale_grid <- data.matrix(fread(csv_file))
threshold_grid <- threshold(greyscale_grid)
test_grid <- maze(threshold_grid)
write.table(test_grid, file = "test.csv",row.names = FALSE, col.names = FALSE,sep = ",")
write.table(threshold_grid, file = "threshold.csv",row.names = FALSE, col.names = FALSE,sep = ",")
cat('lol')
