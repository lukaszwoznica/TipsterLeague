# Generated by Django 3.0.2 on 2020-01-15 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TipsterLeague', '0003_auto_20200115_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='gameweek',
        ),
        migrations.DeleteModel(
            name='Gameweek',
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
