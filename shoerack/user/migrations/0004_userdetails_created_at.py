# Generated by Django 4.1.4 on 2023-08-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_user_userdetails_userr'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
    ]
