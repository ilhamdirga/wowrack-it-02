# Generated by Django 4.2.1 on 2023-05-24 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory_tray_detector', '0010_alter_camcard_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
