library("data.table")


input <- strsplit(as.character(commandArgs(trailingOnly = TRUE)), ' ')[[1]]     #GET INPUT FROM PYTHON
setwd(input[1])                                                                 #SET CURRENT WORKING DIRECTORY
MAZE_GRID <- data.matrix(fread(input[2]))                                       #READ IN MAZE GRID AS MATRIX
QUIT_FILE <- input[3]
UPDATE_FILE <- input[4]
RECTILINEAR <- ifelse(input[5] == 'True', TRUE, FALSE)
END_POINTS <- as.integer(input[6:9])
NODE_FILE <- 'nodes.csv'
if (!RECTILINEAR) {
  RECT_GRID <- data.matrix(fread(input[10]))                                    #READ IN RECT GRID AS MATRIX
}


main <- function() {                                                            #PACKAGE FUNCTION TO CATCH ERRORS
  nodes_vector <- mapply(node_data, col(MAZE_GRID), row(MAZE_GRID))
  nodes <- matrix(nodes_vector[!is.na(nodes_vector)], byrow = TRUE, ncol=4)     #WRITE NODES TO FILE
  write.table(nodes-1, file = NODE_FILE, row.names = FALSE, col.names = FALSE,sep = ",")
  return(NODE_FILE)
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


valid_node <- function(x, y) {                                                  #RETURNS IF POINT IS A NODE
  if (MAZE_GRID[y,x] == 1) {return(FALSE)}                                      #FALSE IF WALL
  if (all(c(x, y) == END_POINTS[1:2])) {return(TRUE)}                           #TRUE IF END POINT
  if (all(c(x, y) == END_POINTS[3:4])) {return(TRUE)}

  if (RECTILINEAR) {
    nbrs_h <- 0
    nbrs_v <- 0
    if (x > 1) {nbrs_h <- nbrs_h + (1 - MAZE_GRID[y,x-1])}
    if (y > 1) {nbrs_v <- nbrs_v + (1 - MAZE_GRID[y-1,x])}
    if (x < ncol(MAZE_GRID)) {nbrs_h <- nbrs_h + (1 - MAZE_GRID[y,x+1])}
    if (y < nrow(MAZE_GRID)) {nbrs_v <- nbrs_v + (1 - MAZE_GRID[y+1,x])}
    if (nbrs_h + nbrs_v > 2) {return(TRUE)}                                     #TRUE IF JUNCTION
    if (nbrs_h == 1 && nbrs_v == 1) {return(TRUE)}                              #TRUE IF CORNER
    return(FALSE)
  }

  else {
    return(ifelse(RECT_GRID[y, x] == 2, FALSE, TRUE))                           #TRUE IF NOT IN RECTANGLE
  }
}


nbr_left <- function(x, y) {                                                    #FIND NBR TO LEFT OF NODE
  if (x == 1) {return(0)}
  pos <- x-1
  while (pos > 0) {
    if (MAZE_GRID[y, pos] == 1) {return(0)}                                     #WALL FOUND SO NO NEIGHBOUR
    if (valid_node(pos, y)) {return(pos)}
    pos <- pos-1
  }
  return(0)                                                                     #NO NEIGHBOUR
}


nbr_up <- function(x, y) {                                                      #FIND NBR ABOVE NODE
  if (y == 1) {return(0)}
  pos <- y-1
  while (pos > 0) {
    if (MAZE_GRID[pos, x] == 1) {return(0)}
    if (valid_node(x, pos)) {return(pos)}
    pos <- pos-1
  }
  return(0)
}


node_data <- function(x, y) {                                                   #RETURN VECTOR OF NODE DATA FOR POINT
  if (y == 1) {update(paste('Finding nodes',round(x/ncol(MAZE_GRID)*100),'%'))}
  if (valid_node(x, y)) {
    return(c(x, y, nbr_left(x, y), nbr_up(x, y)))
  }
  return(c(NA, NA, NA, NA))                                                     #INVALID NODE
}


output <- tryCatch(                                                             #CATCH QUIT ERRORS
  {main()},
  error=function(cond) {return(geterrmessage())}
)
cat(output)                                                                     #RETURN OUTPUT TO PYTHON
