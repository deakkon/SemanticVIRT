library(RMySQL)
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')

rsUser01 <- dbSendQuery(mycon, "SELECT * FROM  `actiontimes` WHERE userID =  'ID01'")
dataUser <- fetch(rsUser01 , n= -1)
dataUser

rsAction <- dbSendQuery(mycon, "SELECT distinct actionTaken FROM  `actiontimes` WHERE sessionID =  'ID01_Session01'")
dataAction <- fetch(rsAction , n= -1)

rsSession <- dbSendQuery(mycon, "SELECT distinct sessionID FROM  `actiontimes` WHERE userID =  'ID01'")
dataSession <- fetch(rsSession , n= -1)
index <- dataSession[,1]
length(index)
dataSession[i,1]

for (i in length(index)) {
	x_temp <- dataSession[i,1]
	x_temp
}

write.50 <- subset(dataAction , actionTaken == "Mouse wheel")
write.50