# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0003_auto_20150123_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauthtokens',
            name='cursor',
            field=models.CharField(default=b'', max_length=2048, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userauthtokens',
            name='dropbox_uid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
