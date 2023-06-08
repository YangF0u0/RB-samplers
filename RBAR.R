thetas<-c()
theta_RBs<-c()

for(I in 1:100){
  ## accept-reject sampler
  T <- 0
  N <- 100
  c <- 3
  U <- c()
  Y <- c()
  X <- c()
  rho <- c()
  set.seed(100)
  
  target_dist <- function(x){
    dt(x,df=5)
  }
  
  proposal_dist <- function(x){
    dnorm(x)
  }
  
  ## a simple AR sampler
  while(length(X) < N){
    U_new <- runif(1, 0, 1)
    U <- c(U,U_new)
    Y_new <- rnorm(1)
    Y <- c(Y,Y_new)
    if(U_new <= (1 / c) * target_dist(Y_new)/proposal_dist(Y_new)){
      X <- c(X,Y_new)
    }
    T <- T+1
  }
  
  ## Non-RB estimator
  theta_hat <- mean(X)
  
  ## DP-based algorithm to compute the sum of products for all possible splits
  sum_products <- function(A,x){
    t<-length(A)
    dp_table <- matrix(0, nrow = t, ncol = x)
    
    for (i in 1:t) {
      for (j in 1:x) {
        if(j==1){
          dp_table[i,j] <- prod(1-A[1:i])*sum(A[1:i]/(1-A[1:i]))
        }
        else if(j>i){
          dp_table[i,j] <- 0
        }
        else if(j<=i){
          dp_table[i,j] <- (1-A[i])*dp_table[i-1,j]+A[i]*dp_table[i-1,j-1]
        }
      }
    }
    
    return(dp_table[t,x])
  }
  
  ## normalizing for rho
  denominator <- sum_products(U[1:(T-1)],N-1)
  
  for(i in 1:(T-1)){
    minus_i <- U[setdiff(1:(T-1),i)]
    numerator <- sum_products(minus_i,N-2)
    rho[i] <- numerator/denominator
  }
  rho[T] <- 1
  
  theta_RB <- sum(rho*Y)/N
  
  thetas<-c(thetas,theta_hat)
  theta_RBs<-c(theta_RBs,theta_RB)
}

data<-data.frame(non=thetas,RB=theta_RBs)
write.csv(data,"out.csv")