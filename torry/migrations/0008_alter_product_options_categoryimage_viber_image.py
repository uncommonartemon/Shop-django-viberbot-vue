# Generated by Django 4.2.1 on 2023-06-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torry', '0007_product_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товар'},
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='viber_image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
