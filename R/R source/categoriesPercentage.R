#libraries 
library(RMySQL)
library(plotrix)
library(ggplot2)


#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from categoriessum")
user <- fetch(rsUser, n= -1)
userc <- c(user)

#all categories
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsCat <- dbSendQuery(mycon, "select distinct category from categoriessum")
category <- fetch(rsCat , n= -1)
cat <- c(as.vector(category)
cat

#number of visited instances across categories per user
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
sumCat <- dbSendQuery(mycon, "SELECT userID,SUM(count) as sumCount FROM categoriessum group by userID")
sum <- fetch(sumCat , n= -1)
sum

#all data from categoriessum to loop first user then action
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
dataCat <- dbSendQuery(mycon, "SELECT * FROM categoriessum order by sessionID")
allData <- fetch(dataCat, n= -1)
allData 

#create matrix to store percentages
mdat <- matrix(nrow = 23, ncol=20); mdat
mcol <- matrix(nrow=23, ncol=2);mcol
#create colors
col <- colors()

##loop through user->action
for (i in 1:20) {	
	print(user[i,1])
	userData<-subset(allData ,userID == user[i,1],select=c(userID,sessionID,category,count))
	userData
	for(j in 1:nrow(category)){
		#print(j)
		#print(user[i,1])
		#print(actions[j,1])
		#print(category[j,1])
		actionData<-subset(userData,category == cat[j,1],select=c(userID,sessionID,category,count))
		actionData
		#print(sum(as.numeric(actionData$count)))
		#print(sum$sumCount[i])
		percentage <- (sum(as.numeric(actionData$count)) / sum$sumCount[i] ) * 100
		percentage 
		mdat[j,i]<-percentage 
		#print(mean(actionData[3]))
		#results[j,i]<-mean(actionData[3])
		mcol[j,1]<- cat[j,1];
		mcol[j,2]<-col[j*28]
		#print(colors())
		
	}
	#linksData<-subset(visitedLinks,userID == user[i,1],select=c(sessionID,nrLinksVisited))
	#results[7,i]<-mean(linksData[2])	
}
dimnames(mdat)<-c(as.vector(category),as.vector(user))
barplot(mdat,main="Category visit structure",xlab="USER",ylab="Structure of visit",col=c(mcol[,2]),xlim=c(1,30))
#legend(25,100,c(category[,1]),cex=0.6)
legend(25,100,c(mcol[,1]),cex=1,fill=c(mcol[,2]))

