csv_file <- as.character(commandArgs(trailingOnly = TRUE))
library("data.table")
csv_file <- '/Users/danarmstrong/Desktop/Coursework/greyscale.csv'
greyscale_grid <- data.matrix(fread(csv_file))
depth <- 256
a <- proc.time()

threshold_value <- function(hist, resolution) {
  mean_values <- hist*0:(length(hist)-1)
  print(mean_values)
  weights_fg <- cumsum(hist) / resolution
  weights_bg <- 1 - weights_fg
  means_fg <- ifelse(cumsum(hist) > 0 , cumsum(mean_values)/cumsum(hist) , 0)
  means_bg <- ifelse(sum(hist)-cumsum(hist) > 0 , cumsum(mean_values)/(sum(hist)-cumsum(hist)) , 0)
  class_variances <- weights_fg*weights_bg*(means_bg-means_fg)^2
  return(which(class_variances==max(class_variances)))
}

threshold <- function(grid, depth) {
  freq <- function(x) {sum(grid==x)}
  hist <- c(0,sapply(0:255, freq),0)
  print(hist)
  t <- threshold_value(hist, nrow(grid)*ncol(grid))
  grid <- ifelse(grid>t,0,1)
  return(grid)
}

threshold_grid <- threshold(greyscale_grid)
print(proc.time()-a)

write.table(threshold_grid, file = "threshold.csv",row.names = FALSE, col.names = FALSE,sep = ",")
print(proc.time()-a)
cat()
