# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0006_userstep_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertour',
            name='current_step',
        ),
        migrations.AlterField(
            model_name='userstep',
            name='user_tour',
            field=models.ForeignKey(related_name='completed_steps', to='photo_geoip.UserTour'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usertour',
            name='user',
            field=models.ForeignKey(related_name='tours', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
