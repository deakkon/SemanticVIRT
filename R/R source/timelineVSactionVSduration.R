#libraries
library(RMySQL)
library(rgl)
library(scatterplot3d)
library(Rcmdr)

#user 1 session 1 data
#mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
#rsUser <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTakenNumeric,a.durationMSEC,a.timelineMSEC from `actiontimes`")
#user1 <- fetch(rsUser, n= -1)
#class(user1$Y)
#pdf("scatterplot2.pdf") 
#x<-as.numeric(user1$X)
#y<-as.numeric(user1$Y)
#scatter3d(x,y,user1$timeline,type="h")
#dev.off()
#plot3d(user1$timeline,user1$X,user1$Y)

##############################################################################
#distinct sessions
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsSessionsU01 <- dbSendQuery(mycon, "select distinct sessionID from actiontimes where userID = 'ID20'")
sessionU01 <-fetch(rsSessionsU01)
sessionU01[2,]
dbDisconnect(mycon)


#user data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTakenNumeric,a.durationMSEC,a.timelineMSEC from `actiontimes` as a where a.userID='ID20'")
user01 <- fetch(rsUser01, n= -1)
user01[1,1]
dbDisconnect(mycon)

#plot loop

#scatter3d
	par(mfrow=c(1,1))
	par(mfrow=c(5,4))
	#jpeg(file="Active screen regions.jpeg")


for (i in 1:10){

	userSubset<-subset(user01,sessionID == sessionU01[i,],select=c(actionTakenNumeric,durationMSEC,timelineMSEC))
	userSubset
	x<-as.numeric(userSubset$X)
	y<-as.numeric(userSubset$Y)
	scatterplot3d(userSubset$durationMSEC,userSubset$timelineMSEC,userSubset$actionTakenNumeric, pch=16, highlight.3d=TRUE, type="h", main="Active screen regions per user")
	#scatter3d(userSubset$durationMSEC,userSubset$timelineMSEC,userSubset$actionTakenNumeric,xlim = c(0,290000), zlim = c(0,5), ylim=c(0,1800000),type="h",main=sessionU01[i,],sub=sessionU01[i,],xlab="Duration", ylab="Timeline", zlab="Action")	
	#part1=rep(".png")
	#nameFull=paste(sessionU01[i,],part1,sep="")
	#nameFull	
	#rgl.snapshot( nameFull, fmt="png", top=TRUE )

}

