# Generated by Django 5.1.1 on 2024-10-04 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_alter_branch_options_remove_truck_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='number',
            field=models.CharField(max_length=20, verbose_name='Number'),
        ),
    ]
