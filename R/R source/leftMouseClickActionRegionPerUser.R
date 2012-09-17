
#libraries
library(RMySQL)
library(rgl)
library(scatterplot3d)
library(Rcmdr)
library(hexbin)
library(rgl)

##############################################################################
#distinct users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsSessionsU01 <- dbSendQuery(mycon, "select distinct userID from actiontimes")
sessionU01 <-fetch(rsSessionsU01)
sessionU01[1,]
dbDisconnect(mycon)


#user data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTaken,a.actionTakenNumeric,a.durationMSEC,a.timelineMSEC, b.X, b.Y from `actiontimes` as a, ulogdata as b where a.actionTakenNumeric='0' and a.originalRECNO = b.RECNO")
user01 <- fetch(rsUser01, n= -1)
user01[1,1]
dbDisconnect(mycon)

#plot loop
	par(mfrow=c(1,1))
	par(mfrow=c(5,4))
	#jpeg(file="LeftClickRegionAction")
#scatter3d
for (i in 1:20){

	userSubset<-subset(user01,userID == sessionU01[i,],select=c(X,Y,timelineMSEC))
	userSubset
	part1=rep("Action Regions.jpeg")
	nameFull=paste(userList[i,],part1,sep="")
	
	#bin<-hexbin(userSubset$timelineMSEC,userSubset$durationMSEC, xbins=50) 
	#plot(bin, main="Hexagonal Binning")
	#scatterplot3d(userSubset$X,userSubset$Y,userSubset$timelineMSEC, pch=16, highlight.3d=TRUE, type="h", main="3D Scatterplot")
	s3d <-scatterplot3d(userSubset$X,userSubset$Y,userSubset$timelineMSEC, pch=16, highlight.3d=TRUE, type="h", main="Left mouse button activity areas")
	fit <- lm(userSubset$timelineMSEC ~ userSubset$X+userSubset$Y) 
	s3d$plane3d(fit)
	
}
#dev.off()

