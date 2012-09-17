library(RMySQL)
#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from idleTimes")
user <- fetch(rsUser, n= -1)
user[4,]
user

#all possible actions
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActions <- dbSendQuery(mycon, "select distinct sessionID from idleTimes")
actions <- fetch(rsActions , n= -1)
actions

#data for user 1
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActionTaken <- dbSendQuery(mycon, "SELECT userID,sessionID, sum(idleTime) as idleTime FROM `idleTimes` group by sessionID")
actionsTaken<-fetch(rsActionTaken, n= -1)
actionsTaken
session = as.vector(as.matrix(actionsTaken[1]))
idleTime = as.vector(as.matrix(actionsTaken[2]))
cumsum(idleTime)
plot(1:length(idleTime),cumsum(idleTime), type="l", main=name,ylim=c(0,10000000))
class(session)
length(actionsTaken[2])

plot(session,idleTime)
dim(actionsTaken)
class(actionsTaken)
head(actionsTaken$actionTaken)
#actionTaken_1 = as.matrix(actionTaken)
actionTaken[,1]
actionTaken[,2]
nrow(actionTaken)
class(actionTaken)

###########################################testing phaze
x.df <- data.frame(actionTaken)
x.df
names(x.df)
x<-subset(actionTaken,sessionID == "ID01_Session02",select=c(actionTaken))
#x<-c(subset(actionTaken,sessionID == "ID01_Session01",select=c(actionTaken)))
class(x)
#hist(x)



############################################

#loop for each session plot out the data for user 1 and that session
#so, my question is how to extracht data for names_1[i] (the session name) from actionTaken (all actions throughut session for user 01)
#plot data for each session
	
	par(mfrow=c(1,1))
	par(mfrow=c(4,5))

	#for (j in 1:length(actionsC)){

		print(j)
		actionsC[j]
		i=1
		#y<-subset(actionsTaken,userID == actionsC[j] ,select=c(userID,sessionID,actionTaken,durationMSEC))
		#y
		tmp6=rep(".pdf")
		name = paste(user[i,],tmp6,sep="")
		#name
		name
		pdf(name)

		for (i in 1:20) {
			x<-subset(actionsTaken,userID == user[i,] ,select=c(userID,sessionID,idleTime))
			x
			#dim(x[1])
			tmp=as.vector(as.matrix(x[3]))
			tmp
			tmp1=as.vector(as.matrix(x[1]))
			tmp1
			length(tmp)
			#tmp[5]
			#plot(1:length(tmp),cumsum(tmp), type="l", main=name,ylim=c(0,00))
			#print(i)	
			
			#print(user[i,])
			if(i==1)
				plot(1:length(tmp),cumsum(tmp), type="l", main=name,ylim=c(0,14000000))
			else
				points(1:length(tmp),cumsum(tmp), type="l", main=name, col=i)	
			#user = c(user[i])
			#col = c(i)
		}
		#legend(1, 5500000, user, cex=0.8, col=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), pch=21:22, lty=1:2)		
		dev.off()
	#}

	



pdf()
plot(1:dim(x)[1],action,"l",ylab=tmp)


#dim(x)
#class(x[1,1])
tmp=as.vector(as.matrix(unique(x)))
num=length(tmp)
action=numeric(dim(x)[1])
for(i in 1:num)
	{index= (x[,1]==tmp[i])
	 action[index]=i
	}
plot(1:dim(x)[1],action,"l")