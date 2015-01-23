# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_geoip', '0002_steps_error_boundary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('clue', models.TextField()),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('error_boundary', models.FloatField(default=0.5, help_text=b'How far can you be from the point (in Km)')),
                ('step_number', models.IntegerField()),
                ('tour', models.ForeignKey(related_name='steps', to='photo_geoip.Tour')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='steps',
            name='tour',
        ),
        migrations.DeleteModel(
            name='Steps',
        ),
    ]
