# Generated by Django 3.2.9 on 2021-11-06 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0002_auto_20211106_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]