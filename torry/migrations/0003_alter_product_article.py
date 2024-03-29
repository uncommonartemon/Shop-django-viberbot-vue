# Generated by Django 4.2 on 2023-05-14 11:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torry', '0002_color_color_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator('^-?\\d{1,30}$', 'ID должен содержать только цифры и знак минуса.')], verbose_name='Номер/Артикль'),
        ),
    ]
