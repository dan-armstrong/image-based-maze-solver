library("data.table")                                                           #PACKAGES


input <- strsplit(as.character(commandArgs(trailingOnly = TRUE)), ' ')[[1]]     #GET INPUT FROM PYTHON
setwd(input[1])                                                                 #SET CURRENT WORKING DIRECTORY
source('merge.r')
GREYSCALE_GRID <- data.matrix(fread(input[2]))                                  #SET GLOBAL CONSTANTS
QUIT_FILE <- input[3]
UPDATE_FILE <- input[4]
RECTILINEAR <- ifelse(input[5] == 'True', TRUE, FALSE)
INVERTED <- ifelse(input[6] == 'True', TRUE, FALSE)
WALL_FILE <- 'walls.csv'
MAZE_FILE <- 'maze.csv'


main <- function() {                                                            #MAIN FUNCTION GROUPED FOR ERROR CHECKING
  update('Loading Greyscale')
  threshold_grid <- threshold(GREYSCALE_GRID)
  if (RECTILINEAR) {                                                            #SAVE MAZE GRID IF RECTILINEAR
    structure_matrix <- wall_data(threshold_grid)
    maze_grid <- maze(threshold_grid, structure_matrix)
    update('Saving Maze')
    write.table(structure_matrix[,3:2]-1, file = WALL_FILE,                     #-1 FOR INDEXING BETWEEN R (1) & PYTHON (0)
                row.names = FALSE, col.names = FALSE,sep = ",")                 #3:2 SO X IS PRINTED BEFORE Y
    write.table(maze_grid, file = MAZE_FILE,
                row.names = FALSE, col.names = FALSE,sep = ",")
    cell_size <- mean(c(structure_matrix[1,1],structure_matrix[3,1]))           #AVERAGE DISTANCE BETWEEN WALLS
    wall_size <- mean(c(structure_matrix[2,1],structure_matrix[4,1]))           #AVERAGE WIDTH OF WALLS
    return(c(WALL_FILE, MAZE_FILE, cell_size, wall_size))
  }
  update('Saving Maze')                                                         #SAVE THRESHOLD GRID IF NON-RECTILINEAR
  write.table(threshold_grid, file = MAZE_FILE,row.names = FALSE, col.names = FALSE,sep = ",")
  return(MAZE_FILE)
}


update <- function(text) {                                                      #EDIT UPDATE FILE
  check_quit()
  f <- file(UPDATE_FILE)
  writeLines(c(text), f)
  close(f)
}


check_quit <- function() {                                                      #CHECK TO SEE IF QUITTING
  status <- readChar(QUIT_FILE, file.info(QUIT_FILE)$size)
  if (status == 'q') {stop('quit')}                                             #STOP PROGRAM
}


threshold_value <- function(hist) {                                             #CALCULATE T-VALUE FOR HISTOGRAM USING OTSU'S METHOD
  weighted_hist <- as.numeric(hist*0:(length(hist)-1))                          #WEIGHTED HIST STORED TO AVOID REPEATED CALCULATION
  class_variance <- function(t) {                                               #CALCULATE CLASS VARAINCE FOR PARTICULAR T VALUE
    update(paste('Calculating Threshold',round(t/length(hist)*100),'%'))
    range_fg <- (t+1):length(hist)                                              #VECTORS OF FOREGROUND & BACKGROUND RANGES
    range_bg <- 1:t
    weight_fg <- sum(hist[range_fg])/sum(hist)
    weight_bg <- sum(hist[range_bg])/sum(hist)
    mean_fg <- ifelse(sum(hist[range_fg]) > 0, sum(weighted_hist[range_fg])/sum(hist[range_fg]), 0)   #AVOID DIVISION BY ZERO
    mean_bg <- ifelse(sum(hist[range_bg]) > 0, sum(weighted_hist[range_bg])/sum(hist[range_bg]), 0)
    return(weight_fg*weight_bg*(mean_bg-mean_fg)^2)                             #RETURN CLASS VARIANCE FOR GIVEN VALUE
  }
  class_variances <- sapply(1:(length(hist)-1), class_variance)                 #CALCULATE CLASS VARIANCE FOR ALL POSSIBLE T_VALUES
  t_values <- which(class_variances==max(class_variances))
  return(median(t_values))                                                      #RETURN MEDIAN T-VALUE WITH MAX VARIANCE
}


threshold <- function(grid) {                                                   #THRESHOLD GREYSCALE GRID USING OTSU'S METHOD
  frequency <- function(x) {
    update(paste('Creating Histogram',round(x/max(grid)*100),'%'))
    sum(as.numeric(grid==x)) }
  hist <- sapply(0:max(grid), frequency)                                        #CREATE HISTOGRAM OF LUMINANCE VALUES
  t <- ifelse(length(hist) > 1, threshold_value(hist), -1)
  update('Creating Binary Grid')
  if (INVERTED) {threshold_grid <- ifelse(grid < t, 0, 1)}                      #IF INVERTED DARK = 0 & LIGHT = 1
  else {threshold_grid <- ifelse(grid > t, 0, 1)}
  return(threshold_grid)                                                        #RETURN BINARY MATRIX
}


local_maximum <- function(vector, a, b) {                                       #FINDS MAX VALUE IN GIVEN RANGE
  range <- vector[a:b]
  maximum <- round(median(which(range==max(range))))
  return(a + maximum - 1)
}


wall_data <- function(threshold_grid) {                                         #DETERMINES STRUCTURE OF WALLS FROM THRESHOLD GRID
  update('Calculating Frequencies')
  rows <- nrow(threshold_grid)
  cols <- ncol(threshold_grid)
  frequencies_h <- apply(threshold_grid, 1, sum)                                #CALCULATE FREQUENCY OF 1'S PER ROW/COLUMN
  frequencies_v <- apply(threshold_grid, 2, sum)
  update('Finding Edges')
  edges_up <- c(head(frequencies_h, 1), diff(frequencies_h))                    #FIND FREQ DIFFERENCES BETWEEN NEIGHBOURING ROWS/COLUMNS
  edges_down <- c(diff(frequencies_h)*(-1), tail(frequencies_h, 1))
  edges_left <- c(head(frequencies_v, 1), diff(frequencies_v))
  edges_right <- c(diff(frequencies_v)*(-1), tail(frequencies_v, 1))
  edges_h <- merge_sort(ifelse(edges_up > 0, edges_up, 0))                      #REPLACE NEGATIVE EDGES
  edges_v <- merge_sort(ifelse(edges_left > 0, edges_left, 0))
  edges_h <- edges_h[1:(length(edges_h)-1)]                                     #REMOVE LARGEST AS THIS IS MAZE BOUNDARY
  edges_v <- edges_h[1:(length(edges_h)-1)]

  histogram_h <- sapply(0:edges_h[length(edges_h)], function(x) sum(edges_h==x))#CALCULATE THRESHOLD VALUE USING OTSU'S METHOD
  histogram_v <- sapply(0:edges_v[length(edges_v)], function(x) sum(edges_v==x))
  threshold_h <- threshold_value(histogram_h)                                   #ROWS/COLUMNS WITH DIFFERENCES ABOVE THRESHOLD ARE WALLS
  threshold_v <- threshold_value(histogram_v)

  update('Finding Walls')
  walls_up <- which(edges_up>threshold_h)                                       #POSITION OF HORIZONTAL/VERTICAL WALLS IN GRID
  walls_down <- which(edges_down>threshold_h)
  walls_left <- which(edges_left>threshold_v)
  walls_right <- which(edges_right>threshold_v)
  wall_widths <- sapply(walls_left, function(x) walls_right[walls_right>=x][1] - x)#AVERAGE DISTANCE BETWEEN SIDES OF WALL
  wall_heights <- sapply(walls_up, function(x) walls_down[walls_down>=x][1] - x)
  wall_width <- mean(wall_widths[wall_widths<=median(wall_widths)]) + 1         #ADD 1 DUE TO UNDERCALCULATION OF SIZE
  wall_height <- mean(wall_heights[wall_heights<=median(wall_heights)]) + 1

  update('Finding Cells')
  cell_widths <- diff(walls_left)                                               #GET DISTANCE BETWEEN NEIGHBOURING WALLS
  cell_heights <- diff(walls_up)
  cell_width <- mean(cell_widths[cell_widths<=median(cell_widths)])             #CALCULATE AVERAGE DISTANCE BETWEEN WALLS
  cell_height <- mean(cell_heights[cell_heights<=median(cell_heights)])

  add_left <- function(i) {                                                     #FINDS MISSING VERTICAL WALLS
    missing_amount <- round(cell_widths[i] / cell_width) - 1                    #NUMBER OF WALLS MISSING
    if (missing_amount > 0) {
      mid_estimates <- (1:missing_amount)*cell_width+walls_left[i]              #FINDS MULTIPLE MISSING WALLS AT ONCE
      min_ranges <- sapply(mid_estimates, function(x) round(x-0.5*cell_width))
      max_ranges <- sapply(mid_estimates, function(x) round(x+0.5*cell_width))
      positions <- mapply(function(a, b) local_maximum(edges_left, a, b), min_ranges, max_ranges) #MOST LIKELY TO BE WALL
      return(positions) }
    return(NA) }                                                                #RETURN PLACEHOLDER TO BE REMOVED

  add_up <- function(i) {                                                       #FINDS MISSING HORIZONTAL WALLS
    missing_amount <- round(cell_heights[i] / cell_height) - 1
    if (missing_amount > 0) {
      mid_estimates <- (1:missing_amount)*cell_height+walls_up[i]
      min_ranges <- sapply(mid_estimates, function(x) round(x-0.5*cell_height))
      max_ranges <- sapply(mid_estimates, function(x) round(x+0.5*cell_height))
      positions <- mapply(function(a, b) local_maximum(edges_up, a, b), min_ranges, max_ranges)
      return(positions) }
    return(NA) }

  update('Locating Missing Walls')
  missing_left <- sapply(1:length(cell_widths), add_left)                       #FIND MISSING WALLS
  missing_up <- sapply(1:length(cell_heights), add_up)
  walls_horizontal <- merge_sort(unlist(c(walls_up, missing_up[!is.na(missing_up)])))#ADD MISSING AND SORT INTO CORRECT ORDER
  walls_vertical <- merge_sort(unlist(c(walls_left, missing_left[!is.na(missing_left)])))

  cell_data <- c(cell_width, wall_width, cell_height, wall_height)              #DATA TO BE RETURNED
  range <- 1:max(length(cell_data),length(walls_horizontal),length(walls_vertical))#MATRIX PADDED WITH NA'S FOR DIFFERENT LENGTHS
  return(matrix(c(cell_data[range],walls_horizontal[range],walls_vertical[range]),ncol=3))
}


maze <- function(threshold_grid, structure_matrix) {                            #CREATE MAZE GRID FROM THRESHOLD GRID
  update('Calculating Structure')
  wall_width <- structure_matrix[2,1]
  wall_height <- structure_matrix[4,1]
  walls_horizontal <- structure_matrix[,2][!is.na(structure_matrix[,2])]
  walls_vertical <- structure_matrix[,3][!is.na(structure_matrix[,3])]
  dimensions_x <- length(walls_vertical)-1
  dimensions_y <- length(walls_horizontal)-1

  section_density <- function(x, y) {                                           #CALCULATE FRACTION OF 1'S IN SECTION
    if (y == 1) {update(paste('Building Maze',round(x/(dimensions_x*2+1)*100),'%'))}
    if (x %% 2 == 0) {                                                          #SECTION OF WALL (VERTICAL)
      range_x <- (walls_vertical[x/2]+wall_width):(walls_vertical[x/2+1]-1) }
    else {                                                                      #SECTION OF PATH
      range_x <- walls_vertical[(x+1)/2]:(walls_vertical[(x+1)/2]+wall_width-1) }
    if (y %% 2 == 0) {                                                          #SECTION OF WALL (HORIZONTAL)
      range_y <- (walls_horizontal[y/2]+wall_height):(walls_horizontal[y/2+1]-1) }
    else {                                                                      #SECTION OF PATH
      range_y <- walls_horizontal[(y+1)/2]:(walls_horizontal[(y+1)/2]+wall_height-1) }
    section <- threshold_grid[range_y,range_x]
    return(mean(section)) }

  empty_grid <- matrix(0, nrow=dimensions_y*2+1, ncol=dimensions_x*2+1)         #EMPTY GRID REPRESENTING EACH SECTION
  density_grid <- matrix(mapply(section_density, col(empty_grid), row(empty_grid)), nrow=nrow(empty_grid))
  maze_grid <- ifelse(density_grid > 0.25, 1, 0)                                #DENSITIES ABOVE 25% ARE WALL SECTIONS
  return(maze_grid)
}

output <- tryCatch(                                                             #CATCH AND RETURN QUIT ERRORS
  {main()},
  error=function(cond) {
    return(geterrmessage())
  }
)
cat(output)                                                                     #RETURN OUTPUT TO PYTHON
