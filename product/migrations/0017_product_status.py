# Generated by Django 3.2.4 on 2021-07-01 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20210629_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Pending', 'Pending')], default='Pending', max_length=100),
        ),
    ]