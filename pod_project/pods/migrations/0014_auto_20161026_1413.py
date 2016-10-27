# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pods', '0013_pod_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pod',
            name='file_size',
            field=models.IntegerField(default=0, verbose_name='Size', editable=False, blank=True),
        ),
    ]
