# Generated by Django 4.2.4 on 2023-09-02 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0015_remove_product_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_sizes',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crafts_by_micks.product'),
        ),
    ]