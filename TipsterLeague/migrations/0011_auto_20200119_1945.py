# Generated by Django 3.0.2 on 2020-01-19 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TipsterLeague', '0010_matchprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchprediction',
            name='correct_match_result',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='matchprediction',
            name='correct_score',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='matchprediction',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Settled')], default='S', max_length=1),
        ),
    ]