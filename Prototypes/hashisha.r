CAP <- 1000

hash <- function(a, b, cap) {
  v <- a*100 + b
  x <- (a*100 + b) * 0.5 * (sqrt(5) - 1)
  return (floor(cap * (x %% 1)))
}



a <- mapply(hash, 1:1000, 1:1000, 100*100)
print(a[1:10])
frequency <- function(x) {
  sum(as.numeric(a==x)) }
print(length(a))
hist <- sapply(0:max(a), frequency)
hist[1:100]
