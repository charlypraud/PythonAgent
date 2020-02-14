# AgentPython

AgentPython est une application permettant d'avoir un monitoring d'une machine en temps réel.

## Guide de l'application

### Prérequis

- Base de donnée MYSQL
- Python 3
- PhpMyAdmin


### Installation

#### Etape 1 : Mise en place de la base de données avec Phpmyadmin

##### Executer le script tests4.sql

```
Se connecter sur la base de données 
=> Cliquer sur Importer 
=> Parcourir les fichiers 
=> Executer 'tests4.sql'
```


#### Modifier le fichier serveur.py

A l'aide d'un éditeur de texte, ouvrez le fichier serveur.py puis modifiez les lignes suivantes

```
connection = pymysql.connect(host='localhost',
                            port=3308,
                            user='root',
                            password='',
                            db='tests4',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
```

- "db" correspond au nom de votre base de données
- "user" correspond à l'utilisateur de la base
- "password" correspond au mot de passe de l'utilisateur
- "port" correspond au port de votre serveur MySQL

#### Etape 2 : Démarrage du serveur de l'application

Ouvrez un invite de commande dans le dossier de l'application et exécutez la ligne suivante

```
python3 serveur.py
```

### Utilisation

Pour utiliser l'application, ouvrez votre navigateur et saisissez dans votre barre d'adresse la ligne suivante

```
http://localhost:5000/
```
('localhost' peut être remplacé par une adresse IP)
