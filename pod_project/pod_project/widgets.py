# -*- encoding: utf-8 -*-
from pods.models import Pod, Channel, Type, Discipline
from django.contrib.auth.models import User

from dashing.widgets import ListWidget
from dashing.widgets import NumberWidget
from dashing.widgets import KnobWidget
from random import randint
from time import gmtime, strftime
import os
from collections import namedtuple

_ntuple_diskusage = namedtuple('usage', 'total used free percent')


class SpaceWidget(KnobWidget):
    title = 'Space'
    def file_size_mo(self, size):
        abbrevs = ((1 << 30L, 'Gio'),
                   (1 << 20L, 'Mio'),
                   (1 << 10L, 'Kio'),
                   (1, 'octet'))
        if size == 0:
            return 'None'
        for factor, suffix in abbrevs:
            if (size >= factor):
                break
        return '%.*f %s' % (2, self.file_size / factor, suffix)

    def disk_usage(self, path):
        """Return disk usage statistics about the given path.

        Returned valus is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        percent = (used / total * 100)
        return _ntuple_diskusage(total, used, free, percent)

    def get_value(self):
        space = self.disk_usage('/')
        print(space)
        return 10

    def get_more_info(self):
        return str(self.disk_usage('/')[1])


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
