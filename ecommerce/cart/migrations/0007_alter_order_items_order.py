# Generated by Django 5.2.3 on 2025-07-09 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_order_delivery_status_order_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_items',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cart.order'),
        ),
    ]
