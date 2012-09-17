library(RMySQL)
#all users
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser <- dbSendQuery(mycon, "select distinct userID from actionlink")
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
rsNames <- dbSendQuery(mycon, "select distinct sessionID from actionlink where userID = 'ID10'")
names <- fetch(rsNames, n= -1)
class(names)
names

dim(names)
class(names)
#names_1=as.matrix(names)
#dim(names_1)

#data for user 1
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsActionTaken <- dbSendQuery(mycon, "select sessionID, Window , actionTaken, nrActionTaken from actionlink where userID = 'ID10'")
actionTaken<-fetch(rsActionTaken , n= -1)
dim(actionTaken)
class(actionTaken)
head(actionTaken$actionTaken)
#actionTaken_1 = as.matrix(actionTaken)
actionTaken
head(actionTaken)
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
	par(mfrow=c(5,2))
	

	k=1
	tmp6=rep(".pdf",length(as.vector(as.matrix(names))))
	tmp7=paste(as.vector(as.matrix(names)),tmp6,sep="")

	pdf(file=tmp7[k])
	for (i in 1:10) {		

		x<-subset(actionTaken,sessionID == names[i,],select=c(Window,actionTaken,nrActionTaken))
		tmp=as.vector(as.matrix(unique(x[1])))
		num=length(tmp)
		print(num)
		for (l in 1:num){
			print(names[i,])
			print(tmp[l])
			print("#################################################################")
			y<-subset(x,Window == tmp[l],select=c(actionTaken,nrActionTaken))
			counts <- as.vector(as.matrix(y$nrActionTaken))
			action <- as.vector(as.matrix(y$actionTaken))
			plot(1:dim(y)[1],counts,,main=names[i,],sub=tmp[l])
			numL = length(counts)
			tmp1= 1:numL
			tmp4=paste(tmp1,action,counts,sep=" ")
			legend(x="topright", legend=c(as.vector(as.matrix(tmp4))))

		}
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