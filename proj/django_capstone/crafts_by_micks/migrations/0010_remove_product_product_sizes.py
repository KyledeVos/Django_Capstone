# Generated by Django 4.2.4 on 2023-09-02 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0009_product_product_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_sizes',
        ),
    ]