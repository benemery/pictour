# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='steps',
            name='error_boundary',
            field=models.FloatField(default=0.5, help_text=b'How far can you be from the point (in Km)'),
            preserve_default=True,
        ),
    ]
