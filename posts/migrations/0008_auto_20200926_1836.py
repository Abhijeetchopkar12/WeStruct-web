# Generated by Django 3.1.1 on 2020-09-26 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_author_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='rating',
        ),
        migrations.AddField(
            model_name='author',
            name='verified_tick',
            field=models.BooleanField(default=False),
        ),
    ]
