# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User

from dashing.widgets import NumberWidget
from random import randint


class NewClientsWidget(NumberWidget):
    title = 'Users'

    def get_value(self):
        nbr_video = 0
        for user in User.objects.distinct():
            nbr_video += user.pod_set.distinct().count()
        return '%s videos' % nbr_video

    def get_detail(self):
        nbr_video = 0
        for user in User.objects.distinct():
            nbr_video += user.pod_set.filter(is_draft=False, encodingpods__gt=0).distinct().count()
        return '%d actives videos' % nbr_video

    def get_more_info(self):
        owners = User.objects.distinct().count()
        return owners
