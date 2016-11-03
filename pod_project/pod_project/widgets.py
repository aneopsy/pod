# -*- encoding: utf-8 -*-
from pods.models import Pod, Channel, Type, Discipline
from django.contrib.auth.models import User

from dashing.widgets import ListWidget
from dashing.widgets import NumberWidget
from dashing.widgets import KnobWidget
from random import randint
from time import gmtime, strftime
import os
import math


class SpaceWidget(KnobWidget):
    title = 'Space'

    def file_size_mo(self, size):
        size_name = ('Octets', 'Kio', 'Mio', 'Gio', 'Tio', 'Pio', 'Eio', 'Zio', 'Yio')
        try:
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size/p, 2)
            if (s > 0):
                return '%.1f %s' % (s, size_name[i])
            else:
                return '0 octets'
        except:
            return '0 octets'


    def disk_usage(self, path):
        """Return disk usage statistics about the given path.

        Returned valus is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        percent = (used * 100) / total
        return (total, used, free, percent)

    def get_value(self):
        space = self.disk_usage('/')
        return space[3]

    def get_more_info(self):
        space = self.disk_usage('/')
        return '%s free \n %s used \n %s' % (self.file_size_mo(space[2]), self.file_size_mo(space[1]), self.file_size_mo(space[0]))


class ServerWidget(NumberWidget):
    title = 'Server'

    def get_value(self):
        return 'On'

    def get_updated_at(self):
        return u'Last updated: {}' . format(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


class VideosWidget(NumberWidget):
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
        return '%d actives' % nbr_video

    def get_more_info(self):
        owners = User.objects.distinct().count()
        return '%d Owners' % owners


class UsersWidget(ListWidget):
    title = 'Users'

    more_info = ''

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

    def get_data(self):
        channels = []
        values = []
        for user in Channel.objects.distinct():
            channels.append(user.title)
            values.append(user.video_count())
        return [{'label': x, 'value': y} for x, y in zip(channels, values)]


class DisciplinesWidget(ListWidget):
    title = 'Disciplines'
    more_info = ''

    def get_data(self):
        disciplines = []
        values = []
        for user in Discipline.objects.distinct():
            disciplines.append(user.title)
            values.append(user.video_count())
        return [{'label': x, 'value': y} for x, y in zip(disciplines, values)]
