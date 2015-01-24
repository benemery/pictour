# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0012_tour_punchline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='punchline',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
