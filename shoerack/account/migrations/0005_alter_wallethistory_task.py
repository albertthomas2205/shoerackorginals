# Generated by Django 4.1.4 on 2023-09-07 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_usercoupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='task',
            field=models.CharField(max_length=100),
        ),
    ]