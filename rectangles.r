library("data.table")


input <- strsplit(as.character(commandArgs(trailingOnly = TRUE)), ' ')[[1]]
setwd(input[1])
source('merge.r')
MAZE_GRID <- data.matrix(fread(input[2]))
QUIT_FILE <- input[3]
UPDATE_FILE <- input[4]
RECT_FILE <- 'rectangles.csv'
RECT_SIZE <- 3                                                                  #MINIMUM DIMENSIONS OF RECTANGLE (3X3)


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


main <- function(maze_grid) {                                                   #FUNCTION PACKED TO CATCH ERRORS
  height_above <- function(x, y) {                                              #STOPS REPEATED CALCULATION OF SAME VALUES
    if (y == 1) {update(paste('Finding free space',round(x/ncol(maze_grid)*100),'%'))}
    pos <- tail(which(maze_grid[1:y, x] == 1), 1)[1]                            #ONLY NEED TO FIND EACH HEIGHT ONCE
    if (is.na(pos)) {return(y)}
    return(y - pos)
  }
                                                                                #AMOUNT OF EMPTY SPACE ABOVE EACH POINT
  height_grid <- matrix(mapply(height_above, col(maze_grid), row(maze_grid)), nrow=nrow(maze_grid))

  max_area <- function(x, y) {                                                  #GETS MAX RECT THAT CAN BE DRAWN FROM POINT
    if (y == 1) {update(paste('Calculating areas',round(x/ncol(maze_grid)*100),'%'))}
    width <- 1
    height <- height_grid[y, x]
    max_width <- 0
    max_height <- 0
    while (height >= RECT_SIZE && x - (width-1) >= 1) {                         #LOOP THROUGH VALID RECTANGLES
      if (height_grid[y, x-(width-1)] < height) {                               #REDUCE HEIGHT TO MATCH CURRENT HEIGHT
        height <- height_grid[y, x-(width-1)]
      }
      if (width*height > max_width*max_height && width >= RECT_SIZE && height >= RECT_SIZE) {
        max_width <- width                                                      #NEW MAX RECT FOUND
        max_height <- height
      }
      width <- width + 1
    }
    return(paste(max_width, max_height, sep='-'))                               #RETURN RECT DATA
  }
                                                                                #MAX RECT THAT CAN BE DRAWN FROM EACH POINT
  area_grid <- matrix(mapply(max_area, col(maze_grid), row(maze_grid)), nrow=nrow(maze_grid))

  create_vector <- function(x, y) {                                             #ADDS POSITION TO RECT DATA
    data <- as.integer(strsplit(area_grid[y, x], '-')[[1]])
    if (data[1]*data[2] > 0) {                                                  #ONLY ADD RECTANGLES WITH ANY AREA
      return(paste(x, y, data[1], data[2], sep='-'))
    }
    return(NA)
  }

  area_vector <- na.omit(mapply(create_vector, col(maze_grid), row(maze_grid))) #VECTOR OR RECT DATA
  if (length(area_vector) > 0) {
    area_vector <- merge_sort(na.omit(area_vector), TRUE)                       #SORT SO LARGEST AREAS EXPLORED FIRST
    check_quit()
  }

  expand_area <- function(data, grid) {                                         #ADD EACH RECT TO RECT GRID
    x <- data[1]
    y <- data[2]
    width <- data[3]
    height <- data[4]
    row_clear = FALSE
    col_clear = FALSE
    while (width >= RECT_SIZE && height >= RECT_SIZE && (!row_clear || !col_clear)) {#REMOVE OVERLAPS
      if (!row_clear) {                                                         #TRIM ROWS
        if (all(grid[y-(height-1), (x-(width-1)):x] == 0)) {row_clear = TRUE}
        else {height <- height - 1}
      }
      if (!col_clear) {                                                         #TRIM COLS
        if (all(grid[(y-(height-1)):y, x-(width-1)] == 0)) {col_clear = TRUE}
        else {width <- width - 1}
      }
    }
    if (width >= RECT_SIZE && height >= RECT_SIZE) {                            #IF RECTANGLE STILL LARGE ENOUGH
      grid[(y-(height-1)), (x-(width-1)):x] <- 1                                #SET PERIMETER TO 1'S
      grid[y, (x-(width-1)):x] <- 1
      grid[(y-(height-1)+1):(y-1), x-(width-1)] <- 1
      grid[(y-(height-1)+1):(y-1), x] <- 1
      grid[(y-(height-1)+1):(y-1), (x-(width-1)+1):(x-1)] <- 2                  #SET CENTER TO 2'S
    }
    return(grid)
  }

  c <- 1
  rect_grid <- matrix(0, nrow=nrow(maze_grid), ncol=ncol(maze_grid))            #CREATE EMPTY RECT GRID
  for (row in area_vector) {
    update(paste('Finding rectangles',round(c/length(area_vector)*100),'%'))
    area_data <- as.integer(strsplit(row, '-')[[1]])
    if (rect_grid[area_data[2], area_data[1]] == 0) {                           #IF NOT PART OF RECT ALREADY
      rect_grid <- expand_area(area_data, rect_grid)
    }
    c <- c + 1
  }

  write.table(rect_grid, file = RECT_FILE,row.names = FALSE, col.names = FALSE,sep = ",")
  return(RECT_FILE)
}


output <- tryCatch(                                                             #CATCH QUIT ERRORS
  {main(MAZE_GRID)},
  error=function(cond) {return(geterrmessage())}
)
cat(output)                                                                     #RETURN OUTPUT TO PYTHON
