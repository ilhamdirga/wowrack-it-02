# Generated by Django 4.2.1 on 2023-05-22 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory_tray_detector', '0003_rename_jumlah_gallery_quantity_gallery_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='picture',
            field=models.ImageField(null=True, upload_to='memory_tray_detector'),
        ),
    ]