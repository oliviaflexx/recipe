# Generated by Django 3.2.4 on 2021-07-13 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210708_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_recipes',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]