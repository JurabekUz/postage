# Generated by Django 5.1.1 on 2024-10-04 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_inventory_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='order_number',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
