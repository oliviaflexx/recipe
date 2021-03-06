# Generated by Django 3.2.4 on 2021-07-04 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_auto_20210704_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='recipe_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_amount', models.IntegerField()),
                ('ingredient_unit', models.CharField(max_length=50)),
                ('ingredient_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipe_list', to='main.ingredients3')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
