# Generated by Django 3.0.10 on 2020-10-23 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0004_auto_20201006_1352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ('domain',), 'verbose_name': 'site', 'verbose_name_plural': 'sites'},
        ),
    ]