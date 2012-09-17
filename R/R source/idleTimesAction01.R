#libraries
library(RMySQL)
library(rgl)
library(scatterplot3d)
library(Rcmdr)

#user 1 session 1 data
#mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
#rsUser <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTaken,a.timelineMSEC,a.durationMSEC,b.X,b.Y,b.Rel__dist_,b.Total_dist_ from `actiontimes` as a , `ulogdata` as b where a.originalRECNO = b.RECNO and a.userID='ID04'")
#user1 <- fetch(rsUser, n= -1)
#class(user1$Y)
#pdf("scatterplot2.pdf") 
#x<-as.numeric(user1$X)
#y<-as.numeric(user1$Y)
#scatter3d(x,y,user1$timeline,type="h")
#dev.off()
#plot3d(user1$timeline,user1$X,user1$Y)

##############################################################################
#database connection
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
#distinct sessions
rsSessionsU01 <- dbSendQuery(mycon, "select distinct userID from actiontimes")
sessionU01 <-fetch(rsSessionsU01)
sessionU01[2,]

#user01 data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select idletimes.userID,idletimes.sessionID,idletimes.message,idletimes.messageNumerical,idletimes.idletime,actiontimes.timelineMSEC from idletimes, actiontimes 
						where idletimes.RECNO=actiontimes.originalRECNO")
user01 <- fetch(rsUser01, n= -1)
user01[1,1]

#plot loop

#scatter3d
#for (i in 1:10){

#	userSubset<-subset(user01,sessionID == sessionU01[i,],select=c(timelineMSEC,X,Y))
#	userSubset
#	x<-as.numeric(userSubset$X)
#	y<-as.numeric(userSubset$Y)
#	scatter3d(x,y,userSubset$timeline,xlim = c(0,1280), ylim = c(0,1024), zlim=c(0,1800000),type="h",main=sessionU01[i,],sub=sessionU01[i,])	
#}

#scatterplot3d
	par(mfrow=c(1,1))
	par(mfrow=c(5,4))
	#jpeg(file="Active screen regions.jpeg")

for (i in 1:20){

	userSubset<-subset(user01,userID == sessionU01[i,],select=c(idletime,messageNumerical,timelineMSEC))
	userSubset
	x<-as.numeric(userSubset$X)
	y<-as.numeric(userSubset$Y)
	scatterplot3d(userSubset$messageNumerical,userSubset$idletime,userSubset$timelineMSEC, pch=16, highlight.3d=TRUE, type="h", main=sessionU01[i,],xlab="Action",ylab="idletime",zlab="timeline")
	#scatter3d(x,userSubset$timeline,y,xlim = c(0,1280), zlim = c(0,1024), ylim=c(0,1800000),type="h",main=sessionU01[i,],sub=sessionU01[i,])	
	#part1=rep(".png")
	#nameFull=paste(sessionU01[i,],part1,sep="")
	#nameFull	
	#rgl.snapshot( nameFull, fmt="png", top=TRUE )

}

dev.off()

