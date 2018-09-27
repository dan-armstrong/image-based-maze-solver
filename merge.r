merge_sort <- function(v, string_input=FALSE) {                                 #PACKAGE FUNCTION TO CATCH ERRORS
  return(tryCatch(
    {main_merge_sort(v, string_input)},
    error=function(cond) {
      return(v)
    }
  ))
}


main_merge_sort <- function(v, string_input) {                                  #SORT TWO VECTORS
  if (length(v) > 10) {update(paste('Sorting vector of length', length(v)))}
  if (length(v) > 1) {
    m <- ceiling(length(v) / 2)                                                 #SPLIT VECTORS AND RECURSE
    a <- main_merge_sort(v[1:m], string_input)
    b <- main_merge_sort(v[(m+1):length(v)], string_input)
    return(merge_vectors(a, b, string_input))
  }
  return(v)
}


merge_vectors <- function(a, b, string_input) {                                 #MERGE TWO VECTORS
  pointer_a = 1
  pointer_b = 1
  range <- length(a)+length(b)
  merged <- rep(0, range)                                                       #CREATE EMPTY MERGED VECTOR
  for (i in 1:range) {
    if (pointer_a > length(a)) {                                                #ADD LEFTOVER ITEMS TO MERGED
      merged[i] <- b[pointer_b]
      pointer_b <- pointer_b + 1
    }
    else if (pointer_b > length(b)) {                                           #ADD LEFTOVER ITEMS TO MERGED
      merged[i] <- a[pointer_a]
      pointer_a <- pointer_a + 1
    }
    else if (string_input) {                                                    #MERGE RECTANGLE STRINGS
      a_value <- prod(as.integer(strsplit(a[pointer_a], '-')[[1]][3:4]))        #SORT BY AREA OF RECTANGLES
      b_value <- prod(as.integer(strsplit(b[pointer_b], '-')[[1]][3:4]))
      if (a_value > b_value) {                                                  #ADD SMALLER ITEM TO VECTOR
        merged[i] <- a[pointer_a]
        pointer_a <- pointer_a + 1
      }
      else{
        merged[i] <- b[pointer_b]
        pointer_b <- pointer_b + 1
      }
    }
    else {                                                                      #MERGE NUMBERS
      if (a[pointer_a] < b[pointer_b]) {                                        #ADD SMALLER ITEM TO VECTOR
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
