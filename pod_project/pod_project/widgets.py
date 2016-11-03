# -*- encoding: utf-8 -*-
from dashing.widgets import NumberWidget
from random import randint
#from django.contrib.auth.models import User


class NewClientsWidget(NumberWidget):
    title = 'New Users'

    def get_value(self):
#        owners = User.objects.distinct().count()
        owners = 10
        return owners

    def get_detail(self):
        return '10 actives'

    def get_more_info(self):
        return '10 fakes'
