# Uso de VIRTUALENV no projeto

Para este projeto, optamos pelo uso do VIRTUALENV para que todos os membros da equipe tenham o mesmo ambiente de desenvolvimento e a certeza de que as condições de teste são iguais a todos de acordo com as versões de ferramentas de terceiros.

## Instalação

Se você está usando Ubuntu ou Debian:

```
aipi@aipi:~/$ sudo apt-get install python-setuptools
aipi@aipi:~/$ sudo easy_install virtualenv
```

Se não está:

```
aipi@aipi:~/$ sudo pip install virtualenv
```

Como o ambiente já está instalado basta você:

``` 
aipi@aipi:~/$ source env/bin/activate
```

Você irá perceber que o prompt do seu shell é alterado após a execução do comando acima, sendo a partir daí, precedido pelo nome do ambiente virtual ativo entre parênteses (veja acima). Isso faz também com que sua variável de ambiente $PATH passe a apontar, em primeiro lugar, para a pasta bin de dentro do ambiente virtual, de forma que quando você chamar o interpretador Python pela linha de comando, o executável que será aberto será o interpretador que está instalado dentro do ambiente virtual atual, pois será o primeiro encontrado no $PATH.

## Instalando pacotes dentro do ambiente virtual

Uma vez que ativamos o ambiente virtual que desejamos usar, podemos então instalar os pacotes que forem necessários para nosso projeto. Por exemplo:

```
(env)aipi@aipi:~/$ pip install Django
Downloading/unpacking Django
    Downloading Django-1.4.1.tar.gz (7.7Mb): 7.7Mb downloaded
    Running setup.py egg_info for package Django
Installing collected packages: Django
    Running setup.py install for Django
Successfully installed Django
Cleaning up...
```

Agora, podemos abrir um shell Python dentro do ambiente `env` recém criado, e testar se o Django está mesmo instalado:

```
(env)aipi@aipi:~/$ python
Python 2.7.2+ (default, Jul 20 2012, 22:15:08) 
[GCC 4.6.1] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.__file__
'/home/user/env/local/lib/python2.7/site-packages/django/__init__.pyc'
```

Tudo certo, o Django está instalado corretamente dentro do ambiente `env`.

Para sair do ambiente virtual ativo, utilize o comando `deactivate`.

## Gerando lista de dependências do projeto

Uma vez que estejamos utilizando ambientes virtuais para nossos projetos, e que estejamos instalando todos os pacotes necessários via pip, temos facilmente em mãos a lista de pacotes dos quais nosso projeto depende. Para obter essa lista, basta utilizar o comando freeze do pip:

```
(env)aipi@aipi:~/$ pip freeze
Django==1.4.1
Werkzeug==0.8.3
argparse==1.2.1
distribute==0.6.24
django-bootstrap-toolkit==2.5.8
django-extensions==0.9
django-registration==0.8
wsgiref==0.1.2
```

Tal comando escreve na saída-padrão a lista de pacotes (bem como suas versões), de cada uma das dependências instaladas via pip no projeto ativo. 

Primeiro, devemos armazenar em um arquivo as informações geradas pelo pip freeze:

```
(env)aipi@aipi:~/$ pip freeze > requirements.txt
```

Após isso, podemos enviar o arquivo requirements.txt para o chefão e, usando o pip, ele poderá executar:

```
(env)anotheruser@anotherhost:~/$ pip install -r requirements.txt
```
