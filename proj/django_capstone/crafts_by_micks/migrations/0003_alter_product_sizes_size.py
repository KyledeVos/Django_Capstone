# Generated by Django 4.2.4 on 2023-09-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0002_rename_price_product_base_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_sizes',
            name='size',
            field=models.CharField(choices=[('n', 'none'), ('xs', 'extra-small'), ('sm', 'small'), ('m', 'medium'), ('lg', 'large'), ('xl-large', 'extra-large'), ('xxl', 'XXL')], max_length=15),
        ),
    ]
