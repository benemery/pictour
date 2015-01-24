# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photo_geoip', '0004_auto_20150123_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('step', models.ForeignKey(to='photo_geoip.Step')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('current_step', models.IntegerField(default=1)),
                ('completed', models.BooleanField(default=False)),
                ('tour', models.ForeignKey(to='photo_geoip.Tour')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userstep',
            name='user_tour',
            field=models.ForeignKey(to='photo_geoip.UserTour'),
            preserve_default=True,
        ),
    ]
