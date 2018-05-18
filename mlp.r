require(nnet)
require(tseriesChaos)

f <- function(net) {
    return ( 1/(1+exp(-net)) )
}

df_dnet <- function(net) {
    return ( f(net) * (1 - f(net)) )
}

fhard <- function(net) {
    r = net
    r[net > 0] = 1
    r[net <= 0] = 0
    return (r)
}

mlp.architecture <- function(input.length = 2,
                 hidden.length = 2,
                 output.length = 1,
                 my.f = f,
                 my.df_dnet = df_dnet) {

    layers = list()
    layers$hidden = matrix(runif(min=-0.5, max=0.5, 
            n=hidden.length*(input.length+1)), 
                   nrow=hidden.length, ncol=input.length+1)

    layers$output = matrix(runif(min=-0.5, max=0.5, 
            n=output.length*(hidden.length+1)), 
                   nrow=output.length, ncol=hidden.length+1)

    model = list()
    model$layers = layers
    model$f = my.f
    model$df_dnet = my.df_dnet

    return (model)
}

mlp.forward <- function(model, x_p) {
    # x = c(1, 0)

    f_h_net_h_pj = rep(0, nrow(model$layers$hidden))
    df_h_dnet_h_pj = rep(0, nrow(model$layers$hidden))
    for (j in 1:nrow(model$layers$hidden)) {
        net_h_pj = c(x_p, 1) %*% model$layers$hidden[j,]
        f_h_net_h_pj[j] = model$f(net_h_pj)
        df_h_dnet_h_pj[j] = model$df_dnet(net_h_pj)
    }

    f_o_net_o_pk = rep(0, nrow(model$layers$output))
    df_o_dnet_o_pk = rep(0, nrow(model$layers$output))
    for (k in 1:nrow(model$layers$output)) {
        net_o_pk = c(f_h_net_h_pj, 1) %*% model$layers$output[k,]
        f_o_net_o_pk[k] = model$f(net_o_pk)
        df_o_dnet_o_pk[k] = model$df_dnet(net_o_pk)
    }

    fwd = list()
    fwd$f_h_net_h_pj = f_h_net_h_pj
    fwd$f_o_net_o_pk = f_o_net_o_pk
    fwd$df_h_dnet_h_pj = df_h_dnet_h_pj
    fwd$df_o_dnet_o_pk = df_o_dnet_o_pk

    return (fwd)
}

mlp.backpropagation <- function(X, Y, model, eta=0.1, threshold=1e-2) {
    
    sqerror = 2 * threshold
    while (sqerror > threshold) {
        sqerror = 0

        # Treinando com cada exemplo de meu conjunto X dadas as classes em Y
        for (p in 1:nrow(X)) {
        x_p = X[p,]
        y_p = Y[p,]

        fwd = mlp.forward(model, x_p)
        o_p = fwd$f_o_net_o_pk

        delta_p = y_p - o_p

        # Calculando erro quadrático
        sqerror = sqerror + sum(delta_p^2)

        # Calculando delta da camada de saída para um padrão
        delta_o_p = delta_p * fwd$df_o_dnet_o_pk

        # Calculando delta da camada escondida para um padrão
        w.length = ncol(model$layers$output)-1
        delta_h_p = fwd$df_h_dnet_h_pj * 
            (delta_o_p %*% model$layers$output[,1:w.length])

        # Atualizando a camada de saída
        model$layers$output = model$layers$output + 
            eta * (as.vector(delta_o_p) %*% t(c(as.vector(fwd$f_h_net_h_pj), 1)))

        # Atualizando a camada escondida
        model$layers$hidden = model$layers$hidden +
            eta * (as.vector(delta_h_p) %*% t(c(x_p, 1)))

         }

         sqerror = sqerror / nrow(X)
         cat("Average squared error: ", sqerror, "\n")
    }

    return (model)
}

xor.test <- function(eta=0.1, threshold=1e-2, plot=T) {

    dataset = read.csv("data.csv", header=T)
    X = matrix(ts(dataset[,2:17]), nrow=17, ncol=36)
    Y = matrix(dataset[,18], ncol=)

    cat("Inputs...\n")
    print(X)

    cat("Expected outputs...\n")
    print(Y)

    cat("Press ENTER to continue...\n")
    readline();

    model = mlp.architecture(2, 2, 1)
    trained.model = mlp.backpropagation(X, Y, model, eta, threshold)

    for (p in 1:nrow(X)) {
        x_p = X[p,]
        y_p = Y[p,]

        fwd = mlp.forward(trained.model, x_p)

        print(x_p)
        print(y_p)
        print(fwd$f_o_net_o_pk)

        #readline()
    }

    if (plot == TRUE) {
        xor.plot(trained.model)
    }

    return (trained.model)
}

xor.plot <- function(model) {
    A = seq(0, 1, length=100)
    net1 = outer(A, A, function(x, y) { 
                cbind(x, y, 1)%*%model$layers$hidden[1,] })
    hyperplane1 = fhard(net1)
    net2 = outer(A, A, function(x, y) { 
                cbind(x, y, 1)%*%model$layers$hidden[2,] })
    hyperplane2 = fhard(net2)

    res = hyperplane1 + hyperplane2
    filled.contour(res)
}

breast.test <- function(hidden.length = 2, eta=0.1, 
            train.size=0.75, threshold=1e-2) {

    dataset = read.table("../datasets/breast/dataset.dat", header=F)
    train.size = ceiling(nrow(dataset) * train.size)
    train.id = sample(1:nrow(dataset), size=train.size)

    train.set = dataset[train.id,]
    test.set = dataset[-train.id,]

    X = matrix(ts(train.set[,1:9]), ncol=9)
    Y = matrix(train.set[,10], ncol=1)

    X.test = matrix(ts(test.set[,1:9]), ncol=9)
    Y.test = matrix(test.set[,10], ncol=1)

    model = mlp.architecture(9, hidden.length, 1)
    trained.model = mlp.backpropagation(X, Y, model, eta, threshold)

    res = NULL
    for (p in 1:nrow(X.test)) {
        x_p = X.test[p,]
        y_p = Y.test[p,]

        fwd = mlp.forward(trained.model, x_p)

        res = rbind(res, cbind(y_p, fwd$f_o_net_o_pk))
    }

    colnames(res) = c("Expected", "Obtained")

    return (res)
}

breast.computer.error <- function(res) {
    res = round(res)
    acc = sum(res[,1] == res[,2]) / nrow(res)
    return (acc)
}

wine.test <- function(hidden.length = 2, eta=0.1, 
            train.size=0.75, threshold=1e-2) {

    dataset = read.csv("../datasets/wine/wine.data", sep=",", header=F)
    features = dataset[,2:14]

    for (i in 1:ncol(features)) {
        features[, i] = (features[,i] - min(features[,i])) / (max(features[,i]) - min(features[,i]))
    }

    classes = class.ind(dataset[,1])
    dataset = cbind(features, classes)

    train.size = ceiling(nrow(dataset) * train.size)
    train.id = sample(1:nrow(dataset), size=train.size)

    train.set = dataset[train.id,]
    test.set = dataset[-train.id,]

    X = matrix(ts(train.set[,1:13]), ncol=13)
    Y = matrix(ts(train.set[,14:16]), ncol=3)

    X.test = matrix(ts(test.set[,1:13]), ncol=13)
    Y.test = matrix(ts(test.set[,14:16]), ncol=3)

    model = mlp.architecture(13, hidden.length, 3)
    trained.model = mlp.backpropagation(X, Y, model, eta, threshold)

    res = NULL
    for (p in 1:nrow(X.test)) {
        x_p = X.test[p,]
        y_p = Y.test[p,]

        fwd = mlp.forward(trained.model, x_p)
        res = rbind(res, c(y_p, fwd$f_o_net_o_pk))
    }

    colnames(res) = c("E1", "E2", "E3", "O1", "O2", "O3")

    return (res)
}

mnist.test <- function(hidden.length = 4, eta=0.1, 
            train.size=0.25, threshold=1e-2) {

    dataset = read.table("../datasets/mnist/mnist.data", header=T)

    train.size = ceiling(nrow(dataset) * train.size)
    train.id = sample(1:nrow(dataset), size=train.size)

    train.set = dataset[train.id,]
    test.set = dataset[-train.id,]

    X = matrix(ts(train.set[,1:(28*28)]), ncol=28*28)
    Y = matrix(ts(train.set[,(28*28+1):ncol(train.set)]), ncol=ncol(train.set)-(28*28))

    X.test = matrix(ts(test.set[,1:(28*28)]), ncol=28*28)
    Y.test = matrix(ts(test.set[,(28*28+1):ncol(test.set)]), ncol=ncol(test.set)-(28*28))

    model = mlp.architecture(28*28, hidden.length, 10)
    trained.model = mlp.backpropagation(X, Y, model, eta, threshold)

    res = NULL
    for (p in 1:nrow(X.test)) {
        x_p = X.test[p,]
        y_p = Y.test[p,]

        fwd = mlp.forward(trained.model, x_p)

        expected.class = which.max(y_p)-1
        obtained.class = which.max(fwd$f_o_net_o_pk)-1
        res = rbind(res, c(expected.class, obtained.class))
    }

    return (res)
}

lorenz.test <- function(hidden.length = 4, eta=0.1, 
            train.size=0.75, threshold=1e-2) {

    dataset = read.table("../datasets/lorenz/lor63.dat", header=F)
    dataset[,1] = (dataset[,1] - min(dataset[,1])) / (max(dataset[,1]) - min(dataset[,1]))

    # Takens' embedding theorem
    # (x(1), x(1+5), x(1+2*5)) => (x(1), x(6), x(11))
    #                 (x(2), x(7), x(12))
    #               ...
    dataset = embedd(dataset[,1], m=3, d=5)

    train.size = ceiling(nrow(dataset) * train.size)
    train.id = sample(1:nrow(dataset), size=train.size)

    train.set = dataset[train.id,]
    test.set = dataset[-train.id,]

    X = matrix(ts(train.set[,1:2]), ncol=2)
    Y = matrix(ts(train.set[,3]), ncol=1)

    X.test = matrix(ts(test.set[,1:2]), ncol=2)
    Y.test = matrix(ts(test.set[,3]), ncol=1)

    model = mlp.architecture(2, hidden.length, 1)
    trained.model = mlp.backpropagation(X, Y, model, eta, threshold)

    res = NULL
    for (p in 1:nrow(X.test)) {
        x_p = X.test[p,]
        y_p = Y.test[p,]

        fwd = mlp.forward(trained.model, x_p)

        res = rbind(res, c(y_p, fwd$f_o_net_o_pk))
    }

    return (res)
}
