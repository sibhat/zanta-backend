# Generated by Django 2.2.1 on 2019-05-17 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zantapp', '0004_auto_20190517_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]