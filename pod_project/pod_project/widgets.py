# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User

from dashing.widgets import ListWidget
from dashing.widgets import NumberWidget
from random import randint


class NewClientsWidget(NumberWidget):
    title = 'Videos'

    def get_value(self):
        nbr_video = 0
        for user in User.objects.distinct():
            nbr_video += user.pod_set.distinct().count()
        return '%s' % nbr_video

    def get_detail(self):
        nbr_video = 0
        for user in User.objects.distinct():
            nbr_video += user.pod_set.filter(is_draft=False, encodingpods__gt=0).distinct().count()
        return '%d actives videos' % nbr_video

    def get_more_info(self):
        owners = User.objects.distinct().count()
        return '%d Owners' % owners


class UsersWidget(ListWidget):
    title = 'Users'
    more_info = 'Those who have more requests'

    def get_updated_at(self):
        return u'Last updated'

    def get_data(self):
        user = ['salut', 'oki']
        nbr = [10, 23]
        return [{'label': x, 'value': y} for x, y in zip(user, nbr)]
#        return [{'label': x, 'value': y} for x, y in zip(user.username, user.pod_set.filter(is_draft=False, encodingpods__gt=0).distinct().count())]
