# Generated by Django 4.1.4 on 2023-07-30 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0008_product_image_alter_productimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=2, upload_to='product_images/'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
