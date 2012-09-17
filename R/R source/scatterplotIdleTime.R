#libraries
library(RMySQL)
library(hexbin)

#user data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.originalRECNO,a.actionTaken,a.actionTakenNumeric,a.actionTime,a.duration,a.timeline,a.durationMSEC,a.timelineMSEC,c.`idleTime` from `actiontimes` as a, `idletimes` as c where a.originalRECNO= c.RECNO")
user01 <- fetch(rsUser01, n= -1)
user01[1,1]

#list of users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
listUser <- dbSendQuery(mycon, "select distinct userID from ulogdata")
userList <- fetch(listUser, n= -1)
par(mfrow=c(5,3))
tmp6=rep("UserScatterActionRegion.pdf")
tmp7=paste(tmp6,sep="")
tmp7
#pdf(tmp7)
jpeg(file="UserScatterActionRegion.jpeg")

par(mfrow=c(1,1))
par(mfrow=c(5,3))

for (i in 1:20){	
	x<-subset(user01 ,userID == userList[i,],select=c(timelineMSEC,idleTime))
	x
	bin<-hexbin(x$timelineMSEC, x$idleTime, xbins=100)
	bin
	part1=rep("Action Regions.jpeg")
	nameFull=paste(userList[i,],part1,sep="")
	nameFull	 	
	#cyl.f <- factor(mtcars$cyl)
	#gear.f <- factor(mtcars$factor) 
	#iplot(x$X, x$Y)
	#iplot.opt(title=nameFull,plot=iplot.cur())
	jpeg(file=nameFull)
	plot(bin, main=nameFull)
	#points(x$X, x$Y)
	dev.off()
}


