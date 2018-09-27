csv_file <- as.character(commandArgs(trailingOnly = TRUE))
library("data.table")
csv_file <- '/Users/danarmstrong/Desktop/Coursework/threshold.csv'
data <- data.matrix(fread(csv_file))

while (sum(data[1,]) < nrow(data)/10) {data <- data[-1,]}
while (sum(data[,1]) < ncol(data)/10) {data <- data[,-1]}
while (sum(data[nrow(data),]) < nrow(data)/10) {data <- data[-nrow(data),]}
while (sum(data[,ncol(data)]) < ncol(data)/10) {data <- data[,-ncol(data)]}

write.table(data, file = "cropped_data.csv",row.names = FALSE, col.names = FALSE,sep = ",")
#cat('done')
