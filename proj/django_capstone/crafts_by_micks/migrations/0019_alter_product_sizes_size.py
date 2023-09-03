# Generated by Django 4.2.4 on 2023-09-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0018_rename_options_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_sizes',
            name='size',
            field=models.CharField(choices=[('xs', 'extra-small'), ('sm', 'small'), ('m', 'medium'), ('lg', 'large'), ('xl-large', 'extra-large'), ('xxl', 'XXL')], max_length=15),
        ),
    ]
