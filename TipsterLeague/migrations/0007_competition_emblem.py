# Generated by Django 3.0.2 on 2020-01-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TipsterLeague', '0006_auto_20200115_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='emblem',
            field=models.CharField(max_length=255, null=True),
        ),
    ]