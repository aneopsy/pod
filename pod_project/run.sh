#!/bin/sh
echo "Lancement du Server"
sudo git -C /home/v-podcast/django_projects/pod/pod_project pull origin master
sudo ~/.virtualenvs/django_pod/bin/python /home/v-podcast/django_projects/pod/pod_project/manage.py runserver 10.3.1.114:80
