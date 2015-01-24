# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0009_tour_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
