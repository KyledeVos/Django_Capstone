# Generated by Django 4.2.4 on 2023-09-23 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crafts_by_micks', '0038_alter_order_delivered_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_received_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='submitted_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]