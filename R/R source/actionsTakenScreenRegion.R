#libraries
library(RMySQL)
library(hexbin)

#user data
mycon <- dbConnect(MySQL(), user='root',dbname='test',host='localhost',password='')
rsUser01 <- dbSendQuery(mycon, "select a.userID,a.sessionID,a.actionTaken,a.timelineMSEC,a.durationMSEC,b.X,b.Y,b.Rel__dist_,b.Total_dist_ from `actiontimes` as a , `ulogdata` as b where a.originalRECNO = b.RECNO")
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

for (i in 17:20){	
	x<-subset(user01 ,userID == userList[i,],select=c(X,Y))
	x
	bin<-hexbin(x$X, x$Y, xbins=100)
	bin
	part1=rep("Action Regions.jpeg")
	nameFull=paste(userList[i,],part1,sep="")
	nameFull	 	
	cyl.f <- factor(mtcars$cyl)
	gear.f <- factor(mtcars$factor) 
	iplot(x$X, x$Y)
	iplot.opt(title=nameFull,plot=iplot.cur())
	#jpeg(file=nameFull)
	#plot(bin, main=nameFull)#,col=rgb(0,100,0,50,maxColorValue=255), pch=16)
	#points(x$X, x$Y)
	#dev.off()
}




## volcano  ## 87 x 61 matrix
#wireframe(volcano, shade = TRUE,
 #         aspect = c(61/87, 0.4),
  #        light.source = c(10,0,10))

#g <- expand.grid(x = 1:10, y = 5:15, gr = 1:2)
#g$z <- log((g$x^g$g + g$y^2) * g$gr)
#wireframe(z ~ x * y, data = g, groups = gr,
 #         scales = list(arrows = FALSE),
  #        drape = TRUE, colorkey = TRUE,
   #       screen = list(z = 30, x = -60))

#cloud(Sepal.Length ~ Petal.Length * Petal.Width | Species, data = iris,
 #     screen = list(x = -90, y = 70), distance = .4, zoom = .6)