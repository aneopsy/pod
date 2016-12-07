### Pré-requis:
* Système exploitation: Installation effectuée sur Debian 8 (jessie) 64bits
* Matériel:
 * Lille1: serveur dédié 8coeurs/8Go de ram
 * Valenciennes: VM 4vcpu et 8Go RAM
 * CNAM (Paris) : VM Debian(wheezy) - Ram 16Go ajustable et CPU 2x2 coeurs ajustable
 * Nice : hébergement chez ovh

### Création d'un nouvel utilisateur
```sh
$ adduser v-podcast
$ apt-get install sudo
$ adduser v-podcast sudo
```
### Mise en place de l'environnement système
_En tant que root_
```sh
root@v-podcast:$ su
root@v-podcast:$ aptitude update
root@v-podcast:$ aptitude install python-pip python-dev build-essential git libmysqlclient-dev graphviz libgraphviz-dev pkg-config libldap2-dev libsasl2-dev libssl-dev libjpeg-dev python-imaging libfreetype6-dev
```
Installation complémentaire pour python :
- python-chardet : Détecteur universel d'encodage de caractères pour Python2
- python-fpconst : Utilities for handling IEEE 754 floating point special values
- python-apt : Interface Python pour libapt-pkg
- python-debian : modules python pour travailler avec des formats de données utilisés dans Debian
- python-debianbts : Python interface to Debian's Bug Tracking System
- python-reportbug : modules Python pour interagir avec des systèmes de gestion de bogues
- python-soappy : SOAP Support for Python

```sh
root@v-podcast:$ aptitude install python-chardet python-fpconst python-apt python-debian python-debianbts python-reportbug python-reportbug python-soappy
```

### Mise en place de l'environnement virtuel
_En tant qu'utilisateur v-podcast_
```sh
v-podcast@v-podcast:$ sudo pip install virtualenvwrapper
v-podcast@v-podcast:$ vim .bashrc
```
_Ajouter ces deux lignes à la fin :_

    <file .bashrc>
    ...
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
    </file>


_Prendre en compte les modifications :_
```sh
v-podcast@v-podcast:$ source .bashrc
```
_Et créer un nouvel environnement virtuel :_
```sh
v-podcast@v-podcast:$ mkvirtualenv --system-site-packages django_pod
  New python executable in django_pod/bin/python
  Installing setuptools, pip...done.
(django_pod)v-podcast@v-podcast:$
```
Vérification de la présence du répertoire .virtualenvs
```sh
(django_pod)v-podcast@v-podcast:$ ls -al
...
  drwxr-xr-x 3 pod pod 4096 mai   19 14:54 .virtualenvs
...
```

### Récupération des sources

_Concernant l'emplacement du projet, je conseille de le mettre dans **/usr/local/django_projects**_
```sh
(django_pod)v-podcast@v-podcast:~$ sudo mkdir /usr/local/django_projects
```
_Vous pouvez faire un lien symbolique dans votre home pour arriver plus vite dans le répertoire django_projects:_
```sh
(django_pod)v-podcast@v-podcast:~$ ln -s /usr/local/django_projects django_projects
```
_Placez vous dans le répertoire django_projects_
```sh
(django_pod)v-podcast@v-podcast:~$ cd django_projects
(django_pod)v-podcast@v-podcast:~/django_projects$
```
_On récupère les sources https://github.com/aneopsy/pod:_
Attention, si vous devez utiliser un proxy, vous pouvez le spécifier avec cette commande :
```sh
$> git config --global http.proxy http://PROXY:PORT
```

```sh
(django_pod)v-podcast@v-podcast:~$ sudo chown pod:pod /usr/local/django_projects
(django_pod)v-podcast@v-podcast:~$ ls -ld /usr/local/django_projects
drwxr-sr-x 2 pod pod 4096 mars  13 10:02 /usr/local/django_projects
(django_pod)v-podcast@v-podcast:~/django_projects$ git clone https://github.com/aneopsy/pod.git

Cloning into 'pod'...
remote: Counting objects: 350, done.
remote: Compressing objects: 100% (277/277), done.
remote: Total 350 (delta 66), reused 336 (delta 58), pack-reused 0
Receiving objects: 100% (350/350), 2.07 MiB | 972 KiB/s, done.
Resolving deltas: 100% (66/66), done.
```

### Installation de toutes les librairies python :
```sh
(django_pod)v-podcast@v-podcast:~/django_projects$ cd pod
(django_pod)v-podcast@v-podcast:~/django_projects/pod$ pip install -r requirements.txt
```
De même, si vous devez utiliser un proxy :
```sh
$> pip install --proxy="PROXY:PORT" -r requirements.txt
```

### Paramétrage
_il faut faire une copie des fichiers de configuration._
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod$ cd pod_project/pod_project/
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project/pod_project$ ls -l
  total 32
  -rwxr-xr-x 1 pod pod 1990 avril 25 17:24 ckeditor.py
  -rwxr-xr-x 1 pod pod    0 avril 25 17:24 __init__.py
  -rwxr-xr-x 1 pod pod 4945 avril 25 17:24 ISOLanguageCodes.py
  -rwxr-xr-x 1 pod pod 8173 avril 25 17:24 settings-sample.py
  -rwxr-xr-x 1 pod pod 4612 avril 25 17:24 urls.py
  -rwxr-xr-x 1 pod pod  899 avril 25 17:24 wsgi-sample.py
```

_On commence par le fichier **wsgi-sample.py**_
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project/pod_project$ cp wsgi-sample.py wsgi.py
```

_Il n'y a plus rien à changer dans ce fichier_

_Ensuite, on fait de même pour le fichier de configuration principal : settings_
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project/pod_project$ cp settings-sample.py settings.py
```
Dans ce fichier, il faut renseigner les noms et adresses mail des administrateurs. Ensuite, la variable DEBUG doit etre laissé à True en mode développement, ca permet d'afficher les erreurs dans le navigateur lors de la navigation. Par contre, il faut la mettre à False en production.
De même pour la base de données, il faut utiliser sqlite pour les tests et mysql pour la production.
Allowed hosts doit contenir la ou les adresses de connexion à la plateforme.
media_root est le chemin pour accéder aux fichiers media. C'est dans ce répertore que vont être stockés les vidéos et leur encodage.
Il faut ensuite configurer le mail, le cas et éventuellement le ldap.
Pour finir, il faut personnaliser les variables de template et d'établissement.

### Base de données

En développement, la base de données est en sqlite, elle va nous permettre de tester le fonctionnement de la plateforme avant sa mise en production

En production, il faudra utiliser du MySql ou du PostgreSql (voir ci-après pour cette mise en place).


```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py makemigrations
...
Migrations for 'filer':
  0002_auto_20150602_1113.py:
    - Alter field polymorphic_ctype on file
Migrations for 'flatpages':
  0002_auto_20150602_1113.py:
    - Add field content_en to flatpage
    - Add field content_fr to flatpage
    - Add field title_en to flatpage
    - Add field title_fr to flatpage
...
```

_Migration des tables :_

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ ./manage.py migrate
Operations to perform:
  Synchronize unmigrated apps: jquery, taggit_templatetags, django_cas_gateway, ckeditor, modeltranslation, haystack, bootstrap3
  Apply all migrations: core, filer, admin, sessions, sites, auth, contenttypes, flatpages, taggit, pods, easy_thumbnails
Synchronizing apps without migrations:
  Creating tables...
    Creating table taggit_templatetags_amodel
  Installing custom SQL...
  Installing indexes...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sites.0001_initial... OK
  Applying flatpages.0001_initial... OK
  Applying filer.0001_initial... OK
  Applying core.0001_initial... OK
  Applying easy_thumbnails.0001_initial... OK
  Applying easy_thumbnails.0002_thumbnaildimensions... OK
  Applying filer.0002_auto_20150602_1113... OK
  Applying flatpages.0002_auto_20150602_1113... OK
  Applying taggit.0001_initial... OK
  Applying pods.0001_initial.../home/moot/.virtualenvs/django_pod/local/lib/python2.7/site-packages/django/db/models/fields/__init__.py:1282: RuntimeWarning: DateTimeField Mediacourses.date_added received a naive datetime (2015-06-02 11:13:33.643534) while time zone support is active.
  RuntimeWarning)

 OK
  Applying sessions.0001_initial... OK
```

_On charge ensuite des données de base en base de données :_
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py loaddata core/fixtures/initial_data.json
```

Et on créé le superutilisateur :
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py createsuperuser --username root
```


## Installation tierce

### FFMPEG

_Utilisé pour l'encodage des vidéos._

Pour installer FFMPEG, j'ai télécharger la dernière version fournit sur le site officiel : http://ffmpeg.org/download.html#build-linux

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ su
  Mot de passe :
root:/home/pod/django_projects/pod/pod_project# cd /usr/local/
root:/usr/local# mkdir ffmpeg && cd ffmpeg
root:/usr/local/ffmpeg# wget http://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
root:/usr/local/ffmpeg# tar -Jxvf ffmpeg-release-64bit-static.tar.xz
root:/usr/local/ffmpeg# ln -s ffmpeg-2.6.3-64bit-static ffmpeg
```
Il faut modifier le fichier settings.py pour indiquer les chemins ffmpeg et ffprobe

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ vim pod_project/settings.py
```


### Elasticsearch

_Moteur de recherche_

Nécessite java pour etre lancé. Si votre machine n'a pas de version 7 ou supérieur, vous pouvez l'installer.
```sh
root:~# aptitude install openjdk-7-jre-headless
```
Il faut se rendre sur cette page et suivre les instructions pour son installation :
[Elasticsearch setup repository](http://www.elastic.co/guide/en/elasticsearch/reference/current/setup-repositories.html)

Il faut ensuite modifier le fichier de configuration d'elasticsearch pour le paramétrer.
Exemple de paramètres :
```


# Name your cluster here to whatever.
# Machine is called "Pod", so...
cluster.name: pod

node.name: "Pod1"

network.host: 127.0.0.1

# Unicast Discovery (disable multicast)
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.unicast.hosts: ["127.0.0.1"]

Vous pouvez également changer les paths :

  logs: /usr/local/var/log
  data: /usr/local/var/data
```

#### Elasticsearch : Ajout du template Pod
Pour optimiser la recherche, il faut créer l'index Pod dans elasticsearch et pousser le template fourni :

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py create_pod_index
```

Une commande est fournie dans le cadre où l'on souhaiterais indexer ou réindexer une,  plusieurs ou toutes les vidéos.

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py index_videos < __ALL__ || pod_id, pod_id...>
```

### Optionnel : Memcached
```sh
root@v-podcast:~# aptitude install memcached
```

### Traduction

_la plateforme est par défaut seulement en anglais mais il est possible de la traduire en français_
```sh
root@v-podcast:~# aptitude install gettext
```
revenir ensuite en tant qu'utilisateur pod (ctrl+d)
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ mkdir locale
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ ls -l
  total 956
  drwxr-xr-x 7 pod pod   4096 mai   19 16:00 core
  -rw-r--r-- 1 pod pod 215040 mai   19 16:02 db.sqlite3
  drwxr-xr-x 2 pod pod   4096 mai   19 15:59 django_cas_gateway
  drwxr-xr-x 2 pod pod   4096 mai   19 16:42 locale
  -rwxr-xr-x 1 pod pod    254 avril 25 17:24 manage.py
  drwxr-xr-x 2 pod pod   4096 mai   19 16:04 pod_project
  drwxr-xr-x 5 pod pod   4096 mai   19 16:00 pods
  -rwxr-xr-x 1 pod pod 730429 avril 25 17:24 schema_bdd.jpg
```

La commande ci-après va créer un fichier nommé django.po avec toutes les phrases clés de la plateforme qu'il faut traduire.
```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ django-admin.py makemessages -l fr
  processing locale fr
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ cd locale/fr/LC_MESSAGES/
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project/locale/fr/LC_MESSAGES$ ls -l
  total 64
  -rw-r--r-- 1 pod pod 61855 mai   19 16:43 django.po
```
Ce fichier peut être édité directement (avec vim ou poedit).
Une version traduite en français et maintenu lors du développement est disponible dans le répertoire traduction à la racine du projet. Il vous suffit de copier ce fichier dans le répertoire pod_project/locale/fr/LC_MESSAGES. Vous également personnaliser les traductions une fois ce fichier copié.

Une fois le fichier renseigné avec les traductions, il faut le compiler.

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project/locale/fr/LC_MESSAGES$ cd ../../..
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ django-admin.py compilemessages
  processing file django.po in /home/pod/django_projects/pod/pod_project/locale/fr/LC_MESSAGES
```

## Thème

Correspondance des images (dans « pod_project/settings.py ») :

- LOGO_SITE : situé à gauche, au dessus du menu, en face de la sélection des langues et du bouton de connexion ;
- LOGO_COMPACT_SITE : est utilisé dans la barre contenant le menu sur les interfaces mobiles, en remplacement de LOGO_SITE ;
- LOGO_ETB : utilisé dans la version par défaut du template personnalisé « templates/pre-header.html » du thème ;
- LOGO_PLAYER : utilisé dans la barre de commandes du lecteur vidéo ;
- SERV_LOGO : utilisé dans la partie gauche du pied de page « templates/footer.html » du thème.

### Header et footer

D'autre part, il vous est possible de créer un header et un footer personnalisés. Pour se faire, il vous faut copier le dossier custom situé dans le dossier templates et modifier les fichier header et footer s'y trouvant.
Une fois fait il ne reste plus qu'à indiquer dans votre settings.py où se trouvent vos templates personnalisés en mettant à jour la constante “TEMPLATE_CUSTOM” (seul le nom du dossier qui se trouve dans “templates” est nécessaire, pas besoin du chemin complet).

## lancement des tests

Tout un ensemble de tests dit unitaires ont été ajoutés depuis la version 1.1. Ils permettent de vérifier la création, la lecture, la mise à jour et la suppression d'éléments sur la plateforme.
De plus, selon la configuration, ils vérifient également la connexion Elasticsearch, CAS, LDAP et testent un encodage.

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py test core pods.tests.tests_models pods.tests.tests_views pods.tests.tests_delete_video
```

## Serveur de développement

N'hésitez pas à lancer le serveur de développement pour vérifier vos modifications au fur et à mesure.

À ce niveau, vous devriez avoir le site en français et en anglais et voir l'ensemble de la page d'accueil.

```sh
(django_pod)v-podcast@v-podcast:~/django_projects/pod/pod_project$ python manage.py runserver ADRESSE_IP/NOM_DNS:8080
```

Vérifier l'accès à la plateforme en saisissant les paramètres fournis http://ADRESSE_IP:8080 ou http://NOM_DNS:8080

--------------------

> Avant la mise en production, il faut vérifier le fonctionnement de la plateforme dont l'ajout d'une vidéo, son encodage et sa suppression.

> Attention, pour ajouter une vidéo, Il faut se rendre dans la partie administration de la plateforme pour créer au moins un type de vidéo (champs obligatoires)

> il faut vérifier l'authentification CAS, le moteur de recherche etc.

--------------------
