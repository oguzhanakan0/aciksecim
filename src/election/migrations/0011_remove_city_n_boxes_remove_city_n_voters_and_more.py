# Generated by Django 4.2.1 on 2023-05-23 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0010_city_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='n_boxes',
        ),
        migrations.RemoveField(
            model_name='city',
            name='n_voters',
        ),
        migrations.AddField(
            model_name='district',
            name='n_boxes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='district',
            name='n_voters',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]