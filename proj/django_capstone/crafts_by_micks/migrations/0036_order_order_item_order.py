# Generated by Django 4.2.4 on 2023-09-22 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crafts_by_micks', '0035_remove_order_item_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_date', models.DateTimeField(default=None)),
                ('total_value', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('ns', 'not_submitted'), ('r', 'receieved'), ('p', 'paid'), ('c', 'completed')], max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order_item',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crafts_by_micks.order'),
        ),
    ]