# -*- encoding: utf-8 -*-
from pods.models import Pod, Channel, Type, Discipline
from django.contrib.auth.models import User

from dashing.widgets import ListWidget
from dashing.widgets import NumberWidget
from dashing.widgets import KnobWidget
from random import randint
import os
import math
import psutil
import time

def file_size_mo(size):
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


def convertColor(percent):
    b = 0
    if percent < 50:
        r = percent * 5.1
        g = 255
    else:
        r = 255
        g = (100 - percent) * 5.1
    return (r, g, b)


class ProcessorWidget(KnobWidget):
    title = 'Processor'

    def __init__(self):
        self.percent = psutil.cpu_percent(interval=1)
        self.net = psutil.net_io_counters()

    def get_value(self):
        return self.percent

    def get_more_info(self):
        return '%s Tx | %s Rx' % (file_size_mo(self.net.bytes_sent), file_size_mo(self.net.bytes_recv))

    def get_data(self):
        return {'readOnly': True, 'fgColor': '#%02x%02x%02x' % convertColor(self.percent)}


class MemoryWidget(KnobWidget):
    title = 'Memory'

    def __init__(self):
        self.space = psutil.virtual_memory()
        self.percent = (self.space.used * 100) / self.space.total

    def get_value(self):
        return self.percent

    def get_more_info(self):
        return '%s free | %s used | %s total' % (file_size_mo(self.space.free), file_size_mo(self.space.used), file_size_mo(self.space.total))

    def get_data(self):
        return {'readOnly': True, 'fgColor': '#%02x%02x%02x' % convertColor(self.percent)}


class SpaceWidget(KnobWidget):
    title = 'Disk'

    def __init__(self):
        self.space = psutil.disk_usage('/')

    def get_value(self):
        return self.space.percent

    def get_more_info(self):
        return '%s free | %s used | %s total' % (file_size_mo(self.space.free), file_size_mo(self.space.used), file_size_mo(self.space.total))

    def get_data(self):
        return {'readOnly': True, 'fgColor': '#%02x%02x%02x' % convertColor(self.space.percent)}


class ServerWidget(NumberWidget):
    title = 'Server'

    def get_value(self):
        return 'On'

    def get_updated_at(self):
        return u'Last updated: {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


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
        return '%d Users' % owners


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
