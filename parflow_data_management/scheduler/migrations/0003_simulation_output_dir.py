# Generated by Django 3.0.10 on 2021-02-17 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20210217_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='output_dir',
            field=models.CharField(default='default_path', max_length=100),
            preserve_default=False,
        ),
    ]
