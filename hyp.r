source("mlp.r")

test <- function(dataset=dataset, eta=0.2){
    #dataset = cbind(rnorm(mean=0, sd=1, n=100), rnorm(mean=0, sd=1, n=100), 0)
    #dataset = rbind(dataset, cbind(rnorm(mean=0, sd=1, n=100), rnorm(mean=1, sd=1, n=100), 1))
    dataset = read.csv('dataset.csv', header=F, skip=1)
    dataset = rbind(dataset, read.csv('dataset.csv', header=F, skip=1))

    plot(dataset[,1:2], col=dataset[,3]+1)
    locator(1)

    ids = sample(1:nrow(dataset), size=150)
    train = dataset[ids,]
    test = dataset[-ids,]

    for(hyp in 1:10){
        #model = mlp.architecture(input.length=2, output.length=1, hidden.length=hyp)
        #trained = mlp.backpropagation(model=model, dataset=train, eta=eta)
        model = mlp.architecture(input.length=14, output.length=1, hidden.length=hyp)
        trained = mlp.backpropagation(dataset=train, model=model, eta=eta)

        wrong = 0
        for(j in 1:nrow(test)){
            x = test[j, 1:2]
            y.e = as.numeric(test[j, 3])
            y.o = round(mlp.forward(model=trained$model, Xp=x)$f_net_o_p)
            if(y.e != y.o){
                wrong = wrong + 1
            }
        }
        error = wrong / nrow(test)
        cat(hyp, "\t", error, "\n")
    }

}