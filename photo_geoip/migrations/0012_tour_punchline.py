# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0011_auto_20150124_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='punchline',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
