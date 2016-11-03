# -*- encoding: utf-8 -*-
from pods.models import Pod, Channel, Type, Discipline
from django.contrib.sites.models import Site
from django.conf import settings as django_settings
from django.contrib.auth.models import User

from dashing.widgets import NumberWidget
from random import randint


class NewClientsWidget(NumberWidget):
    title = 'Users'

    def get_value(self):
        owners = User.objects.distinct().count()
        owners = 10
        return owners

    def get_detail(self):
        return '10 actives'

    def get_more_info(self):
        return '10 fakes'
