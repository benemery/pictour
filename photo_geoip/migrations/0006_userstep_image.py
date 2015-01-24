# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0005_auto_20150124_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstep',
            name='image',
            field=models.ImageField(default='', upload_to=b''),
            preserve_default=False,
        ),
    ]
