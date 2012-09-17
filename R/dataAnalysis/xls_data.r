require(xlsx)
res<-read.xlsx("ID01_actionDuration.xlsx",1,header="false")
res[,1]
y_n = nrow(res[1])
y_n
actionTaken <- res[2]

par(mfrow=c(1,1))

par(mfrow=c(5,2))

for (i in 1:10)	{
	print(i)
	
	#dev.print()
	res<-read.xlsx("ID01_actionDuration.xlsx",i,header="false",colIndex=1,rowIndex=NULL)
	y_n = nrow(res)
	#windows()
	#plot(res,1:y_n,type="l")

	plot(1:y_n,res[,1], type="l")
	#par(mfrow=c(2,2))

	#pdf(file="histogram.pdf")
	#dev.off() 
	}
