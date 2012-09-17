#libraries
library(RMySQL)
library(rgl)
library(scatterplot3d)
#library(Rcmdr)
library(hexbin)

##############################################################################
#distinct users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsSessionsU01 <- dbSendQuery(mycon, "select distinct userID from actiontimes")
sessionU01 <-fetch(rsSessionsU01)
sessionU01[1,]
dbDisconnect(mycon)


#user data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTakenNumeric,a.durationMSEC,a.timelineMSEC from `actiontimes` as a where a.actionTakenNumeric='0'")
user01 <- fetch(rsUser01, n= -1)
user01[1,1]
dbDisconnect(mycon)

#plot loop

#scatter3d
for (i in 1:10){

	userSubset<-subset(user01,userID == sessionU01[i,],select=c(durationMSEC,timelineMSEC,actionTakenNumeric))
	userSubset
	part1=rep("Action Regions.jpeg")
	nameFull=paste(userList[i,],part1,sep="")
	jpeg(file=nameFull)
	#scatterplot3d(userSubset$timelineMSEC,userSubset$actionTakenNumeric,userSubset$durationMSEC, pch=16, highlight.3d=TRUE, type="h", main="3D Scatterplot")
	#bin<-hexbin(userSubset$timelineMSEC,userSubset$durationMSEC, xbins=50) 
	#plot(bin, main="Hexagonal Binning")
	dev.off()
}