library(RMySQL)
#return all data from actiontimes
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsAll <- dbSendQuery(mycon, "select * from actiontimes where userID = 'ID01'")
dataAll <- fetch(rs, n= -1)
dataAll
dim(dataAll)
dbDisconnect(mycon)
#return first session
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsS01 <- dbSendQuery(mycon, "SELECT * FROM  `actiontimes` WHERE sessionID =  'ID01_Session01'")
rsAction <- dbSendQuery(mycon, "SELECT distinct actionTaken FROM  `actiontimes` WHERE sessionID =  'ID01_Session01'")
rsSession <- dbSendQuery(mycon, "SELECT distinct * FROM  `actiontimes` WHERE userID =  'ID02'")
dataS01 <- fetch(rsS01, n= -1)
dataSession <- fetch(rsSession , n= -1)
dataAction <- fetch(rsAction , n= -1)
dataS01=read.csv("actiontimes.csv")
#plot
x<-c(dataS01[,4])
x_n = as.numeric(x)
x_n
x_r <- range(x_n)
x_r
y<-c(1:nrow(dataS01))
y
w_n<-c(dataSession[,4])
w_n
w_n <- as.numeric(w)
z<-c(1:nrow(dataSession))
z
plot(y,x_n,type="o")
plot(z,w_n, type="o",col="blue")
par(pch=22, col="red")
plot(y,x,main="title", sub="subtitle",  xlab="X-axis label", ylab="y-axix label") 
lines(y, x, type="l") 
rsS02 <- dbSendQuery(mycon, "SELECT * FROM  `actiontimes` WHERE sessionID =  'ID01_Session02'")
dataS02 <- fetch(rsS02, n= -1)
x<-c(dataS02[,4])
y<-c(1:nrow(dataS02))

##################################
data=read.csv("actiontimes.csv")
x<-c(data[,4])
y<-c(1:nrow(data))
plot(x,y)
length(x)
length(y)
class(x)
class(y)
plot(y,x)
r##################################

length(data1)
nrow(data1)
data1
class(data1)
dim(data1)
head(data1,n=10)
tail(data1)
head(data1[,2])
class(head(data1[,4]))
data1[,4]

# user 1 and left mouse button press
index1 = (data1[,3]== "ID01_Session01")

sum(index1 & index2)
data2=data1[index1,]
index2 = (data2[,2] == "Left mouse button pressed")
# ==name[i]

data3=data2[index2,]
head(data2,n=10)
head(data3,n=30)
dim(data3)
sum(data1[,4]== "Left mouse button pressed")
name=unique(data1[,2])
class(name)
tmp=as.matrix(data1)


as.numeric(tmp[1,1])


# for (i in 1:20)

	# {}
#

demo()
help()

x <- c(1,3,6,9,12)
y <- c(1.5,2,7,8,15)
plot(x,y)

# Example 2. Draw a plot, set a bunch of parameters.
plot(x,y, xlab="x axis", ylab="y axis", main="my plot", ylim=c(0,20), xlim=c(0,20), pch=15, col="blue")
# fit a line to the points
myline.fit <- lm(y ~ x)

# get information about the fit
summary(myline.fit)

# draw the fit line on the plot
abline(myline.fit)

# Example 3
# add some more points to the graph
x2 <- c(0.5, 3, 5, 8, 12)
y2 <- c(0.8, 1, 2, 4, 6)

points(x2, y2, pch=16, col="green")
#loop through all user 01 session and get lefb mouse button action
rs <- dbSendQuery(mycon, "select distinct sessionID from actiontimes where userID = 'ID01'")
dataSID <- fetch(rs, n= -1)
dataSID
if(dbMoreResults(mycon)){	
	rs1<-dbNextResult(con)
	data1<-fetch(rs1,n=-1)	
	rs2 <- dbSendQuery(mycon, "select distinct * from actiontimes where userID = 'data1[1]'")
	dataUID<-fetch(rs2,n=-1)	
	dataUID		
}

