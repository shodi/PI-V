f <- function(net) {
    return ( 1/(1+exp(-net)) )
}

df_dnet <- function(f_net) {
    return (f_net * (1 - f_net))
}

mlp.architecture <- function(input.length=2,
                             hidden.length=2,
                             output.length=1,
                             activation.function=f,
                             d_activation.function=df_dnet) {

    model = list()
    model$input.length = input.length
    model$hidden.length = hidden.length
    model$output.length = output.length

    model$hidden = matrix(runif(min=-0.5, max=0.5, 
            hidden.length*(input.length+1)), 
                   nrow=hidden.length, ncol=input.length+1)

    model$output = matrix(runif(min=-0.5, max=0.5, 
            output.length*(hidden.length+1)), 
                   nrow=output.length, ncol=hidden.length+1)

    model$f = activation.function
    model$df_dnet = d_activation.function

    return (model)
}

mlp.forward <- function(model, Xp) {
    # Hidden layer
    net_h_p = model$hidden %*% c(Xp, 1)
    f_net_h_p = model$f(net_h_p)
   
   # Output layer
   net_o_p = model$output %*% c(as.numeric(f_net_h_p), 1)
   f_net_o_p = model$f(net_o_p)

   # Results
   ret = list()
   ret$net_h_p = net_h_p
   ret$net_o_p = net_o_p
   ret$f_net_h_p = f_net_h_p
   ret$f_net_o_p = f_net_o_p

   return (ret)
}

mlp.backpropagation <- function(model,
                                dataset,
                                eta=0.1,
                                threshold=1e-4) {

    squaredError = 2 * threshold
    counter = 0

    while(squaredError > threshold) {
        squaredError = 0
 
        for (p in 1:nrow(dataset)) {
            Xp = as.numeric(dataset[p, 1:model$input.length])
            Yp = as.numeric(dataset[p,
                    (model$input.length+1):ncol(dataset)])

            results = mlp.forward(model, Xp)
            Op = results$f_net_o_p

            # Calculando o erro
            error = Yp - Op

            squaredError = squaredError + sum(error^2)

            delta_o_p = error * model$df_dnet(results$f_net_o_p)
        
            w_o_kj = model$output[,1:model$hidden.length]
            delta_h_p = 
                as.numeric(model$df_dnet(results$f_net_h_p)) *
                    (as.numeric(delta_o_p) %*% w_o_kj)

            model$output = model$output +
                eta*(delta_o_p%*%as.vector(c(results$f_net_h_p,1)))
            model$hidden = model$hidden +
                eta*(t(delta_h_p) %*% as.vector(c(Xp,1)))
        }
        squaredError = squaredError / nrow(dataset)

        cat("Erro médio quadrado = ", squaredError, "\n")

        counter = counter + 1
    }
    cat("Base treinada Daniel, SEU GOSTOSO!")
    ret = list()
    ret$model = model
    ret$counter = counter

    return (ret)
}


dataset = read.csv('__data.csv', header=F, skip=1)
dataset <- dataset[c(1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 8)]
ids = sample(1:nrow(dataset), size=50)
training = dataset[ids,]
test = dataset[-ids,]
model = mlp.architecture(input.length=15, output.length=1, hidden.length=16)
trained = mlp.backpropagation(dataset=training, model=model, eta=0.5)
write.csv(trained$model$hidden, file="hidden.csv", row.names=FALSE)
write.csv(trained$model$output, file="output.csv", row.names=FALSE)
