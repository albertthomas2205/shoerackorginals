# Generated by Django 4.1.4 on 2023-09-07 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0018_productimage_crop_height_productimage_crop_width_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='crop_height',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_width',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_x',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='crop_y',
        ),
    ]
