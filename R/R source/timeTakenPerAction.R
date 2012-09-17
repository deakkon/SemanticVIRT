library(RMySQL)
#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from actiontimes")
user <- fetch(rsUser, n= -1)
user[4,]
user

#all possible actions
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActions <- dbSendQuery(mycon, "select distinct actionTaken from actiontimes")
actions <- fetch(rsActions , n= -1)
actions
actionsC <- as.vector(as.matrix(actions))
actionsC
length(actionsC)
actionsC[5]
class(actionsC)

#data for user 1
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActionTaken <- dbSendQuery(mycon, "select userID, sessionID, actionTaken, durationMSEC from actiontimes ORDER BY  `sessionID` ")
actionsTaken<-fetch(rsActionTaken , n= -1)
actionsTaken
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
		y<-subset(actionsTaken,actionTaken == actionsC[j] ,select=c(userID,sessionID,actionTaken,durationMSEC))
		#y
		tmp6=rep(".pdf")
		name = paste(actionsC[j],tmp6,sep="")
		#name
		name
		pdf(name)

		for (i in 1:20) {
			x<-subset(y,userID == user[i,],select=c(sessionID,actionTaken,durationMSEC))
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
				plot(1:length(tmp),cumsum(tmp), type="l", main=name,ylim=c(0,27000))
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