# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0012_auto_20161025_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='pod',
            name='file_size',
            field=models.IntegerField(default=0, verbose_name='Duration', editable=False, blank=True),
        ),
    ]
