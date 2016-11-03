# -*- encoding: utf-8 -*-
from dashing.widgets import NumberWidget
from random import randint
from django.contrib.auth.models import User

class NewClientsWidget(NumberWidget):
    title = 'New Users'

    def get_value(self):
        owner = User.objects.filter(pod__in=Pod.objects.filter(
            is_draft=False,
            encodingpods__gt=0).distinct()).order_by('last_name').distinct()
        return owner.count()

    def get_detail(self):
        return Video.objects.filter(categories__in=self.categories.all()).filter(is_draft=False).count()
        return '{} actives'.format(users/3)

    def get_more_info(self):
        return self.pod_set.filter(is_draft=False, encodingpods__gt=0).distinct().count()
        return '{} fakes'.format(users/10)
