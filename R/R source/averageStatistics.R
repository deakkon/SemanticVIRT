allData<-read.csv("actiontimesRelativeDistanceVectorSpeedAllData.csv",header=TRUE)
#allData<-read.csv("sessionUserStatisticalData.csv",header=TRUE)

#distinct users from actiontimes
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUsers <- dbSendQuery(mycon, "select distinct userID from actiontimes")
users <-fetch(rsUsers)
#users[1,]
dbDisconnect(mycon)

#distinct action taken
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsAT <- dbSendQuery(mycon, "select distinct(`actionTakenNumeric`) from actiontimes")
at <-fetch(rsAT)
at[1,]
dbDisconnect(mycon)

	#create plot
	#yrange <- c(1:10)
	#xrange <- c(1:10) 
	#plot(xrange,yrange, type="n", xlab="Session", ylab="X position" ) 


for (i in 1:20){

	#users[i,]
	userData<-subset(allData,userID==users[i,])

	#user sessions
	sqlTemp=rep("select distinct sessionID from actiontimes where userID = '")
	sqlFull = paste(sqlTemp,users[i,],"'",sep="")
	mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
	rsSessionData <- dbSendQuery(mycon,sqlFull)
	sessionData <-fetch(rsSessionData)
	dbDisconnect(mycon)

	#for(j in 1:10){
		sessionUserData<-subset(userData,sessionID==sessionData[j,])
		#session based statistics standard deviation
		x0<-sessionData[j,]
		x11<-mean(sessionUserData$durationMSEC)
		x1<-sd(sessionUserData$durationMSEC)
		x2<-sd(sessionUserData$X)
		x12<-mean(sessionUserData$x)		
		x3<-sd(sessionUserData$Y)
		x13<-mean(sessionUserData$Y)
		x4<-sd(sessionUserData$Rel__dist_)
		x14<-mean(sessionUserData$Rel__dist_)
		x5<-sd(sessionUserData$Total_dist_)
		x15<-mean(sessionUserData$Total_dist_)
		x6<-sd(as.numeric(sessionUserData$total_vx))
		x16<-mean(as.numeric(sessionUserData$total_vx))
		x7<-sd(as.numeric(sessionUserData$total_vy))
		x17<-mean(as.numeric(sessionUserData$total_vy))
		x8<-sd(as.numeric(sessionUserData$rel_vx))
		x18<-mean(as.numeric(sessionUserData$rel_vx))
		x9<-sd(as.numeric(sessionUserData$rel_vy))
		x19<-mean(as.numeric(sessionUserData$rel_vy))
		x10<-users[i,]

		#mean
		x <- cbind (x10,x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,"Mean Values",x11,x12,x13,x14,x15,x16,x17,x18,x19)
		write(x,file="sessionUserStatisticalDataAll.txt",append=TRUE,ncolumns=11)
	#}
	

	y0<-users[i,]
	y1<-sd(userData$durationMSEC)
	y11<-mean(userData$durationMSEC)
	y2<-sd(userData$X)
	y12<-mean(userData$X)
	y3<-sd(userData$Y)
	y13<-mean(userData$Y)
	y4<-sd(userData$Rel__dist_)
	y14<-mean(userData$Rel__dist_)
	y5<-sd(userData$Total_dist_)
	y15<-mean(userData$Total_dist_)
	y6<-sd(as.numeric(userData$total_vx))
	y16<-mean(as.numeric(userData$total_vx))
	y7<-sd(as.numeric(userData$total_vy))
	y17<-mean(as.numeric(userData$total_vy))
	y8<-sd(as.numeric(userData$rel_vx))
	y18<-mean(as.numeric(userData$rel_vx))
	y9<-sd(as.numeric(userData$rel_vy))
	y19<-mean(as.numeric(userData$rel_vy))
	y <- cbind (y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,"Mean Values",y11,y12,y13,y14,y15,y16,y17,y18,y19)
	write(y,file="userStatisticalDataAll.txt",append=TRUE,ncolumns=10)

	#ploting
	#sessionStatData<-subset(plotData,SessionID==sessionData[j,])
	#plotData <- subset(sessionAnalysisData,userID==users[i,])

	# get the range for the x and y axis 

	#line(c(1:10),plotData$X)

	#colors <- rainbow(20) 
	#linetype <- c(1:20) 
	#plotchar <- seq(18,18+ntrees,1)

}

#plot





