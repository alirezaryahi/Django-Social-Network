# Generated by Django 3.1.5 on 2021-01-12 22:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])]),
        ),
    ]