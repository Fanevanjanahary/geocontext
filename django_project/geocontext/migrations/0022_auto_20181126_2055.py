# Generated by Django 2.1.3 on 2018-11-26 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geocontext', '0021_auto_20181123_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contextgroup',
            old_name='is_graph',
            new_name='graphable',
        ),
    ]