# Generated by Django 4.2 on 2023-05-14 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color_translation',
            field=models.CharField(default=None, max_length=40, verbose_name='Название цвета'),
            preserve_default=False,
        ),
    ]