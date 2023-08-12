# Generated by Django 4.1.4 on 2023-08-03 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0014_brand_rename_name_category_category_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AddField(
            model_name='productsize',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]