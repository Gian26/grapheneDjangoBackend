# Generated by Django 2.0.5 on 2018-05-31 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='noticias',
            old_name='publish',
            new_name='public',
        ),
    ]
