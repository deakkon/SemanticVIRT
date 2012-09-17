library(RMySQL)
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')

#timeline <- dbSendQuery(mycon, "SELECT timelineMSEC FROM  `actiontimes` WHERE userID =  'ID01'")
timeline <- dbSendQuery(mycon, "SELECT actionTaken,timelineMSEC FROM  `actiontimes` WHERE sessionID =  'ID01_Session01'")
dataUser <- fetch(timeline, n= -1)
dataUser