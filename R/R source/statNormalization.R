#libraries
library(RMySQL)
library(Hmisc)
library(pastecs)
library(psych)
library(Rcmdr)
require(vegan)
library(car)
library(LPE)


#user01 data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTaken,a.timelineMSEC,a.durationMSEC,b.X,b.Y,b.Rel__dist_,b.Total_dist_ 
from `actiontimes` as a , `ulogdata` as b where a.originalRECNO = b.RECNO and a.actionTakenNumeric='0'")
user <- fetch(rsUser, n= -1)
dbDisconnect(mycon)
user01[1,1]

#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsData <- dbSendQuery(mycon, "select distinct userID from actiontimes")
dataUser <- fetch(rsData , n= -1)
dbDisconnect(mycon)
user01[2,]

par(mfrow=c(1,1))
par(mfrow=c(5,4))
for(i in 1:20){
	x<-subset(user,user$userID==dataUser[i,],select = c(durationMSEC,sessionID))
	sqlTemp=rep("select distinct sessionID from actiontimes where userID = '")
	sqlFull = paste(sqlTemp,dataUser[i,],"'",sep="")
	mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
	rsSessionData <- dbSendQuery(mycon,sqlFull)
	sessionData <-fetch(rsSessionData)
	dbDisconnect(mycon)
	#hist(x$durationMSEC)
	#hist(log(x$durationMSEC))
	nameTemp=rep("LogNormalizedLeftClick.png")
	nameFull = paste(dataUser[i,],nameTemp,sep="")
	png(nameFull,width = 1920, height = 1200 )
	
	par(mfrow=c(1,1))
	par(mfrow=c(5,4))	

	
	for(j in 1:10){
		y <- subset(x,x$sessionID==sessionData[j,],select = durationMSEC)		

		#hist(var1)
		hist(log(y$durationMSEC))
		
	}
	dev.off()
}



x <- sapply(user01$durationMSEC, mean, na.rm=TRUE)
summary(user01$durationMSEC)
describe(user01$durationMSEC) 
stat.desc(user01$durationMSEC) 
x <- describe.by(user01$durationMSEC, list(user01$userID),mat=TRUE)
write.table(user01, file = "SUMMARY STATISTICS BY GROUP USER ID01.csv", sep = ",", col.names = NA)

dataACtionTimes <- read.csv2('USER DATA ACTION TIMES SUMMARY ID01.csv',header=TRUE,sep=',')
head(dataACtionTimes)

user01
user01

qqnorm(user01$durationMSEC, main="text you want above plot")
qqline(user01$durationMSEC)

qqnorm(subsetSID$durationMSEC, main="text you want above plot")
qqline(subsetSID$durationMSEC)

#log transformation
logID.data <- log(user$durationMSEC)
logSID.data <- log(subsetSID$durationMSEC)
write.table(logID.data, file = "SUMMARY STATISTICS BY GROUP USER ID01 log transformed.csv", sep = ",", col.names = NA)
logID.data <- read.csv("SUMMARY STATISTICS BY GROUP USER ID01 log transformed.csv",header=TRUE)
qqnorm(logID.data$x, main="text you want above plot")
qqline(logID.data$x)

#sqrt transformation
sqrtID.data<-sqrt(user$durationMSEC)
qqnorm(sqrtID.data, main="sqrt trasnform")
qqline(sqrtID.data)

#asin transformation
asinID.data<-asin(user$durationMSEC)
qqnorm(asinID.data, main="sqrt trasnform")
qqline(asinID.data)

#logit
logitID.data<-logit(user$durationMSEC)
qqnorm(logitID.data, main="sqrt trasnform")
qqline(logitID.data)


qqnorm(logSID.data, main="text you want above plot")
qqline(logSID.data)