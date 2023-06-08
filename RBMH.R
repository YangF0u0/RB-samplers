theta_hat_MH <- c()
theta_RB_MH <- c()

for (iter in 1:1000){
  # Define the target distribution
  target <- function(x) {
    dnorm(x)
  }
  
  # Define initial starting point
  x_init <- 0
  
  # Define the proposal transition kernel
  proposal <- function(y,x) {
    dcauchy(y, location=x, scale=1)
  }
  
  # Define the acceptance probability
  acc <- function(x,y){
    min(1, (target(y)*proposal(x,y)) / (target(x)*proposal(y,x)))
  }
  
  n_samples <- 1000
  samples <- numeric(n_samples)
  curr_x <- x_init
  acc_probs <- c()
  y <- c()
  u <- c()
  accepted <- rep(0,n_samples)
  
  for (i in 1:n_samples) {
    # Propose a new sample
    y_new <- rcauchy(1, curr_x, scale=1)
    y <- c(y,y_new)
    
    # Calculate acceptance probability
    acc_prob <- acc(curr_x,y_new)
    acc_probs <- c(acc_probs,acc_prob)
    
    # Accept or reject the proposal
    u_new <- runif(1)
    u <- c(u,u_new)
    if (u_new < acc_prob) {
      curr_x <- y_new
      accepted[i] <- 1
    }
    
    # Store the current sample
    samples[i] <- curr_x
  }
  
  ## non-RB estimator for the true mean of X
  theta_hat_MH <- c(theta_hat_MH,mean(samples))
  
  acc_y <- y[accepted==1]
  zeta <- function(xi,y,n){
    sum <- 1
    j <- which(samples==xi)[1]+1
    while (u[j] > acc(xi,y[j]) && j<=n_samples) {
      for(t in j:1){
        sum <- 1+sum*(1-acc(xi,y[t]))
      }
      j <- j+1
    }
    return(sum)
  }
  
  zeta_hat <- c()
  for(i in 1:length(acc_y)){
    zeta_hat[i] <- zeta(acc_y[i],y,n_samples)
  }
  theta_RB_MH <- c(theta_RB_MH,sum(zeta_hat*acc_y)/n_samples)
  
  data_MH<-data.frame(non=theta_hat_MH,RB=theta_RB_MH)
  write.csv(data_MH,"out_MH.csv")
}