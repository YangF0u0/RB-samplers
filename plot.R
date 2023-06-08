## plot for RB-AR

out <- read.csv("out.csv")

hist(out$non, breaks=10, col=rgb(1,0,0,0.3), xlab="theta", ylim = c(0,5),
     ylab="density", main="distribution of theta_hat",probability = T )
hist(out$RB, breaks=10, col=rgb(0,0,1,0.3), add=T, probability = T)
lines(density(out$non),col=rgb(1,0,0))
lines(density(out$RB),col=rgb(0,0,1))
legend("topright", legend=c("non-RB","RB"), col=c(rgb(1,0,0,0.5), 
                                                      rgb(0,0,1,0.5)), pt.cex=2, pch=15 )

## plot for RB-MH

MH <- read.csv("out_MH.csv")

hist(MH$non, breaks=30, col=rgb(1,0,0,0.3), xlab="theta",ylim = c(0,9), 
     ylab="density", main="distribution of theta_hat",probability = T )
hist(MH$RB, breaks=30, col=rgb(0,0,1,0.3), add=T, probability = T)
lines(density(MH$non),col=rgb(1,0,0))
lines(density(MH$RB),col=rgb(0,0,1))
legend("topright", legend=c("non-RB","RB"), col=c(rgb(1,0,0,0.5), 
                                                  rgb(0,0,1,0.5)), pt.cex=2, pch=15 )