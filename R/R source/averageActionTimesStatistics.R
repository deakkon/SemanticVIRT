#libraries 
library(RMySQL)
library(plotrix)

#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from `idletimes`")
user <- fetch(rsUser, n= -1)
userc <- c(user)

#all categories
#mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
#rsCat <- dbSendQuery(mycon, "select distinct category from datahistory ")
#category <- fetch(rsCat , n= -1)
#cat <- c(category )

#sum of categories
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
dataCat <- dbSendQuery(mycon, "select userID,sum(`idletime`) as it from `idletimes` group by sessionID")
cat <- fetch(dataCat, n= -1)
cat


##loop through user->action
for (i in 1:20) {	
	#print(user[i,1])
	userData<-subset(cat ,userID == user[i,1],select=c(it))
	mv <- mean(as.numeric(userData$it))

	#print (user[i,1])
	print(mv)
	
}

