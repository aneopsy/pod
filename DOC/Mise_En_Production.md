## Mise en production
### Base de données

Lors de la mise en production, il est conseillé d'utiliser une base de données MySql ou PostgreSql.

Si vous n'avez pas de serveur existant, voici un exemple de mise en place MySql :
```sh
root@podvm:~# aptitude install mysql-server mysql-client phpmyadmin
```
La base de données pour l'application a été créée via phpmyadmin avec comme utilisateur pod et la base de données pod.

2° méthode sans phpmyadmin :
Installer mysql (installation en root):
```sh
root@podvm:~# aptitude install mysql-server mysql-client
```
 Pour faciliter l'accès à mysql créer dans /root un fichier ”.my.cnf” et mettez dedans :
```sh
[client]
user = root
password = 'celui choisi à l installation de mysql'
```
Créer la base de données que nous appellerons 'pod' :
```sh
root@podvm:~# mysqladmin create pod
```
Puis donnez les droits d'accès à pod à notre utilisateur pod
```sh
root@podvm:~# mysql
mysql> GRANT ALL PRIVILEGES ON pod.* TO 'pod'@localhost IDENTIFIED BY 'mot de passe';
Query OK, 0 rows affected (0.00 sec)
```
```sh
mysql> exit
```
----
 Après avoir créé une base mysql, dans le settings.py, remplacer la partie database par :

```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',           # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pod',                          # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'pod',
        'PASSWORD': 'mot de passe de pod',
        'HOST': '',                        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                                 # Set to empty string for default.
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' },        # On veut que la base utilise des tables au format InnoDB
    }
}
```
**Voici la configuration pour PostGreSql :**

```Python
DATABASES = {
#Configuration MySql
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pod',
        'USER': 'pod',
        'PASSWORD': '********',
        'HOST': '',
        'PORT': '',
        #'OPTIONS': {'init_command': 'SET storage_engine=INNODB;'}
    }
}
```

Attention, pour PostGreSql, il faudra installer ces paquets supplémentaires :

```sh
(django_pod)v-podcast@v-podcast:~# sudo aptitude install libpq-dev
(django_pod)v-podcast@v-podcast:~# pip install psycopg2
```

#### CREATION BDD :
On repasse en pod et on crée les tables dans la bases de données :
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py migrate
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py loaddata core/fixtures/initial_data.json
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py createsuperuser --username root
```

### Serveur Web en Frontal
#### Apache

**Installation des paquets**
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 libapache2-mod-wsgi
```

**Création du virtual host**
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo nano /etc/apache2/sites-available/pod.conf
```

_Voici un exemple de vhost :_
_Attention, les données sont à modifier selon votre installation_

> Apache 2.4

```sh

<VirtualHost *:80>

        ServerName v-podcast.upf.pf

        ServerAdmin admin@upf.pf


        ErrorLog ${APACHE_LOG_DIR}/pod-error.log
        CustomLog ${APACHE_LOG_DIR}/pod-access.log combined

        Alias /robots.txt /home/v-podcast/django_projects/pod/pod_project/static/robots.txt
        Alias /favicon.ico /home/v-podcast/django_projects/pod/pod_project/static/favicon.ico

        Alias /media/ /var/v-podcast/media/
        Alias /static/ /home/v-podcast/django_projects/pod/pod_project/static/

        <Directory /home/v-podcast/django_projects/pod/pod_project/static>
        Require all granted
        </Directory>

        <Directory /var/v-podcast/media>
        Require all granted
        </Directory>

        WSGIScriptAlias / /home/v-podcast/django_projects/pod/pod_project/pod_project/wsgi.py
        #WSGIPythonPath /home/pod/django_projects/pod/pod_project:/var/www/.virtualenvs/django_pod/lib/python2.7/site-packages
        WSGIDaemonProcess v-podcast python-path=/home/v-podcast/django_projects/pod/pod_project:/home/pod/.virtualenvs/django_pod/lib/python2.7/site-packages
        WSGIProcessGroup v-podcast

        <Directory /home/v-podcast/django_projects/pod/pod_project/pod_project>
        <Files wsgi.py>
        Require all granted
        </Files>
        </Directory>

</VirtualHost>

```


***
> _Attention, les vidéos vont être uploadées dans le répertoire « média ». Il faut donc prévoir de l'espace disque pour ce répertoire et **donner le droit en lecture et en écriture** à l'utilisateur web (www-data)_
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo chown -R www-data:www-data media/
```

**Activer le vhost**
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo a2ensite pod.conf
  Enabling site pod.
  To activate the new configuration, you need to run:
    service apache2 reload
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo service apache2 reload
  [ ok ] Reloading web server config: apache2.
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$
```

### Fichier static

Par défaut, chaque application possède ses propres fichiers statiques (images, css, javascript etc.)
La commande ci-après permet de les centraliser pour que ces fichiers soient distribués plus facilement par le fontal web.

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ mkdir static
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ ll
  total 968
  drwxr-xr-x 7 pod pod   4096 mai   19 17:12 core
  -rw-r--r-- 1 pod pod 221184 mai   19 17:12 db.sqlite3
  drwxr-xr-x 2 pod pod   4096 mai   19 17:05 django_cas_gateway
  drwxr-xr-x 3 pod pod   4096 mai   19 16:43 locale
  -rwxr-xr-x 1 pod pod    254 avril 25 17:24 manage.py
  drwxr-xr-x 5 pod pod   4096 mai   19 17:11 media
  drwxr-xr-x 2 pod pod   4096 mai   19 17:05 pod_project
  drwxr-xr-x 5 pod pod   4096 mai   19 16:00 pods
  -rwxr-xr-x 1 pod pod 730429 avril 25 17:24 schema_bdd.jpg
  drwxr-xr-x 2 pod pod   4096 mai   19 17:26 static
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py collectstatic
```

**Attention, il faudra donc répéter cette commande lors de chaque mise en production.**
```sh
workon django_pod
cd /home/v-podcast/django_projects/pod/pod_project/
./manage.py collectstatic
```

### Relance du serveur et tests finaux

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ sudo service apache2 restart
  [ ok ] Restarting web server: apache2 ... waiting
```

Refaire les tests de fonctionnement.
> Bien vérifier l'ajout d'une vidéo et son encodage.
