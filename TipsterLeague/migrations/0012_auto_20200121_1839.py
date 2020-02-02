# Generated by Django 3.0.2 on 2020-01-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TipsterLeague', '0011_auto_20200119_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('SC', 'Scheduled'), ('FI', 'Finished')], default='SC', max_length=2),
        ),
        migrations.AlterField(
            model_name='matchprediction',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Settled')], default='P', max_length=1),
        ),
    ]