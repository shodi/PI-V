# PI-V
PI machine learning

Para que você possa executar o programa corretamente é necessário que você possua os seguintes pré requisitos:
  * SO Linux ou iOS
  * Python2.7 (Versões anteriores podem ocasionar erro de importação de submódulos)
  * Algum compilador LaTeX para gerar o relatório da aplicação
  * Possuir a lib libasound2-dev
  * Possuir a lib portaudio19-dev

### Como executar
Criar o ambiente virtual (vide venv), e instalar as dependências. Executar `pip install -r requirements.txt` na raiz do projeto.

### Executando mlp.r
```
source("mlp.r")
dataset = read.csv('__data.csv', header=F, skip=1)
dataset <- dataset[c(1,2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 8)]
ids = sample(1:nrow(dataset), size=100)
training = dataset[ids,]
test = dataset[-ids,]
model = mlp.architecture(input.length=14, output.length=1, hidden.length=15)
trained = mlp.backpropagation(dataset=training, model=model, eta=0.5)
mlp.forward(model=trained$model, Xp=as.numeric(test[1,1:14]))
```
