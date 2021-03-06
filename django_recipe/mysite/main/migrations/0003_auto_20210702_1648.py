# Generated by Django 3.2.4 on 2021-07-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210702_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='genres3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='recipes3',
            name='genre',
            field=models.ManyToManyField(related_name='recipes', to='main.genres3'),
        ),
    ]
