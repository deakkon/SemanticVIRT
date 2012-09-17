#libraries 
library(RMySQL)
library(plotrix)

#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from datahistory ")
user <- fetch(rsUser, n= -1)
userc <- c(user)

#all categories
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsCat <- dbSendQuery(mycon, "select distinct category from datahistory ")
category <- fetch(rsCat , n= -1)
cat <- c(category )

#sum of categories
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
dataCat <- dbSendQuery(mycon, "select count(*) as count, `category`, userID from datahistory group by userID, `category`")
cat <- fetch(dataCat, n= -1)
cat


##loop through user->action
for (i in 1:20) {	
	print(user[i,1])
	userData<-subset(cat ,userID == user[i,1],select=c(sessionID,actionTaken,numberTimes))
	for(j in 1:6){
		#print(j)
		#print(user[i,1])
		#print(actions[j,1])
		actionData<-subset(userData,actionTaken== actions[j,1],select=c(sessionID,actionTaken,numberTimes))
		#print(mean(actionData[3]))
		results[j,i]<-mean(actionData[3])
	}
	linksData<-subset(visitedLinks,userID == user[i,1],select=c(sessionID,nrLinksVisited))
	results[7,i]<-mean(linksData[2])

	
}

