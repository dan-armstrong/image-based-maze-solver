library("data.table")


input <- strsplit(as.character(commandArgs(trailingOnly = TRUE)), ' ')[[1]]
setwd(input[1])
MAZE_GRID <- data.matrix(fread(input[2]))
QUIT_FILE <- input[3]
UPDATE_FILE <- input[4]
AREA_FILE <- 'areas.csv'

main <- function() {
  get_areas <- function(x, y) {max_area(x, y, 1, count_up(x,y), 0, 0)}
  areas <- matrix(mapply(get_areas, col(MAZE_GRID), row(MAZE_GRID)), nrow=nrow(MAZE_GRID))
  write.table(areas, file = AREA_FILE, row.names = FALSE, col.names = FALSE,sep = ",")
  return(AREA_FILE)
}


update <- function(text) {
  check_quit()
  f <- file(UPDATE_FILE)
  writeLines(c(text), f)
  close(f)
}


check_quit <- function() {
  status <- readChar(QUIT_FILE, file.info(QUIT_FILE)$size)
  if (status == 'q') {stop('quit')}
}


count_up <- function(x, y) {
  if (MAZE_GRID[y,x] == 1) {return(0)}
  prev_wall <- tail(which(MAZE_GRID[1:y,x]==1),1)[1]
  if (is.na(prev_wall)) {return(y)}
  return(y-prev_wall)
}


max_area <- function(x, y, width, height, max_width, max_height) {
  if (MAZE_GRID[y, x-width+1] == 1) {return(paste(max_width,max_height,sep='-'))}
  if (x - width == 0) {return(paste(max_width,max_height,sep='-'))}
  if (height < 3) {return(paste(max_width,max_height,sep='-'))}
  if (width*height > max_width*max_height && width >= 3) {
    max_width <- width
    max_height <- height
  }
  if (count_up(x-width, y) < height) {
    return(max_area(x, y, width+1, count_up(x-width, y), max_width, max_height))
  }
  else {
    return(max_area(x, y, width+1, height, max_width, max_height))
  }
}


output <- tryCatch(
  {main()},
  error=function(cond) {
    return(geterrmessage())
  }
)
cat(output)
