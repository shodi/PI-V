f <- function(net) {
    return ( 1/(1+exp(-net)) )
}

df_dnet <- function(net) {
    return ( f(net) * (1 - f(net)) )
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
        x_p = as.numeric(dataset[p, 1:model$input.length])
        y_p = as.numeric(dataset[p, (model$input.length+1):ncol(dataset)])

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
