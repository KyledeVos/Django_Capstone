# Generated by Django 4.2.4 on 2023-09-21 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0033_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_item',
            name='options',
            field=models.TextField(default=None),
        ),
    ]
