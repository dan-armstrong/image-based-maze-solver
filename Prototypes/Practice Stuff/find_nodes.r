fileName <- as.character(commandArgs(trailingOnly = TRUE))
library("data.table")
fileName <- "/Users/danarmstrong/Desktop/Coursework/image_data.csv"
imgData <- data.matrix(fread(fileName))
crop <- function(data) {
  while (sum(data[1,]) < nrow(data)/2) {data <- data[-1,]}
  while (sum(data[,1]) < ncol(data)/2) {data <- data[,-1]}
  while (sum(data[nrow(data),]) < nrow(data)/2) {data <- data[-nrow(data),]}
  while (sum(data[,ncol(data)]) < ncol(data)/2) {data <- data[,-ncol(data)]}
  return(data)
}
#WALL LENGTHS CHANGES ANALYSIS

dimensions <- function(data) {
  f<-file("update.txt")
  width <- ncol(data)
  height <- nrow(data)
  cellSizes <- c()
  prevWallPos <- 0
  prevBlackCount <- 0

  for (x in 1:width) {
    blackCount <- sum(data[,x])
    if (blackCount > prevBlackCount*1.25) {
      cellSizes <- c(cellSizes, x - prevWallPos)
      prevWallPos <- x
      data[,x] = 2;
    }
    prevBlackCount <- blackCount
    writeLines(c('D', round((x/width)*100)), f)
  }

  avgCellSize <- quantile(cellSizes, .33)[[1]]
  wallSize <- width - (prevWallPos-1)
  dimX <- round((width - wallSize)/avgCellSize)
  dimY <- round((height - wallSize)/avgCellSize)
  writeLines(c('D', 100), f)
  close(f)
  return(c(dimX, dimY, avgCellSize))
}

maze <- function(data, dimX, dimY, cellSize) {
  f<-file("update.txt")
  maze <- matrix(0,nrow=dimY*2+1,ncol=dimX*2+1)

  for (x in 1:dimX) {
    for (y in 1:dimY) {
      cellMinX <- round((x-1) * cellSize)+1
      cellMidX <- round((x-0.5) * cellSize)+1
      cellMinY <- round((y-1) * cellSize)+1
      cellMidY <- round((y-0.5) * cellSize)+1

      if (sum(data[cellMidY, max(cellMinX-1,1):(cellMinX+1)]) > 0) {
        maze[(2*y-1):(2*y+1),(2*x-1)] <- 1
      }
      if (sum(data[max(cellMinY-1,1):(cellMinY+1), cellMidX]) > 0) {
        maze[(2*y-1),(2*x-1):(2*x+1)] <- 1
      }

      if (x == dimX) {
        cellMaxX <- round((x) * cellSize)+1
        if (sum(data[cellMidY, (cellMaxX-1):min(cellMaxX+1,ncol(data))]) > 0) {
          maze[(2*y-1):(2*y+1),(2*x+1)] <- 1
        }
      }
      if (y == dimY) {
        cellMaxY <- round((y) * cellSize)+1
        if (sum(data[(cellMaxY-1):min(cellMaxY+1,nrow(data)), cellMidX]) > 0) {
          maze[(2*y+1),(2*x-1):(2*x+1)] <- 1
        }
      }
    }
    writeLines(c('M', round((x/dimX)*100)), f)
  }


  writeLines(c('M', 100), f)
  close(f)
  return(maze)
}

validNode <- function(data, x, y) {
  if (data[y,x] == 0){
    if ((x == 1) | (y == 1) | (x == ncol(data)) | (y == nrow(data))){
      return(TRUE)
    }
    else if (sum(data[y-1,x], data[y+1,x], data[y,x-1], data[y,x+1]) != 2) {
      return(TRUE)
    }
    else if (data[y-1,x] != data[y+1,x]) {
      return(TRUE)
    }
  }
  return(FALSE)
}

nodes <- function(data){
  f<-file("update.txt")
  positions <- c()
  ends <- c()

  for (x in 1:ncol(data)) {
    for (y in 1:nrow(data)) {
      if (validNode(data, x, y)) {
        pos <- c(x-1, y-1)
        nbrs <- c()
        if (x != 1) {
          nbrX <- x-1
          if (data[y,nbrX] == 0) {
            while (validNode(data, nbrX, y) == FALSE) {nbrX <- nbrX-1}
            nbrs <- c(nbrs, nbrX-1, y-1)
          }
        }
        if (y != 1) {
          nbrY <- y-1
          if (data[nbrY,x] == 0) {
            while (validNode(data, x, nbrY) == FALSE) {nbrY <- nbrY-1}
            nbrs <- c(nbrs, x-1, nbrY-1)
          }
        }
        if ((x == 1) | (y == 1) | (x == ncol(data)) | (y == nrow(data))){
          ends <- c(ends, paste(pos, collapse=' '))
        }
        positions <- c(positions, paste(c(pos, nbrs), collapse=' '))
      }
    }
    writeLines(c('N', round((x/ncol(data))*100)), f)
  }

  writeLines(c('N', 100), f)
  close(f)
  return(paste(c(ends, positions), collapse='\n'))
}

croppedData <- crop(imgData)
dims <- dimensions(croppedData)
mazeData <- maze(croppedData, dims[1], dims[2], dims[3])
write.table(mazeData, file = "maze_data.csv",row.names = FALSE, col.names = FALSE,sep = ",")
nodes <- nodes(mazeData)
cat(nodes)
a <- 'section_density <- function(x, y) {
  if (x %% 2 == 0) {range_x <- :}
  else {range_x <- :((x-1)*cell_width+wall_width)}
  if (x %% 2 == 0) {range_y <- ((y-1)*cell_height+wall_height):(y*cell_height)}
  else {range_y <- ((y-1)*cell_height):((y-1)*cell_height+wall_height)}
  section <- cropped_grid[range_x,range_y]
  return (sum(section)/(range_x*range_y))
}

maze_grid <- matrix(0, nrow=(dimensions_y*2+1), ncol=(dimensions_x*2+1))

position_x <- structure_matrix[1][1]
position_y <- structure_vect[2]
maze_width <- structure_vect[3]
maze_height <- structure_vect[4]
cell_width <- structure_vect[5]
cell_height <- structure_vect[6]
wall_width <- structure_vect[7]
wall_height <- structure_vect[8]
dimensions_x <- ((maze_width-wall_width)/cell_width)                          #CALCULATE TOTAL NUMBER OF ROWS & COLUMNS IN MAZE
dimensions_y <- ((maze_height-wall_height)/cell_height)
cropped_grid <- threshold_grid[position_y:(position_y+maze_height-1),         #CROP THRESHOLD GRID TO REMOVE EXCESS INFORMATION
                               position_x:(position_x+maze_width-1)]
maze_grid <- matrix(0, nrow=(dimensions_y*2+1), ncol=(dimensions_x*2+1))
section_density <- function(x, y) {
  if (x %% 2 == 0) {range_x <- ((x-1)*cell_width+wall_width):(x*cell_width)}
  else {range_x <- ((x-1)*cell_width):((x-1)*cell_width+wall_width)}
  if (x %% 2 == 0) {range_y <- ((y-1)*cell_height+wall_height):(y*cell_height)}
  else {range_y <- ((y-1)*cell_height):((y-1)*cell_height+wall_height)}
  section <- cropped_grid[range_x,range_y]
  return (sum(section)/(range_x*range_y))
}

maze_grid <- matrix(mapply(section_density, col(1), row(1)), nrow=nrow(1))'
