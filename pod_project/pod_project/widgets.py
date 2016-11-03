# -*- encoding: utf-8 -*-
from pods.models import Pod, Channel, Type, Discipline
from django.contrib.auth.models import User

from dashing.widgets import ListWidget
from dashing.widgets import NumberWidget
from random import randint
from time import gmtime, strftime


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

    more_info = ''

    def get_updated_at(self):
        return u'Last updated: {}' . format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    def get_data(self):
        users = []
        values = []
        for user in User.objects.distinct():
            users.append(user.username)
            values.append(user.pod_set.filter(is_draft=False, encodingpods__gt=0).distinct().count())
        return [{'label': x, 'value': y} for x, y in zip(users, values)]


class ChannelsWidget(ListWidget):
    title = 'Channels'
    more_info = ''

    def get_updated_at(self):
        return u'Last updated: {}' . format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    def get_data(self):
        users = []
        values = []
        for user in Channel.objects.distinct():
            users.append(user.title)
            values.append(user.video_count())
        return [{'label': x, 'value': y} for x, y in zip(users, values)]
