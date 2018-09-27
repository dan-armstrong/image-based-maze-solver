source('/Users/danarmstrong/Desktop/Coursework/merge.r')


orientation <- function(a, b, c) {
  value = (c[1]-b[1]) * (b[2]-a[2]) - (b[1]-a[1]) * (c[2]-b[2])
  if (value == 0) {return(0)}
  return(ifelse(value<0, -1, 1))
}

convex_hull <- function(positions) {
  points <- data.frame(x=positions[,1],
                       y=positions[,2],
                       angle=numeric(nrow(positions)))
  max_y <- max(points$y)
  bottom_points <- subset(points, y == max_y)
  min_x <- min(bottom_points$x)
  start_index <- which.min(bottom_points$x)
  points <- points[-start_index,]
  print(points[1,]$angle)
  merge_sort(points)
}

point <- setRefClass("point",
    fields = list(x = "numeric", y = "numeric",
                  orientation = "numeric", angle = "numeric"))

a <- matrix(c(1,2,3,4,5,6,7,8,9,10,5,10), ncol=2, byrow = TRUE)
print(a)
convex_hull(a)
