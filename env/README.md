# Instalação

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

Agora, podemos abrir um shell Python dentro do ambiente NomeDoAmbiente recém criado, e testar se o Django está mesmo instalado:

```
(env)aipi@aipi:~/$ python
Python 2.7.2+ (default, Jul 20 2012, 22:15:08) 
[GCC 4.6.1] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.__file__
'/home/user/NomeDoAmbiente/local/lib/python2.7/site-packages/django/__init__.pyc'
```

Tudo certo, o Django está instalado corretamente dentro do ambiente `env`.

Para sair do ambiente virtual ativo, utilize o comando `deactivate`.
