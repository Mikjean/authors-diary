# Generated by Django 3.2.9 on 2021-11-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0004_auto_20211108_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='user_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
