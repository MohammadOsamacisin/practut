# Generated by Django 3.2 on 2021-06-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='main_product/'),
        ),
    ]
