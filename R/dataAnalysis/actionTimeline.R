library(RMySQL)
#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from actiontimes")
user <- fetch(rsUser, n= -1)
user[4,]
user

#all possible actions
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActions <- dbSendQuery(mycon, "select distinct actionTaken from actionsession")
actions <- fetch(rsActions , n= -1)
actions
actionsC <- c(actions)
actionsC

#session names for user 1
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsNames <- dbSendQuery(mycon, "select distinct sessionID from actiontimes where userID = 'ID10'")
names <- fetch(rsNames, n= -1)
class(names)
names[4,]
namesDF[1,]

dim(names)
class(names)
#names_1=as.matrix(names)
#dim(names_1)

#data for user 1
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActionTaken <- dbSendQuery(mycon, "select sessionID, actionTaken,timelineMSEC from actiontimes where userID = 'ID10'")
actionTaken<-fetch(rsActionTaken , n= -1)
dim(actionTaken)
class(actionTaken)
head(actionTaken$actionTaken)
#actionTaken_1 = as.matrix(actionTaken)
actionTaken[,1]
nrow(actionTaken)
class(actionTaken)


#loop for each session plot out the data for user 1 and that session
#so, my question is how to extracht data for names_1[i] (the session name) from actionTaken (all actions throughut session for user 01)
#plot data for each session
	
	par(mfrow=c(1,1))
	par(mfrow=c(5,2))
	

	k=1
	tmp6=rep(".pdf",length(as.vector(as.matrix(names))))
	tmp7=paste(as.vector(as.matrix(names)),tmp6,sep="")

	pdf(file=tmp7[k])
	for (i in 1:10) {	

		x<-subset(actionTaken,sessionID == names[i,],select=c(actionTaken,timelineMSEC))
		tmp=as.vector(as.matrix(unique(x[1])))
		num=length(tmp)
		action=numeric(dim(x)[1])
		for(j in 1:num)
			{
			index= (x[,1]==tmp[j])
			action[index]=j
			}
		
		#plot(1:dim(x)[2],x[2],"p",xlab=tmp)
		temp6=as.vector(as.matrix(x[2]))
		plot(1:length(temp6),temp6,main=names[i,])
		#tmp1=1:num
		#tmp2=rep("=",num)
		#tmp3=as.vector(as.matrix(x[2]))
		#tmp4=paste(tmp1,tmp2,tmp,tmp3,sep=" ")
		#legend(130,0.5,tmp4)
	}
	dev.off()



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